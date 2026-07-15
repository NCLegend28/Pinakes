# Connecting Gmail to Delphi

Delphi reads and sends Gmail through IMAP+SMTP, the same way every native
mail client (Apple Mail, Thunderbird) does. There are two ways to authorize:

1. **App password (v1 — what's supported today).** Works in five minutes,
   requires Google 2-step verification.
2. **OAuth2 / "Sign in with Google" (deferred).** Would skip the app
   password but requires a Google Cloud project and an OAuth consent
   screen. Tracked as a follow-up.

This doc covers the app-password path.

---

## Prerequisites

- A Google account with **2-Step Verification enabled.** Google won't
  generate app passwords for accounts that don't have 2SV on. Turn it on at
  <https://myaccount.google.com/security>.

## Step 1 — Generate a Gmail app password

1. Visit <https://myaccount.google.com/apppasswords>. (If the page says
   "The setting you are looking for is not available for your account,"
   2SV is not on — see prerequisites.)
2. Under "App name," type `Delphi`.
3. Click **Create.** Google returns a 16-character password formatted in
   four groups of four (e.g. `abcd efgh ijkl mnop`). **Copy it now** —
   Google won't show it again.

The spaces in the displayed password are decorative; Delphi accepts the
password with or without them.

## Step 2 — Add the account in Delphi

1. Open Delphi → **Settings → Email → Accounts → Add Account.**
2. **Provider:** pick **Gmail.** This auto-fills:
   - IMAP host: `imap.gmail.com`, port `993`
   - SMTP host: `smtp.gmail.com`, port `465`, SSL
3. **Email:** your Gmail address (e.g. `you@gmail.com`).
4. **IMAP / SMTP username:** the same Gmail address.
5. **IMAP / SMTP password:** the 16-character app password from Step 1.
6. **Save.** Delphi will probe the connection and surface a clear error if
   anything is off — wrong password, 2SV not enabled on the account,
   "less secure app access" still enabled (it shouldn't be; Google
   removed that toggle in 2022).

## What "AI triage" does once it's connected

Once the account is healthy, the Email tab gets:

- Auto-summary per thread (Delphi router decides which model)
- Urgency scoring + push notification for high-urgency mail
- Auto-tag based on sender, subject, content
- Draft replies in the Drafts folder you can edit before sending
- Auto-spam scoring with quarantine

Every triage LLM call flows through Delphi's pipeline, so the soul,
classifier, and vault writes apply the same as chat does. The triage
output is written to `Vault of Knowledge/conversations/...` alongside
regular chat exchanges — every email Delphi reviews becomes part of the
graph.

## Troubleshooting

- **"Invalid credentials" / "Authentication failed."** The most common
  cause is using your Google account password instead of the app
  password. Re-paste the 16-character string from Step 1.
- **"Connection refused" on port 993.** A firewall or VPN is blocking
  the connection. On Tailscale, confirm Delphi's host can reach
  `imap.gmail.com:993` directly (e.g. `nc -zv imap.gmail.com 993`).
- **"Less secure app access" warnings.** Should not occur — that toggle
  was deprecated in 2022 and app passwords replaced it. If you see this
  error, the account isn't actually using an app password; revisit
  Step 2.
- **App passwords option is missing from your Google account.** 2SV
  isn't enabled. Turn it on first.

## When OAuth lands

Future Delphi will add a one-click **"Sign in with Google"** button next
to the Provider dropdown. The IMAP+SMTP path documented here will still
work — OAuth is additive, not a replacement. The decision log entry on
the day OAuth ships will name the exact migration path.

## Related

- [`docs/plans/2026-06-07-delphi-becomes-the-architecture.md`](../../../Delphi/docs/plans/2026-06-07-delphi-becomes-the-architecture.md)
  — Phase 4 / Task #17 of the chassis merge, which is what this doc
  unblocks.
