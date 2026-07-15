# Chatbot Status & Architecture

Last updated: 2026-02-22

---

## Architecture Overview

The chatbot is a full-stack feature with a React frontend and an Express backend that proxies requests to the Moonshot (Kimi K2) LLM.

```
Browser (ChatBot.jsx)
  └─ POST /api/chat  { messages: [...] }
       └─ Express server (server.cjs, port 3000)
            └─ Prepends system prompt (systemPrompt.cjs)
            └─ POST https://api.moonshot.ai/v1/chat/completions
                 └─ Model: kimi-k2-0905-preview
            └─ Returns { reply: "..." } to the browser
```

### Key Files

| File | Purpose |
|---|---|
| `server.cjs` | Express backend, rate limiter, Moonshot API proxy |
| `systemPrompt.cjs` | Tali's persona and knowledge — injected server-side on every request |
| `src/components/ChatBot.jsx` | React UI — renders messages, calls `/api/chat`, handles errors |
| `.env` | Contains `MOONSHOT_API_KEY` — never committed, never exposed to the client |

### How the Conversation Flow Works

1. The user types a message. ChatBot.jsx appends it to local state and sends the full conversation history (last 20 messages, user/assistant only) to `POST /api/chat`.
2. The server prepends the system prompt (Tali's persona) to the messages array — the client never sees the system prompt.
3. The server enforces a second 20-message sliding window on the server side.
4. The Moonshot API returns a completion; the server extracts `choices[0].message.content` and sends `{ reply }` back to the browser.
5. ChatBot.jsx appends the assistant reply to local state and re-renders.

### Rate Limiting

- 20 requests per IP per 15-minute window, applied only to `/api/chat`.
- Returns HTTP 429 with a user-friendly message when exceeded.

---

## Success Criteria Validation (2026-02-22)

### 1. Responds accurately to questions about Tali

Test: `"What projects have you built?"`

Result: The model returned a detailed, conversational description of Financio, Apollo Gloves, AI Receptionist, Electromagnetic Wristband, and AI Inventory Management — all accurate per the system prompt.

Status: PASS

### 2. Responds naturally to off-topic / random messages

Test: `"my butt itches"`

Result: The model responded with humor and warmth ("*laughs* Man, that's the realest thing anyone's said to me all week..."), with no scripted redirect to the contact email.

Status: PASS

### 3. No frontend errors

The Vite build completed without errors or warnings:
- `dist/index.html` — 0.65 kB
- `dist/assets/index-DH62e29x.css` — 31.84 kB
- `dist/assets/index-D5ejQLN5.js` — 224.07 kB
- Built in 1.53s

Status: PASS

### 4. Server running and stable

Server running on port 3000, process confirmed via `lsof -i :3000`. Logs show clean startup. No errors after the model name fix.

Status: PASS

---

## Fixes Applied This Session

### Fix: Incorrect Moonshot model name

- **Problem**: `server.cjs` was using `model: 'kimi-k2'`, which does not exist on the Moonshot API. Every chat request returned a 404 error (`"Not found the model kimi-k2 or Permission denied"`).
- **Root cause**: The model was renamed/versioned; the correct ID is `kimi-k2-0905-preview`.
- **Fix**: Updated line 50 in `server.cjs` from `'kimi-k2'` to `'kimi-k2-0905-preview'`.
- **Verified by**: Querying `GET https://api.moonshot.ai/v1/models` with the API key — `kimi-k2-0905-preview` was the first result returned.
- **File changed**: `/Users/mosley/projects/website/tali-portfolio/server.cjs`

---

## How to Restart the Server

```bash
# From the project root
cd /Users/mosley/projects/website/tali-portfolio

# Kill any existing process on port 3000
kill $(lsof -ti :3000) 2>/dev/null

# Start server in background, append logs
node server.cjs >> server.log 2>&1 &

# Verify it's running
lsof -i :3000
```

To check live logs:

```bash
tail -f /Users/mosley/projects/website/tali-portfolio/server.log
```

---

## How to Update the System Prompt

1. Edit `/Users/mosley/projects/website/tali-portfolio/systemPrompt.cjs`.
2. The file exports a single template-literal string via `module.exports`. Edit the string directly.
3. Restart the server (see above) — no frontend rebuild is needed because the system prompt is server-side only.

Example: to add a new project, append it under `KEY PROJECTS:` in the template literal.

---

## How to Rebuild the Frontend

```bash
cd /Users/mosley/projects/website/tali-portfolio
npm run build
```

The compiled assets land in `dist/`. The Express server serves `dist/` as static files for the production site.

---

## Available Moonshot Models (as of 2026-02-22)

Confirmed via `GET https://api.moonshot.ai/v1/models`:

- `kimi-k2-0905-preview` — 262,144 context (currently in use)
- `moonshot-v1-8k-vision-preview` — 8,192 context, supports image input
- `moonshot-v1-32k-vision-preview` — 32,768 context, supports image input
- (additional models truncated)

To switch models, update the `model` field in the `client.chat.completions.create()` call in `server.cjs` (line 50), then restart the server.
