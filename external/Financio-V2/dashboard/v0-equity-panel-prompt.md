# v0 Prompt — Cyberpunk Equity Curve Panel (Financio)

Paste everything in the code block below into v0.dev. Iterate there, then export
("Code" button) or send the share link back here for porting into Financio.

---

Build a single self-contained React + TypeScript dashboard panel component styled in a
**cyberpunk / cyberdeck** aesthetic. Use Tailwind CSS, shadcn/ui primitives (Card, Button),
and **Recharts** for the chart. Include mock data inline.

## Component
A "Performance" panel card containing a row of 4 tab buttons and a chart below:
- Tabs: **Equity**, **Realized P&L**, **Gross Proceeds**, **Fees**
- Equity tab → Recharts `AreaChart` with a glowing neon stroke and gradient fill
- Realized P&L → `LineChart`; Gross Proceeds & Fees → `BarChart`
- Header reads "PERFORMANCE" in an uppercase display font with a small live "● ONLINE" status dot

## Data shape (use exactly this — it matches our app)
```ts
interface MetricPoint {
  timestamp: string;     // ISO date
  equity: number;
  grossProceeds: number;
  fees: number;
  realizedPnl: number;
}
```
Generate ~40 points of realistic mock MetricPoint data (an upward-trending equity curve
with volatility, starting ~100000).

## Cyberpunk theme — be disciplined, not neon-everything
- Background: near-black `#0a0e14`. Panel surface slightly lifted `#0d1117` with a thin
  1px neon-cyan border at ~30% opacity and a faint outer glow.
- Primary accent (equity line, active tab, glow): neon cyan `#00f0ff`.
- Secondary accents: hot magenta `#ff003c` (fees/loss), neon green `#00ff9f` (gains),
  amber `#f59e0b` (realized P&L line).
- Sharp corners (border-radius 2-4px max), NOT rounded-xl.
- Fonts: **Orbitron** or **Chakra Petch** for the header/labels (uppercase, letter-spaced);
  **JetBrains Mono** for all numbers and axis ticks. Use tabular figures.
- Subtle CRT scanline overlay across the panel (repeating-linear-gradient, very low opacity).
- Active tab: filled cyan with glow; inactive: dark with thin cyan-tinted border, hover brightens.
- Chart: dark grid lines (`#1a2332`), cyan glowing area stroke with `drop-shadow` filter,
  gradient fill fading to transparent. Tooltip: dark `#0a0e14` card, cyan border + glow,
  mono font, values formatted as USD currency.
- Add a faint animated pulse/flicker on the status dot and a soft glow animation on the
  active chart line. Keep motion subtle.

## Constraints
- One file, default export, no required props (mock data inside).
- No localStorage/sessionStorage.
- Keep it production-portable: plain Tailwind utility classes + shadcn, no exotic deps
  beyond recharts and lucide-react.

Make it feel like a HUD from a trading terminal in 2099 — restrained, high-contrast,
data-forward. Neon reserved for live data and focus states.
