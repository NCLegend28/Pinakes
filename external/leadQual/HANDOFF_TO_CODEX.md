# 🤝 Handoff to OpenAI Codex

**From:** Claude Code
**To:** OpenAI Codex
**Date:** 2025-10-21
**Status:** Authentication Complete, Dashboard Settings + Integrations Phase

---

## ✅ Completed to Date

### Dashboard Core (Week 2 Phase 1)
- Layout shell (`app/dashboard/layout.tsx`)
- Overview analytics (`app/dashboard/page.tsx`)
- Conversations list + detail views (`app/dashboard/conversations/*`)
- Reusable navigation + filters components
- Demo seeding script (`npm run seed:demo`)
- Lint/type cleanup across workflow utilities

---

## 🚧 Current Focus (Week 2 Phase 2)

### 1. Settings Overview Page (`app/dashboard/settings/page.tsx`)
Create a multi-section settings page with cards:
- **Tenant Profile:** Name, industry, timezone (read-only for now)
- **Branding:** Primary color, logo upload placeholder (show current hex + upload CTA)
- **Business Hours:** Display configured hours or placeholder CTA
- **Support Contact:** Email/phone used in chat footer

Use data from `Tenant` row via `getTenantBySlug` (or session user fields). For now, display values with “Edit” buttons (modal placeholders) so UI is ready for future forms.

### 2. AI Configuration Editor (`app/dashboard/settings/ai/page.tsx`)
Allow admins to view and update agent configs:
- Table/list of agents (guard, qualifier, clarifier, action)
- Fields: provider, model, temperature, max tokens, status toggle
- “Edit config” button opening a form on the right (server components ok)

Use `getTenantConfig` utilities; for now, edits can be mocked (no API) but structure the form to POST to `/api/dashboard/agents/[agentId]` later. Provide a `Save changes` button disabled with tooltip “Coming soon”.

### 3. Widget Setup Page (`app/dashboard/settings/widget/page.tsx`)
- Show embeddable script snippet using tenant slug
- Include quick instructions (copy embed, optional React component usage)
- Add preview panel with simple chat mockup

### 4. Integrations Hub (`app/dashboard/integrations/page.tsx`)
- Zapier “Manage” now opens the external integration console; Slack “Connect” links to an in-app setup guide. Coming-soon integrations remain disabled.

### 5. Billing Summary (`app/dashboard/billing/page.tsx`)
- “Change plan” routes to `/dashboard/billing/plans` for plan selection.
- Invoices download via `/api/dashboard/billing/invoices/[id]/[format]` supporting PDF and CSV formats.

### 6. Token/Cost Tracking
- ✅ Workflow pipeline now captures provider usage and pricing so `total_cost` reflects real spend.

---

## Navigation Updates

Add entries to sidebar/navigation:
- `/dashboard/settings`
- `/dashboard/settings/ai`
- `/dashboard/settings/widget`
- `/dashboard/integrations`
- `/dashboard/billing`

Ensure mobile dropdown includes new routes.

---

## Data Access Helpers

- Tenant info: `getTenantBySlug(user.tenantSlug)`
- Agent configs: `loadTenantConfig(tenantSlug)`
- Usage stats: `getConversationStats(tenantId, start, end)`

For now, read-only pages are acceptable; forms can log “coming soon”.

---

## Design Notes

- Stick with existing Tailwind aesthetic (cards with `border bg-white shadow-sm`)
- Use `text-slate` palette for neutral text
- Buttons: primary (`bg-blue-600 text-white`) and secondary (`border-slate-200`)
- Include breadcrumbs or page titles for clarity (e.g., “Settings → AI Configuration”)

---

## Testing & Validation

- Run `npm run lint` after updates
- Optionally use `npm run seed:demo` to refresh data and preview settings/integrations pages

---

## Outstanding Questions / Assumptions

- Editing forms will be wired once API endpoints exist; keep components modular so we can drop in actions later.
- Billing data is static for now—display placeholder invoices but structure markup for future integration.
- Token/cost tracking pending; display current `total_cost` but annotate with “prototype” badge or tooltip.

---

**Let’s ship the settings suite, then move to widget + billing polish before diving into workflow cost tracking.**
