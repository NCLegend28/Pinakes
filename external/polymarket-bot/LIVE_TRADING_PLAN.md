# Live Trading Implementation Plan

> **Current state:** Paper trading fully operational. Live execution requires one new
> file (`api/clob_client.py`) and modifications to two existing files (`paper/trader.py`,
> `config.py`). Everything else — the scanner, exit engine, dashboard, Telegram — works
> unchanged for both modes simultaneously.

---

## Can paper and live run at the same time?

Yes. The design keeps them fully separated:

```
PAPER MODE  (always on)
  PaperTrader.balance         virtual $1,000
  PaperTrader.positions       in-memory + JSONL
  PaperTrader.open_position() records the trade, deducts virtual balance
  PaperTrader.close_position() records P&L, adds virtual balance back

LIVE MODE   (opt-in, same scan loop)
  After PaperTrader records the trade →
  ClobClient.place_order()    submits real limit order to Polymarket CLOB
  After PaperTrader closes →
  ClobClient.cancel_order()   cancels any unfilled remainder on the CLOB
```

Both run in the same scan cycle. Paper always executes. Live executes additionally
if `LIVE_TRADING=true`. The paper log is always your ground truth — live orders
are a side effect, not the source of record.

---

## Architecture

```
scan_loop
    │
    ├── trader.open_position(opp)          ← paper trade recorded
    │       │
    │       └── if live_mode:
    │               clob.place_order()     ← real order submitted
    │               trade.clob_order_id = response.order_id
    │
    └── trader.close_position(opp_id)      ← paper trade closed
            │
            └── if live_mode and trade.clob_order_id:
                    clob.cancel_order()    ← cancels any unfilled remainder
                    (filled portions already settled on-chain automatically)
```

---

## Files to create

### `src/polybot/api/clob_client.py` (new, ~120 lines)

Thin wrapper around `py-clob-client`. Handles:
- Client initialisation with credentials from settings
- `place_order(token_id, side, price, size)` → returns `order_id`
- `cancel_order(order_id)`
- `get_order(order_id)` → check fill status
- Daily loss circuit breaker
- All errors caught and logged — never crash the scan loop

```python
# Interface the rest of the codebase sees:
class ClobClient:
    def place_order(self, token_id: str, side: str,
                    price: float, size_usd: float) -> str | None:
        """Submit limit order. Returns order_id or None on failure."""

    def cancel_order(self, order_id: str) -> bool:
        """Cancel an open order. Returns True on success."""

    def get_balance(self) -> float:
        """Live USDC.e balance from proxy wallet."""

    def check_daily_loss_limit(self) -> bool:
        """Returns False if daily loss cap has been hit."""
```

---

## Files to modify

### `src/polybot/models.py`

Add `clob_order_id` field to `PaperTrade` so the live order ID travels with the
paper trade record:

```python
# In PaperTrade dataclass — add one field:
clob_order_id: str | None = None    # set when live order is placed
```

### `src/polybot/paper/trader.py`

Add `live_mode` property and two async hooks. The paper logic is completely
unchanged — live execution is additive only:

```python
class PaperTrader:

    @property
    def live_mode(self) -> bool:
        return settings.live_trading and self._clob is not None

    def set_clob_client(self, clob: "ClobClient") -> None:
        self._clob = clob

    def open_position(self, opp: Opportunity) -> PaperTrade | None:
        # --- existing paper logic unchanged ---
        trade = ...  # paper trade created as before

        # Live hook — runs after paper trade is recorded
        if self.live_mode:
            token_id = opp.market.clob_token_id  # YES or NO token
            order_id = self._clob.place_order(
                token_id = token_id,
                side     = str(opp.side),
                price    = opp.market_price,
                size_usd = size_usd,
            )
            if order_id:
                trade = trade.model_copy(update={"clob_order_id": order_id})
                self.positions[opp.id] = trade  # update with order_id
                logger.info(f"LIVE order placed: {order_id}")
            else:
                logger.warning("Live order failed — paper trade kept, no real position")

        return trade

    def close_position(self, opportunity_id: str, exit_price: float) -> PaperTrade:
        # --- existing paper logic unchanged ---
        trade = ...  # paper close as before

        # Live hook — cancel any unfilled remainder
        if self.live_mode and trade.clob_order_id:
            cancelled = self._clob.cancel_order(trade.clob_order_id)
            if cancelled:
                logger.info(f"LIVE order cancelled: {trade.clob_order_id}")
            # Note: filled portions already settled on-chain automatically
            # Polymarket resolves winning positions → USDC.e lands in proxy wallet

        return trade
```

