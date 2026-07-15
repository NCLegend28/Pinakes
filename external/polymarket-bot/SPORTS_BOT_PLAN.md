# Polymarket Sports Bot — Implementation Plan v2

> Two completely separate systems. The weather bot uses the Global API.
> The sports bot uses the US API. They never share a client, never share
> credentials, never share an endpoint. Clean walls between them.
>
> **Target:** Live sports trading on Polymarket US.
> **Timeline:** ~2 weeks to first live sports trade.
> **Docs:** https://docs.polymarket.us/getting-started/quickstart

---

## The Two Platforms (Hard Separation)

These are **not** two versions of the same API. They are different products
run by different legal entities with different infrastructure.

```
┌──────────────────────────────────┐  ┌──────────────────────────────────┐
│     GLOBAL PLATFORM (existing)   │  │     US PLATFORM (new)            │
│                                  │  │                                  │
│  Entity:  Polymarket (offshore)  │  │  Entity:  QCX LLC (CFTC-reg'd)  │
│  Site:    polymarket.com         │  │  Site:    polymarket.us          │
│  API:     clob.polymarket.com    │  │  API:     api.polymarket.us      │
│           gamma-api.polymarket.  │  │                                  │
│  Auth:    EIP-712 wallet signing │  │  Auth:    Ed25519 key signing    │
│  SDK:     py-clob-client         │  │  SDK:     polymarket-us          │
│  Creds:   PRIVATE_KEY +          │  │  Creds:   POLYMARKET_KEY_ID +    │
│           CLOB_API_KEY/SECRET/   │  │           POLYMARKET_SECRET_KEY  │
│           PASSPHRASE             │  │                                  │
│  Wallet:  Safe proxy (0xE64f...) │  │  Account: KYC'd, managed by app │
│  Chain:   Polygon (USDC.e)       │  │  Chain:   Abstracted (no wallet) │
│  Markets: weather, crypto, etc.  │  │  Markets: sports only (for now)  │
│  Status:  GEOBLOCKED for orders  │  │  Status:  LIVE for US users      │
│           (price data still OK)  │  │                                  │
│                                  │  │                                  │
│  Used by: Weather bot (paper)    │  │  Used by: Sports bot (live)      │
│           Sports bot (READ ONLY  │  │           (execution only)       │
│            — price signals)      │  │                                  │
└──────────────────────────────────┘  └──────────────────────────────────┘
```

### Three-Layer Signal Architecture

The sports bot's edge comes from comparing prices across three sources:

```
┌─────────────────────────────────────────────────────────────────────┐
│                     SPORTS BOT DATA FLOW                            │
│                                                                     │
│  LAYER 1 — Global Polymarket (Gamma API)     ◄── PRIMARY SIGNAL    │
│  │  3,500+ sports markets, $700M+ volume                           │
│  │  Free, unlimited, no auth, NOT geoblocked for reads             │
│  │  Smart money + bots + global liquidity = best price discovery   │
│  │  Uses existing gamma.py (already built for weather bot)         │
│  │                                                                  │
│  LAYER 2 — Sportsbook Consensus (The Odds API)  ◄── CONFIRMATION  │
│  │  15+ sportsbooks aggregated, de-vigged                          │
│  │  500 req/month free tier (fine as secondary, not primary)       │
│  │  Confirms or contradicts Layer 1 signal                         │
│  │                                                                  │
│  LAYER 3 — Polymarket US (US SDK)            ◄── EXECUTION TARGET  │
│     New platform, thinner liquidity, retail-heavy user base        │
│     This is where we actually TRADE                                │
│     Price discrepancy vs Layer 1 = THE EDGE                        │
│                                                                     │
│  EDGE = Global Price (Layer 1) - US Price (Layer 3)                │
│  CONFIRMATION = Sportsbook Odds (Layer 2) agrees with Layer 1     │
└─────────────────────────────────────────────────────────────────────┘
```

**Analogy:** This is the same structure as the weather bot. Open-Meteo (physics
model) says "38% chance" but the market says 12¢ — that's the edge. Here,
the global Polymarket platform (billions in volume, smart money) says "65%"
but the US platform (new, retail-heavy) says 58¢ — same structure, same edge.

### API Rules

**Order execution:** Sports bot places orders ONLY through the US SDK
(`polymarket-us`). Never through the global CLOB (`py-clob-client`).

