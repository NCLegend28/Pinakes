# CI/CD Setup — Tali Portfolio (cPanel + GitHub)

## Architecture

```
[Local] git push → [GitHub] → GitHub Actions (CI: install + build check)
                             ↓ webhook
                         [cPanel Git Version Control]
                             ↓ pulls repo, runs .cpanel.yml
                         [cPanel Node.js App]
                           npm ci + npm run build → restart server.cjs
```

---

## Step 1 — Initialize git locally

```bash
git init
git add .
git commit -m "feat: initial commit"
git branch -M main
```

## Step 2 — Create GitHub repo and push

```bash
git remote add origin <github-repo-url>
git push -u origin main
```

## Step 3 — cPanel: Set up Node.js App

1. cPanel → **Node.js Apps** → **Create Application**
2. Node.js version: **20.x**
3. Application root: `tali-portfolio/` (wherever the repo will be cloned)
4. Application startup file: `server.cjs`
5. Add environment variables:
   - `MOONSHOT_API_KEY` — your API key
   - `PORT` — if needed (Passenger usually manages this)

## Step 4 — cPanel: Git Version Control

1. cPanel → **Git Version Control** → **Create**
2. Clone URL: your GitHub repo URL (use HTTPS)
3. Repository path: `/home/<user>/tali-portfolio`
4. Enable **"Deploy HEAD Commit"** / auto-deploy on push via webhook

## Step 5 — GitHub: Add deploy webhook

In GitHub repo → **Settings** → **Webhooks** → **Add webhook**

- Payload URL: provided by cPanel's Git Version Control panel
- Content type: `application/json`
- Event: `push`

## Step 6 — Set `VITE_API_URL` for production

`.env.production` is gitignored, so set it one of two ways:
- In cPanel's Node.js App environment variables UI, **or**
- Create it manually on the server after first deploy:
  ```bash
  echo "VITE_API_URL=https://your-domain.com" > /home/<user>/tali-portfolio/.env.production
  ```

---

## How deploys work after setup

1. You push to `main`
2. GitHub Actions runs `npm ci` + `npm run build` — if it fails, cPanel is never triggered
3. GitHub sends a webhook to cPanel
4. cPanel pulls the latest commit and runs `.cpanel.yml` (install + build)
5. Passenger (cPanel's process manager) restarts `server.cjs` automatically

---

## Verification

```bash
# 1. Push a small change to main
git commit --allow-empty -m "chore: trigger deploy"
git push

# 2. Check GitHub Actions CI passes (green checkmark in repo Actions tab)

# 3. Check cPanel Git Version Control confirms pull was triggered

# 4. Test the API
curl http://your-domain.com/api/chat \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"hello"}]}'

# 5. Visit the live site and test the chatbot
```

---

## Key Constraints

| Item | Status |
|------|--------|
| `package-lock.json` | **Committed** — required by `npm ci` |
| `.env` / `.env.production` | Gitignored — secrets live in cPanel env vars |
| `dist/` | Gitignored — built server-side by `.cpanel.yml` |
| GitHub Actions | CI only (no deploy) — validates build before cPanel pulls |
| Process management | Passenger (cPanel) handles restarts |