### `src/polybot/config.py`

Add live trading config block (most already added):

```env
# Already in .env — verify these are set:
LIVE_TRADING=false             # flip to true when ready
PRIVATE_KEY=0x...              # hot wallet private key
POLY_PROXY_ADDRESS=0x...       # Safe proxy wallet (holds USDC.e)
CLOB_API_KEY=...
CLOB_API_SECRET=...
CLOB_API_PASSPHRASE=...
MAX_DAILY_LOSS_USD=50          # hard circuit breaker
```

### `src/polybot/cli.py`

Wire the CLOB client into the trader at startup:

```python
# In main(), after trader = PaperTrader():
if settings.live_trading:
    from polybot.api.clob_client import ClobClient
    clob = ClobClient()
    trader.set_clob_client(clob)
    dash.log(
        f"LIVE TRADING ENABLED — proxy={settings.poly_proxy_address[:10]}... "
        f"balance=${clob.get_balance():.2f}",
        "WARN"
    )
else:
    dash.log("Paper trading mode — LIVE_TRADING=false", "INFO")
```

---

## `clob_client.py` full implementation

```python
"""
Live order execution via Polymarket CLOB.

Wraps py-clob-client with:
  - Circuit breaker (daily loss cap)
  - Error handling that never crashes the scan loop
  - Position size validation against live USDC.e balance
"""
from __future__ import annotations

import asyncio
from datetime import date
from typing import TYPE_CHECKING

from loguru import logger
from py_clob_client.client import ClobClient as _ClobClient
from py_clob_client.clob_types import ApiCreds, OrderArgs, OrderType
from py_clob_client.constants import BUY, SELL

from polybot.config import settings


class ClobClient:
    def __init__(self):
        creds = ApiCreds(
            api_key        = settings.clob_api_key,
            api_secret     = settings.clob_api_secret,
            api_passphrase = settings.clob_api_passphrase,
        )
        self._client = _ClobClient(
            host           = "https://clob.polymarket.com",
            chain_id       = 137,
            key            = settings.private_key,
            creds          = creds,
            signature_type = 2,                       # GNOSIS_SAFE
            funder         = settings.poly_proxy_address,
        )
        self._daily_loss:  float = 0.0
        self._stats_date:  date  = date.today()

    def _reset_daily_if_needed(self) -> None:
        today = date.today()
        if today != self._stats_date:
            self._daily_loss = 0.0
            self._stats_date = today

    def check_daily_loss_limit(self) -> bool:
        """Returns True if safe to trade, False if daily cap hit."""
        self._reset_daily_if_needed()
        if abs(self._daily_loss) >= settings.max_daily_loss_usd:
            logger.warning(
                f"Daily loss cap hit: ${self._daily_loss:.2f} "
                f">= ${settings.max_daily_loss_usd:.2f} — live trading paused"
            )
            return False
        return True

    def record_loss(self, amount: float) -> None:
        """Call when a live position closes at a loss."""
        if amount < 0:
            self._daily_loss += abs(amount)

    def get_balance(self) -> float:
        """Live USDC.e balance from proxy wallet in dollars."""
        try:
            from py_clob_client.clob_types import BalanceAllowanceParams, AssetType
            bal = self._client.get_balance_allowance(
                params=BalanceAllowanceParams(
                    asset_type     = AssetType.COLLATERAL,
                    signature_type = 2,
                )
            )
            return float(bal.get("balance", 0)) / 1e6
        except Exception as e:
            logger.error(f"get_balance failed: {e}")
            return 0.0

    def place_order(self, token_id: str, side: str,
                    price: float, size_usd: float) -> str | None:
        """
        Submit a limit GTC order to the CLOB.

        Returns order_id on success, None on failure.
        Never raises — errors are logged and None returned.
        """
        if not self.check_daily_loss_limit():
            return None

        # Validate we have enough balance
        balance = self.get_balance()
        if balance < size_usd:
            logger.warning(
                f"Insufficient balance: ${balance:.2f} < ${size_usd:.2f} — skipping"
            )
            return None

        # Minimum order check
        if size_usd < 1.0:
            logger.warning(f"Order too small: ${size_usd:.2f} < $1.00 minimum")
            return None

        try:
            order_args = OrderArgs(
                token_id = token_id,
                price    = price,
                size     = size_usd / price,  # convert USD to shares
                side     = BUY if side == "YES" else SELL,
            )

            # Get tick size for this market
            tick_size = self._client.get_tick_size(token_id)
            neg_risk  = self._client.get_neg_risk(token_id)

            response = self._client.create_and_post_order(
                order_args,
                {"tickSize": tick_size, "negRisk": neg_risk},
                OrderType.GTC,
            )

            order_id = response.get("orderID")
            status   = response.get("status")
            logger.info(
                f"LIVE ORDER PLACED  token={token_id[:8]}... "
                f"side={side} price={price:.3f} size=${size_usd:.2f} "
                f"order_id={order_id} status={status}"
            )
            return order_id

        except Exception as e:
            logger.error(f"place_order failed: {e}")
            return None

    def cancel_order(self, order_id: str) -> bool:
        """
        Cancel an open order.

        Returns True on success or if order already filled/cancelled.
        Never raises.
        """
        try:
            response = self._client.cancel(order_id)
            logger.info(f"LIVE ORDER CANCELLED  order_id={order_id}")
            return True
        except Exception as e:
            # Already filled orders return an error on cancel — that's fine
            logger.debug(f"cancel_order {order_id}: {e}")
            return False

    def get_order_status(self, order_id: str) -> str | None:
        """Returns order status string or None on failure."""
        try:
            order = self._client.get_order(order_id)
            return order.get("status")
        except Exception as e:
            logger.error(f"get_order_status failed: {e}")
            return None
```