**Price reads:** Sports bot reads price signals from the Gamma API (global)
for consensus pricing. This is READ-ONLY — no auth, no wallet, no orders.
The existing `gamma.py` is reused as a shared data source, not a trading client.

**Weather bot:** Uses global API only (Gamma + CLOB for paper). Unchanged.

**The firewall:** No file places orders through both `py-clob-client` AND
`polymarket-us`. Gamma is a read-only data source shared by both bots.

---

## Prerequisites (Do These Before Coming Back)

### 1. Get off the Polymarket US waitlist
- Download the iOS app
- Use invite code: `COVERS`, `LABS`, `GOAL`, or `GRINDERS`
- Sign up with Apple or Google (remember which one — it matters later)

### 2. Complete KYC
- Government photo ID (driver's license or passport)
- SSN
- Proof of address (utility bill or bank statement, dated within 90 days)
- Wait for "Approved to Start Trading" confirmation in the app

### 3. Generate Ed25519 API keys
- Go to `polymarket.us/developer`
- **Sign in with the SAME method used in the app** (Apple/Google/email)
  - Switching sign-in methods can break API key access
- Click "Create API Key"
- You get two values: **Key ID** and **Secret Key**
- **The secret key is shown ONCE.** Copy it immediately. Store it securely.
- Save both to your `.env` as:
  ```env
  POLYMARKET_KEY_ID=your-key-id-here
  POLYMARKET_SECRET_KEY=your-secret-key-here
  ```

### 4. Fund the US account
Deposit through the app. Options:
- Credit/debit card
- Bank transfer / ACH
- Transfer USDC from an exchange (Coinbase, Crypto.com, etc.)

### 5. Migrate funds from global proxy wallet (optional)
Your USDC.e is sitting in the Safe proxy wallet on Polygon (`0xE64f...`).
To move it to the US account:

```
Global proxy wallet (0xE64f...)  →  withdraw USDC.e to your EOA/exchange
    →  send USDC from exchange to Polymarket US deposit address (shown in app)
```

**Critical:** The two platforms have separate balances. Money in your global
wallet does NOT appear in the US app. You must explicitly transfer.

### 6. Verify California is not restricted
As of March 2026, CA is clear. Blocked states: AZ, IL, MA, MD, MI, MT, NJ, NV, OH.

---

## Phase 1 — US API Client + Verification (~2 days)

### 1A. Install the Official SDK

```bash
pip install polymarket-us --break-system-packages
```

Requires Python 3.10+. This is the official SDK from Polymarket:
- PyPI: https://pypi.org/project/polymarket-us/
- GitHub: https://github.com/Polymarket/polymarket-us-python

### 1B. New Config Fields

**Add to `src/polybot/config.py`:**
```python
# ── Polymarket US (sports bot) ────────────────────────────────
# Completely separate from global CLOB credentials.
# These come from polymarket.us/developer after KYC.
polymarket_key_id: str = ""
polymarket_secret_key: str = ""
```

**Add to `.env` / `.env.example`:**
```env
# ── Polymarket US API (sports bot) ─────────────────────────────
# From polymarket.us/developer. NOT related to global CLOB keys.
POLYMARKET_KEY_ID=
POLYMARKET_SECRET_KEY=

# ── The Odds API (sports data) ─────────────────────────────────
ODDS_API_KEY=
```

Global CLOB fields (`CLOB_API_KEY`, `PRIVATE_KEY`, `POLY_PROXY_ADDRESS`, etc.)
stay untouched. The weather bot still reads them.

### 1C. New US Client Wrapper

**New file: `src/polybot/api/polymarket_us.py`**

This wraps the official SDK with our safety layer (circuit breakers, logging,
balance checks). It does NOT subclass or reference the global `ClobClient`.

```python
"""
Polymarket US API client for sports trading.

Uses the official polymarket-us SDK (Ed25519 auth).
Has NOTHING to do with the global CLOB client (py-clob-client).

Ref: https://docs.polymarket.us/getting-started/quickstart
SDK: https://docs.polymarket.us/api-reference/sdks/python/quickstart
"""

import logging
from datetime import date

from polymarket_us import PolymarketUS, AsyncPolymarketUS
from polymarket_us import (
    AuthenticationError,
    BadRequestError,
    NotFoundError,
    RateLimitError,
    APITimeoutError,
    APIConnectionError,
)

logger = logging.getLogger(__name__)


class PolymarketUSClient:
    """Wraps the official polymarket-us Python SDK with safety controls."""

    def __init__(self, key_id: str, secret_key: str, max_daily_loss: float = 50.0):
        self._client = PolymarketUS(
            key_id=key_id,
            secret_key=secret_key,
            timeout=30.0,
        )
        self._max_daily_loss = max_daily_loss
        self._daily_loss = 0.0
        self._loss_date = date.today()

    # ── Market Data (public, no auth needed) ──────────────────

    def list_events(self, limit: int = 50, active: bool = True) -> dict:
        """Fetch active events (sports games)."""
        return self._client.events.list({"limit": limit, "active": active})

    def get_market(self, slug: str) -> dict:
        """Fetch a single market by slug."""
        return self._client.markets.retrieve_by_slug(slug)

    def get_book(self, slug: str) -> dict:
        """Fetch order book for a market."""
        return self._client.markets.book(slug)

    def get_bbo(self, slug: str) -> dict:
        """Fetch best bid/offer for a market."""
        return self._client.markets.bbo(slug)

    def search_markets(self, query: str) -> dict:
        """Search markets by keyword."""
        return self._client.search.query({"query": query})

    def list_sports(self) -> dict:
        """Fetch available sports categories."""
        return self._client.sports.list()

    # ── Account (authenticated) ───────────────────────────────

    def get_balance(self) -> dict:
        """Fetch account balances."""
        return self._client.account.balances()

    def get_positions(self) -> dict:
        """Fetch open positions."""
        return self._client.portfolio.positions()

    def get_activities(self) -> dict:
        """Fetch recent account activity."""
        return self._client.portfolio.activities()

    # ── Orders (authenticated) ────────────────────────────────

    def place_order(
        self,
        market_slug: str,
        side: str,          # "YES" or "NO"
        price: float,       # 0.01 – 0.99
        quantity: int,       # number of contracts
        tif: str = "GTC",
    ) -> dict | None:
        """Place a limit order. Returns order dict or None on failure.

        Unlike the global ClobClient which silently returns None,
        this client logs the SPECIFIC error type so we always know
        exactly why an order failed.
        """
        # Daily loss circuit breaker
        if self._loss_date != date.today():
            self._daily_loss = 0.0
            self._loss_date = date.today()

        if self._daily_loss >= self._max_daily_loss:
            logger.warning("Daily loss cap ($%.2f) hit — skipping order",
                          self._max_daily_loss)
            return None

        # Map YES/NO to SDK intent strings
        # YES = BUY_LONG (you profit if outcome happens)
        # NO  = BUY_SHORT (you profit if outcome doesn't happen)
        intent = (
            "ORDER_INTENT_BUY_LONG" if side == "YES"
            else "ORDER_INTENT_BUY_SHORT"
        )

        # Map TIF shorthand to SDK constants
        tif_map = {
            "GTC": "TIME_IN_FORCE_GOOD_TILL_CANCEL",
            "IOC": "TIME_IN_FORCE_IMMEDIATE_OR_CANCEL",
            "FOK": "TIME_IN_FORCE_FILL_OR_KILL",
        }

        try:
            order = self._client.orders.create({
                "marketSlug": market_slug,
                "intent": intent,
                "type": "ORDER_TYPE_LIMIT",
                "price": {"value": str(price), "currency": "USD"},
                "quantity": quantity,
                "tif": tif_map.get(tif, "TIME_IN_FORCE_GOOD_TILL_CANCEL"),
            })
            logger.info("US ORDER PLACED: %s %s @ $%.2f x%d → id=%s",
                       side, market_slug, price, quantity,
                       order.get("id", "???"))
            return order

        except AuthenticationError as e:
            logger.error("Auth error: %s", e.message)
        except BadRequestError as e:
            logger.error("Bad request: %s", e.message)
        except RateLimitError as e:
            logger.error("Rate limited: %s", e.message)
        except NotFoundError as e:
            logger.error("Market not found '%s': %s", market_slug, e.message)
        except APITimeoutError:
            logger.error("Timeout placing order on %s", market_slug)
        except APIConnectionError as e:
            logger.error("Connection error: %s", e.message)
        except Exception as e:
            logger.error("Unexpected error placing order: %s", e)

        return None

    def cancel_order(self, order_id: str) -> dict | None:
        """Cancel an open order."""
        try:
            return self._client.orders.cancel(order_id)
        except Exception as e:
            logger.error("Cancel order %s failed: %s", order_id, e)
            return None

    def cancel_all(self) -> dict | None:
        """Cancel all open orders."""
        try:
            return self._client.orders.cancel_all()
        except Exception as e:
            logger.error("Cancel all failed: %s", e)
            return None

    def list_orders(self) -> dict:
        """Fetch all open orders."""
        return self._client.orders.list()

    def preview_order(self, params: dict) -> dict | None:
        """Preview order impact without placing it."""
        try:
            return self._client.orders.preview(params)
        except Exception as e:
            logger.error("Preview failed: %s", e)
            return None

    def close_position(self, market_slug: str) -> dict | None:
        """Close an entire position in a market."""
        try:
            return self._client.orders.close_position(market_slug)
        except Exception as e:
            logger.error("Close position '%s' failed: %s", market_slug, e)
            return None

    def record_loss(self, amount: float):
        """Track daily losses for circuit breaker."""
        if amount > 0:
            self._daily_loss += amount

    def close(self):
        """Clean up the SDK client."""
        self._client.close()
```

### 1D. Async Version for Scanner

```python
"""Async version for use inside the LangGraph scanner loop.

Ref: https://docs.polymarket.us/api-reference/sdks/python/quickstart#async-usage
"""

import asyncio
from polymarket_us import AsyncPolymarketUS

class AsyncPolymarketUSClient:
    """Async wrapper for the sports scanner pipeline."""

    def __init__(self, key_id: str, secret_key: str):
        self._client = AsyncPolymarketUS(
            key_id=key_id,
            secret_key=secret_key,
        )

    async def list_events(self, limit=50, active=True):
        return await self._client.events.list(
            {"limit": limit, "active": active}
        )

    async def get_book(self, slug: str):
        return await self._client.markets.book(slug)

    async def get_bbo(self, slug: str):
        return await self._client.markets.bbo(slug)

    async def search(self, query: str):
        return await self._client.search.query({"query": query})

    async def place_order(self, market_slug, side, price, quantity, tif="GTC"):
        intent = (
            "ORDER_INTENT_BUY_LONG" if side == "YES"
            else "ORDER_INTENT_BUY_SHORT"
        )
        return await self._client.orders.create({
            "marketSlug": market_slug,
            "intent": intent,
            "type": "ORDER_TYPE_LIMIT",
            "price": {"value": str(price), "currency": "USD"},
            "quantity": quantity,
            "tif": "TIME_IN_FORCE_GOOD_TILL_CANCEL",
        })

    async def close(self):
        await self._client.close()
```

### 1E. Verification Script

**New file: `scripts/verify_us_api.py`**

```python
"""
Verify Polymarket US API credentials.
Run ONCE after generating keys at polymarket.us/developer.

Usage:
    PYTHONPATH=src python scripts/verify_us_api.py
"""

import os
from polymarket_us import PolymarketUS

def main():
    key_id = os.environ.get("POLYMARKET_KEY_ID")
    secret_key = os.environ.get("POLYMARKET_SECRET_KEY")

    if not key_id or not secret_key:
        print("ERROR: Set POLYMARKET_KEY_ID and POLYMARKET_SECRET_KEY in .env")
        return

    print("=" * 50)
    print("Polymarket US API Verification")
    print("=" * 50)

    # 1. Public endpoints (no auth)
    print("\n1. Public endpoint test...")
    public = PolymarketUS()
    events = public.events.list({"limit": 3, "active": True})
    count = len(events.get("events", []))
    print(f"   OK — {count} events fetched")
    for e in events.get("events", [])[:3]:
        print(f"      {e.get('title', '???')}")
    public.close()

    # 2. Authenticated endpoints
    print("\n2. Authenticated endpoint test...")
    client = PolymarketUS(key_id=key_id, secret_key=secret_key)

    balances = client.account.balances()
    print(f"   OK — Balance: {balances}")

    positions = client.portfolio.positions()
    pos_count = len(positions.get("positions", []))
    print(f"   OK — Open positions: {pos_count}")

    # 3. Sports
    print("\n3. Sports endpoint test...")
    sports = client.sports.list()
    print(f"   OK — Sports: {sports}")

    # 4. Order book
    print("\n4. Order book test...")
    markets = client.markets.list({"limit": 1})
    if markets.get("markets"):
        slug = markets["markets"][0].get("slug", "")
        book = client.markets.book(slug)
        print(f"   OK — Book for '{slug}'")

    print("\n" + "=" * 50)
    print("ALL CHECKS PASSED — Ready for sports bot")
    print("=" * 50)
    client.close()

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    main()
```

---

## Phase 2 — Sports Data Pipeline (~3 days)

### 2A. Three-Layer Data Sources

| Layer | Source | Purpose | Auth | Rate Limit |
|-------|--------|---------|------|------------|
| **1 (primary)** | **Gamma API** (`gamma-api.polymarket.com`) | Global sports prices — smart money consensus | None | Unlimited, free |
| **2 (confirm)** | **The Odds API** (`the-odds-api.com`) | Sportsbook consensus from 15+ books | API key | 500 req/mo free |
| **3 (execute)** | **Polymarket US SDK** (`api.polymarket.us`) | US market prices + order placement | Ed25519 | 60 req/min public |
| **support** | **ESPN API** (unofficial) | Schedules, scores, injuries | None | Free |

**Why Gamma is Layer 1:** The global platform has 3,500+ active sports
markets with $700M+ in volume. Those prices are set by sophisticated traders
and bots putting real money behind their estimates. The Gamma API is free,
unlimited, requires no auth, and is NOT geoblocked for reads — only order
placement gets the 403. You already have `gamma.py` built and working.

**Why the US platform is Layer 3 (execution target):** It's new, retail-heavy
(sports bettors from the waitlist), and has thinner liquidity than global.
Prices on the US platform may lag behind global price discovery, creating
exploitable edges. This is the same dynamic that makes cross-platform
arbitrage profitable — the less-efficient market is where you trade.

**Why The Odds API drops to Layer 2:** Still valuable as independent
confirmation. If global Polymarket AND 15 sportsbooks agree on 65%, but
US Polymarket shows 58%, that's a high-confidence edge. But Gamma alone
gives you the primary signal — the 500/month free limit is fine for
spot-checking, not scanning.

### 2B. API Clients

**`src/polybot/api/gamma.py`** — ALREADY BUILT (shared with weather bot)
```python
# Reuse existing gamma.py to fetch global sports markets
# No changes needed — it already fetches by category keyword
# Filter for sports keywords: NBA, NFL, MLB, NHL, FIFA, etc.
# Returns: market question, yes_price, volume, token IDs
```

**`src/polybot/api/odds.py`** — NEW (secondary confirmation)
```python
class OddsClient:
    """The Odds API — sportsbook consensus as confirmation layer."""
    async fetch_odds(sport, region="us") → list[GameOdds]
    async fetch_scores(sport)            → list[GameScore]
```

**`src/polybot/api/espn.py`** — NEW (schedule/injury data)
```python
class ESPNClient:
    async fetch_schedule(league, date) → list[Game]
    async fetch_injuries(league)       → list[InjuryReport]
```

### 2C. Sports Market Discovery

**Two parallel discovery paths:**

```python
# Path 1: Global Gamma API (primary — consensus prices)
global_sports = await gamma.fetch_markets(
    category_keywords=["NBA", "NFL", "MLB", "NHL", "FIFA", "UFC",
                        "Premier League", "Champions League"],
    active=True, min_volume=500
)
# Returns: question, yes_price (global consensus), volume, liquidity

# Path 2: US SDK (execution target — where we actually trade)
us_events = await us_client.list_events(limit=100, active=True)
# Returns: slug, title, prices (US market), book depth
```

**Match global markets to US markets** by team names / event titles.
When the same game is priced differently across the two platforms, that's
the edge signal.

### 2D. Market Matching

```python
def match_global_to_us(global_market, us_markets) -> Optional[MatchedPair]:
    """
    Match a global Gamma market to its US SDK equivalent.

    Global: "Will the Los Angeles Lakers beat the Boston Celtics?"
    US:     slug="lakers-celtics-mar-29", title="Lakers vs Celtics"

    Returns a MatchedPair with both prices for edge computation.
    """
    # 1. Extract team names from global question (reuse weather parser pattern)
    # 2. Fuzzy-match against US market titles/slugs
    # 3. Return matched pair with global_price, us_price, volume, book depth
```

---

## Phase 3 — Sports Strategy Engine (~4 days)

### 3A. Core Model: Cross-Platform Price Discrepancy

The edge is the gap between global Polymarket prices (smart money) and US
Polymarket prices (retail-heavy, thinner liquidity).

```python
def compute_edge(global_price: float, us_price: float) -> float:
    """
    Primary edge: global consensus vs US execution price.
    Positive = US is underpriced relative to global smart money.
    """
    return global_price - us_price

def compute_confirmed_edge(
    global_price: float,
    us_price: float,
    sportsbook_prob: float | None,  # Layer 2, may be None if no Odds API data
) -> tuple[float, float]:
    """
    Returns (edge, confidence).

    confidence levels:
    - 1.0: all three layers agree (global + sportsbooks vs US)
    - 0.7: global price alone disagrees with US (no sportsbook data)
    - 0.5: global and sportsbooks disagree with each other
    """
    edge = global_price - us_price

    if sportsbook_prob is None:
        # No sportsbook data — use global alone
        return edge, 0.7

    # Sportsbooks confirm global?
    books_agree = abs(global_price - sportsbook_prob) < 0.03  # within 3 cents
    if books_agree:
        return edge, 1.0  # high confidence — two independent sources agree
    else:
        # Global and sportsbooks disagree — lower confidence
        # Use the average as the consensus
        avg_consensus = (global_price + sportsbook_prob) / 2
        return avg_consensus - us_price, 0.5
```

**When to trade:**
- `edge >= 0.05` (5 cents) AND `confidence >= 0.7`
- OR `edge >= 0.03` (3 cents) AND `confidence == 1.0` (all layers agree)
- Order book depth on US market >= 3x position size
- Game > 2 hours away
- Not at max open positions

### 3B. Vig Removal (for Layer 2 sportsbook data)

```python
def devig_odds(home_implied: float, away_implied: float) -> tuple[float, float]:
    """Remove bookmaker vig. Raw implied probs sum to ~1.05, true probs sum to 1.0."""
    total = home_implied + away_implied
    return home_implied / total, away_implied / total
```

### 3C. Strategy File

**New: `src/polybot/strategies/sports.py`**

```python
class SportsStrategy:
    """Finds mispricings between global Polymarket and US Polymarket."""

    async def evaluate(
        matched_pair: MatchedPair,       # global + US prices for same game
        odds_data: GameOdds | None,      # Layer 2 sportsbook data (optional)
        injuries: list[InjuryReport],
    ) -> Optional[Opportunity]:
        # 1. Compute primary edge: global price vs US price
        # 2. If Odds API data available, compute confirmed edge
        # 3. Apply signal adjustments (injuries, B2B, line movement)
        # 4. If adjusted_edge >= threshold at sufficient confidence → Opportunity
        # 5. Choose YES or NO side based on which is underpriced on US
        # 6. Return Opportunity with market_slug (US), entry_price (US), etc.
```

Returns `Opportunity` objects — same interface as `weather.py`.

### 3D. Signal Strength Adjustments

| Signal | Effect | Source |
|--------|--------|--------|
| **Layer 2 confirms Layer 1** | Boost confidence to 1.0 | The Odds API |
| **Global volume is high** | Higher trust in global price | Gamma API |
| **US book is thin** | Wider edge but more slippage risk | US SDK |
| **Injury news** | Adjust probability if not yet priced in | ESPN |
| **Back-to-back games** | NBA B2B teams underperform | Schedule data |
| **Line movement** | Global price trending our direction = confirmation | Gamma over time |

### 3E. Exit Strategy Tuning

| Trigger | Sports Setting |
|---------|----------------|
| `profit_target` | entry * 1.5 |
| `edge_collapsed` | 4 cents against entry |
| `time_stop` | 30 min before game start |
| `market_closed` | price >= 0.95 |

**New trigger:** `pregame_lock` — exit 5 min before game starts.

---

## Phase 4 — LangGraph Pipeline (~2 days)

### Separate Graph (does NOT branch the weather graph)

**New: `src/polybot/scanner/sports_graph.py`**

```
fetch_global_sports → fetch_us_events → match_markets → fetch_odds → run_strategy → monitor
       │                    │                │              │              │            │
  Gamma API           US SDK          match by team    Odds API      sports.py     US SDK
  (READ ONLY)      (READ + EXEC)      name fuzzy     (optional)                  (prices)
  no auth needed    Ed25519 auth       matching       Layer 2 confirm
  Layer 1 signal   Layer 3 target
```

**New: `src/polybot/scanner/sports_state.py`**

```python
class SportsScanState(TypedDict):
    # Layer 1: Global consensus prices
    global_sports: list[dict]        # from Gamma API (gamma.py)

    # Layer 3: US execution targets
    us_events: list[dict]            # from Polymarket US SDK

    # Matched pairs (global ↔ US for same game)
    matched_pairs: list[MatchedPair]

    # Layer 2: Sportsbook confirmation (optional)
    odds_data: list[GameOdds]        # from The Odds API

    # Support data
    injuries: list[InjuryReport]     # from ESPN

    # Strategy output
    opportunities: list[Opportunity]
    open_positions: list[Trade]      # injected before each scan
```

Runs as its own `asyncio` task alongside the weather graph.
Sports scans every ~30s (faster near game time). Weather stays at ~2min.

---

## Phase 5 — Trader Routing (~1 day)

**Modify `src/polybot/paper/trader.py`:**

```python
class Trader:
    def __init__(self, ..., us_client: PolymarketUSClient | None = None):
        self._us_client = us_client

    def open_position(self, opp: Opportunity):
        trade = self._record_paper_trade(opp)

        if self.live_mode and opp.category == "sports":
            if self._us_client is None:
                logger.warning("No US client — paper only")
                return trade
            order = self._us_client.place_order(
                market_slug=opp.market_slug,
                side=opp.side,
                price=opp.entry_price,
                quantity=opp.quantity,
            )
            if order:
                trade.live_order_id = order.get("id")
                trade.live_platform = "polymarket_us"

        elif self.live_mode and opp.category == "weather":
            logger.info("Weather — paper only (no US market yet)")

        return trade
```

**The `live_platform` field** makes it unambiguous which API placed each order.

---

## Phase 6 — Dashboard + Telegram (~1 day)

**Dashboard:** Add SPT panel. Condense: `"LAL vs BOS · NBA · Mar 29"`
**Telegram:**
```
[LIVE] 🏀 Opened: LAL vs BOS — YES @ $0.58
  Consensus: 65.2% | Edge: +7.2¢ | $5.00
  Game: Mar 29 7:30 PM PT | Platform: Polymarket US
```

---

## Phase 7 — Paper Test → Live Ramp (~3-5 days)

50+ paper trades, then:

| Week | Cap | Size | Gate |
|------|-----|------|------|
| 1 | $20/day | $1-2 | >55% paper WR |
| 2 | $50/day | $3-5 | Positive live P&L |
| 3 | $100/day | $5-10 | No breaker hits |
| 4+ | $200/day | Kelly | 2 profitable weeks |

---

## File Map

### New Files (sports bot — US API for execution, Gamma for signals)
| File | Imports |
|------|---------|
| `src/polybot/api/polymarket_us.py` | `polymarket_us` SDK |
| `src/polybot/api/odds.py` | `httpx` |
| `src/polybot/api/espn.py` | `httpx` |
| `src/polybot/strategies/sports.py` | internal only |
| `src/polybot/scanner/sports_graph.py` | `polymarket_us.py`, `gamma.py`, `odds.py` |
| `src/polybot/scanner/sports_state.py` | internal only |
| `scripts/verify_us_api.py` | `polymarket_us` SDK |

### Existing Files (weather bot — Global API only, UNCHANGED)
| File | Status | Uses |
|------|--------|------|
| `src/polybot/api/clob_client.py` | **UNCHANGED** | `py-clob-client` |
| `src/polybot/api/openmeteo.py` | **UNCHANGED** | Open-Meteo |
| `src/polybot/strategies/weather.py` | **UNCHANGED** | internal |
| `src/polybot/scanner/graph.py` | **UNCHANGED** | `gamma.py`, `clob_client.py` |

### Shared Files (both bots use)
| File | Change |
|------|--------|
| `src/polybot/api/gamma.py` | **SHARED READ-ONLY** — weather bot reads weather markets, sports bot reads sports markets. Same client, different keyword filters. No orders ever placed through Gamma. |
| `src/polybot/config.py` | Add US API + Odds API fields |
| `src/polybot/paper/trader.py` | Add `us_client`, route by category |
| `src/polybot/strategies/exit.py` | Add `pregame_lock` trigger |
| `src/polybot/cli.py` | Run sports scanner as separate task |
| `src/polybot/web/server.py` | Add SPT panel |
| `src/polybot/telegram/bot.py` | Sport-specific alerts |
| `.env` / `.env.example` | New US API + Odds API fields |

### Import Firewall

```
src/polybot/api/
├── clob_client.py      ← py_clob_client    (GLOBAL ORDERS — weather paper only)
├── gamma.py            ← httpx              (GLOBAL READS — shared by both bots)
├── openmeteo.py        ← httpx              (weather data)
├── polymarket_us.py    ← polymarket_us      (US ORDERS — sports live execution)
├── odds.py             ← httpx              (sportsbook data, Layer 2)
└── espn.py             ← httpx              (sports schedule/injuries)

RULES:
  1. clob_client.py and polymarket_us.py NEVER import each other.
  2. No file places orders through BOTH py-clob-client AND polymarket-us.
  3. gamma.py is READ-ONLY data. Both bots can import it for price reads.
     It never places orders. It never imports py-clob-client or polymarket-us.
  4. The sports scanner imports gamma.py (Layer 1 reads) AND
     polymarket_us.py (Layer 3 execution). This is safe because
     gamma.py is purely a data source, not an order client.
```

---

## Fund Migration

Your USDC.e in the global proxy wallet → US account:

1. **Withdraw from global** — website UI or programmatic via contracts
2. **Deposit into US** — app → Deposit → Transfer Crypto → copy address
3. **Send USDC** from your exchange/wallet to that address on Polygon
4. **Test first** — send $5, verify it arrives, then send the rest
5. **Wrong network = lost funds** — always confirm Polygon

---

## US SDK vs Global SDK — Key Differences

| Feature | Global (`py-clob-client`) | US (`polymarket-us`) |
|---------|--------------------------|----------------------|
| Market ID | token_id (long numeric) | slug ("lakers-celtics") |
| Order side | `"BUY"` / `"SELL"` | `ORDER_INTENT_BUY_LONG/SHORT` |
| Price | float (0.55) | `{"value": "0.55", "currency": "USD"}` |
| Create order | `create_and_post_order()` | `orders.create({...})` |
| TIF | GTC implicit | Explicit constant required |
| Errors | **Silent None** | **Typed exceptions** |
| Async | Not native | `AsyncPolymarketUS` built-in |
| WebSocket | Separate setup | `client.ws.markets()` / `.private()` |

**Biggest win:** Real error messages instead of silent failures.

---

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| CA gets restricted | Monitor state AG; Kalshi as backup |
| Global and US prices converge (no edge) | Monitor spread over time; if consistently < 3¢, pivot to sportsbook arb |
| Odds API rate limit (500/mo) | Now Layer 2 only (confirmation) — 500/mo is plenty for spot-checks |
| Sports edges smaller than weather | Higher volume (more games/day); three-layer confirmation = higher win rate |
| US SDK breaking changes | Pin version; subscribe to changelog |
| Game postponed | Check resolution rules before trading |
| Gamma API changes or gets restricted | Odds API becomes primary signal; system still works without Layer 1 |
| Confused API routing | Import firewall; `live_platform` field on trades; gamma.py is read-only |

---

## FIFA World Cup 2026

Starts **June 11** in US/Mexico/Canada. Billions in volume expected.
Build soccer support early. Have bot battle-tested by early June.

---

## Checklist (When You Come Back)

```
□ Signed up with invite code, completed KYC
□ "Approved to Start Trading" confirmed in app
□ Generated API keys at polymarket.us/developer
□ POLYMARKET_KEY_ID and POLYMARKET_SECRET_KEY saved to .env
□ Funded US account ($50-100)
□ Run: PYTHONPATH=src python scripts/verify_us_api.py → all green

Then build:
  Phase 1 → polymarket_us.py wrapper (US SDK)
  Phase 2 → gamma.py sports filters + odds.py + espn.py pipeline
  Phase 3 → sports.py strategy (3-layer edge model)
  Phase 4 → sports_graph.py LangGraph pipeline
  Phase 5 → trader.py routing
  Phase 6 → dashboard + telegram
  Phase 7 → paper test → live ramp
```

---

*Created: March 28, 2026*
*Based on: https://docs.polymarket.us/getting-started/quickstart*
*SDK ref: https://docs.polymarket.us/api-reference/sdks/python/quickstart*
*SDK source: https://github.com/Polymarket/polymarket-us-python*