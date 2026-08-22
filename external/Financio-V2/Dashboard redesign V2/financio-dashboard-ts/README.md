# Financio — Trading Dashboard (TypeScript)

A React + TypeScript + Vite port of the Financio dashboard prototype, structured so
a backend can be integrated by implementing **one interface**. Every screen reads
data through the `ApiClient` seam — no component fetches directly — so wiring a real
API touches exactly one file.

## Run

```bash
npm install
npm run dev        # http://localhost:5173
npm run typecheck  # tsc --noEmit
npm run build      # type-check + production build
```

The app ships with a **mock client** (`src/api/mock.ts`) that returns the reference
figures ($7,505.52 equity, −$404.40 realized P&L, 0% win rate, 550 NFLX trades,
1 / 3 bots live), so it runs with no backend.

## Integrating your backend

1. Open `src/api/client.ts`. It defines the `ApiClient` interface and includes a
   commented **`httpClient`** REST reference implementation.
2. Implement `ApiClient` against your service (fill in the fetch paths, or adapt
   `httpClient` to your endpoints/response shapes). Set `VITE_API_BASE` in a
   `.env` file if you use it.
3. Change the last lines of `client.ts`:
   ```ts
   // import { mockClient } from './mock';
   export const api: ApiClient = httpClient;
   ```
4. Done. All components and the `useDashboardData` hook go live unchanged. Make your
   API return the shapes in `src/types.ts` and the UI renders them.

### The contract (`ApiClient`)

| Method | Returns | Notes |
| --- | --- | --- |
| `getSummary(botId?)` | `PortfolioSummary` | KPI strip, risk, profile totals |
| `getPerformanceSeries(botId?)` | `PerformanceSeries` | Full history per metric; UI slices by timeframe |
| `getSectors()` | `Sector[]` | Right-rail bars |
| `getTicker()` | `Quote[]` | Masthead marquee |
| `getTrades(limit?)` | `Trade[]` | Recent activity + Trades tab |
| `getOrders(limit?)` | `Order[]` | Orders tab |
| `getBots()` | `Bot[]` | Bots tab |
| `toggleBot(botId)` | `Bot` | Pause / activate |
| `getRiskParams()` | `RiskParams` | Risk tab + dialog |
| `updateRiskParams(params)` | `RiskParams` | Persist dialog edits |
| `getUserProfile()` | `UserProfile` | Profile tab |

All methods are `async` (return `Promise`), so swapping mock → HTTP requires no
signature changes.

## Project structure

```
src/
  types.ts            Domain models — the API contract. Match your backend to these.
  api/
    client.ts         ApiClient interface + REST reference (httpClient) + active `api` export
    mock.ts           Mock implementation (reference figures). Delete once live.
  lib/
    format.ts         money / signed / percent / date formatting (pure)
    series.ts         Timeframe slicing + deterministic mock-series generation
  hooks.ts            useDashboardData() — loads everything through `api` on mount
  theme.ts            Ink / red / muted palette constants for SVG + computed styles
  ui.ts               Shared inline-style helpers (grid cells, BUY/SELL labels)
  components/
    Masthead.tsx      Header: equity, filters, ticker
    Ticker.tsx        Infinite quote marquee
    TabNav.tsx        Overview / Bots / Trades / Orders / Risk / Profile
    Chart.tsx         Hand-built SVG area+line chart
    Overview.tsx      KPI strip, performance panel, sector rail, recent activity
    Bots.tsx          Bot roster with pause/activate
    TradesView.tsx    Full fills table
    OrdersView.tsx    Bot-submitted orders
    RiskView.tsx      Exposure, drawdown, active parameters
    RiskDialog.tsx    Modal parameter editor (drafts locally, commits on save)
    ProfileView.tsx   Trader profile + lifetime stats
  App.tsx             Composition + tab/timeframe/dialog state
  styles.css          Modernist design-system tokens & components (unmodified)
  app.css             App resets (ticker keyframe, select styling)
```

## Design system

Visuals follow the **Modernist** system — flat, architectural, Archivo throughout,
near-mono red-on-light, 2px rules, zero radius. `src/styles.css` is the design
system's stylesheet verbatim; all colors/spacing come from its `--color-*` /
`--font-*` tokens. Semantic meaning is carried by typography and direction
(▴/▾, +/−, ink for gains, red for losses) rather than traffic-light colors.

## Notes for integration

- **Money is never fabricated in the UI.** The backend supplies `gross`, `fee`,
  `pnl`; the UI only formats. Keep it that way to avoid rounding drift.
- **Timeframe filtering is client-side** over the full series returned by
  `getPerformanceSeries`. If your history is large, add a `timeframe` argument to
  that method and slice server-side instead (`src/lib/series.ts` has `DAYS`).
- **`botId` filter** is plumbed through the masthead but not yet applied to the
  requests — pass `botFilter` into the `api.getSummary(botId)` /
  `getPerformanceSeries(botId)` calls in `src/hooks.ts` when your API supports it.
- **Optimistic updates**: `toggleBot` and `updateRiskParams` patch local state from
  the returned entity; adjust if your API is fire-and-forget.
- **Avatar**: `UserProfile.avatarUrl` renders when present (grayscaled to match the
  system); otherwise a placeholder shows.
- Timestamps are pass-through strings in the mock (`formatTime` in `lib/format.ts`);
  switch to `Date` formatting there when the backend sends ISO 8601.