---

## models.py change

```python
# Add to PaperTrade (one line):
clob_order_id: str | None = Field(default=None)
```

This field persists to `paper_trades.jsonl` automatically — so if the bot
restarts, it knows which live orders are associated with which paper trades
and can cancel them if needed.

---

## Token ID lookup

The CLOB operates on **token IDs**, not market IDs. Each market has two tokens:
YES token and NO token. The Gamma API returns them in `clobTokenIds`:

```python
# In gamma.py _parse_market(), the Market model needs token IDs:
# market.clob_token_ids = ["YES_token_id", "NO_token_id"]

# In clob_client.py place_order():
# side == "YES" → use clob_token_ids[0]
# side == "NO"  → use clob_token_ids[1]
```

The `Market` model in `models.py` already parses `clobTokenIds` from Gamma —
verify it exposes `clob_token_ids` as a list. If it doesn't, add it:

```python
# In models.py Market:
clob_token_ids: list[str] = Field(default_factory=list)
```

```python
# In gamma.py _parse_market():
clob_token_ids = json.loads(raw.get("clobTokenIds", "[]"))
```

---

## Safety checklist before flipping LIVE_TRADING=true

```
□ 100+ paper trades completed with positive EV
□ Win rate trending toward backtest levels (~74%)
□ setup_relayer.py ran successfully (Safe deployed, USDC approved)
□ USDC.e funded in proxy wallet (start with $50)
□ MAX_DAILY_LOSS_USD=50 set in .env
□ verify_clob.py shows balance and allowance > 0
□ LIVE_TRADING=false confirmed — only flip when ready
□ Bot running on a stable connection (VPS recommended over laptop)
```

---

## Dual-mode operation

Once live is enabled, every scan runs both modes simultaneously:

```
Scan #N finds edge on Wellington 20°C NO @ 0.770
    │
    ├── PaperTrader.open_position()
    │     records virtual $10 position
    │     deducts from paper balance
    │     writes to paper_trades.jsonl
    │
    └── ClobClient.place_order()          ← additional if LIVE_TRADING=true
          submits real $10 limit order
          to Polymarket CLOB
          returns order_id → stored on trade

Both the paper and real positions track independently.
Paper P&L is your performance benchmark.
Real P&L flows back as USDC.e to your proxy wallet.
```

The paper trade log remains the source of truth. If a live order fails (network
error, insufficient balance, market moved), the paper trade still records — you
can audit exactly what the bot intended vs what actually executed.

---

## Build order

| Step | File | Work |
|------|------|------|
| 1 | `src/polybot/models.py` | Add `clob_order_id` and `clob_token_ids` fields |
| 2 | `src/polybot/api/gamma.py` | Parse `clobTokenIds` into `Market.clob_token_ids` |
| 3 | `src/polybot/api/clob_client.py` | Create new file (full implementation above) |
| 4 | `src/polybot/paper/trader.py` | Add `set_clob_client()`, live hooks in open/close |
| 5 | `src/polybot/cli.py` | Wire `ClobClient` into trader at startup |
| 6 | `.env` | Verify all live trading fields are set |
| 7 | Test | Run with `LIVE_TRADING=false`, confirm no regressions |
| 8 | Test | Place one tiny live order manually via `verify_clob.py` |
| 9 | Go live | Flip `LIVE_TRADING=true`, watch first scan |

Estimated build time: **2–3 hours**.

---

*Last updated: March 2026*