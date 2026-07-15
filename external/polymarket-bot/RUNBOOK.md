# Polymarket Bot — VPS Runbook

End-to-end ops guide for running the bot 24/7 on an Exoscale VPS, managed
over Tailscale, with Claude Code on the box for in-place edits.

This runbook is opinionated: it picks one path and explains why, instead of
listing every alternative. Deviate only with cause.

---

## 0. Picking a zone

Polymarket geoblocks at the API layer based on the requesting IP. The zone
you provision in matters as much as the zone you live in.

| Zone     | Country     | Polymarket status            | Use it? |
|----------|-------------|------------------------------|---------|
| CH-DK-2  | Switzerland | Fully blocked (Nov 2024)     | No      |
| CH-GVA-2 | Switzerland | Fully blocked                | No      |
| DE-FRA-1 | Germany     | Trading prohibited (view only) | No    |
| DE-MUC-1 | Germany     | Trading prohibited           | No      |
| **AT-VIE-1** | **Austria** | **Clear**                    | **Yes** |
| **AT-VIE-2** | **Austria** | **Clear**                    | Yes (HA pair) |
| BG-SOF-1 | Bulgaria    | Not on any restricted list   | Probably (verify) |
| HR-ZAG-1 | Croatia     | Not on any restricted list   | Probably (verify) |

**Default pick: AT-VIE-1.** Austria is clean, Vienna has good peering to
Polymarket's primary EU region, and `at-vie-2` exists if you ever want a
warm standby in the same metro.

---

## 1. Provision the VPS (Exoscale)

In the Exoscale portal:

1. **Compute → Add Instance**
2. **Template:** Ubuntu 24.04 LTS
3. **Zone:** AT-VIE-1
4. **Instance type:** *Small* (2 vCPU / 4 GB RAM / 50 GB disk) — €0.0260/hr,
   roughly €19/mo. The bot is mostly idle; CPU spikes during a scan and
   the LangGraph pipeline. Tiny (1 GB) is too small once Docker + the bot
   + Claude Code share the box.
5. **SSH key:** add your laptop's public key. You'll mostly use Tailscale
   SSH after bootstrap, but this gets you in the first time.
6. **Security group:** create one named `polybot-sg` allowing only:
   - TCP 22 from **your home IP/32** (not 0.0.0.0/0) — break-glass only
   - All outbound traffic
   - No other inbound rules. The dashboard binds to 127.0.0.1 in
     docker-compose and is reached over Tailscale.
7. **Boot.** Note the public IPv4.

> Existing `scripts/exoscale-security-groups.sh` opens 8765/8766 to the
> world. **Don't run it as-is** — it predates the Tailscale model. Either
> delete it or rewrite it to mirror the rules above.

---

## 2. Bootstrap the box

SSH in once with the key you uploaded:

```bash
ssh ubuntu@<vps-ipv4>      # Exoscale's default user on the Ubuntu template
```

Pull the bootstrap script and run it. The script wants two optional secrets:

- A Tailscale auth key (one-time, expires in 90 days): generate at
  <https://login.tailscale.com/admin/settings/keys>
- Your laptop's SSH pubkey (so you have a break-glass path if Tailscale ever
  has an outage): copy from `~/.ssh/id_ed25519.pub` on your laptop

```bash
sudo curl -fsSL https://raw.githubusercontent.com/<you>/polymarket-bot/main/vps-setup.sh -o /root/vps-setup.sh
sudo TAILSCALE_AUTHKEY="tskey-auth-..." \
     SSH_PUBKEY="ssh-ed25519 AAAA... you@laptop" \
     bash /root/vps-setup.sh
```

The script is idempotent — re-run it any time you bump a dependency.

When it finishes you'll see the VPS's Tailscale IP and the SSH command to
use from your laptop:

```bash
tailscale ssh botuser@<hostname>-polybot
```

From this point on, you do **not** need the public IP. Lock the Exoscale
Security Group's port 22 rule down to your home IP only (or remove it
entirely if you're confident in the Exoscale web console as break-glass).

---

## 3. Deploy the bot

From your laptop:

```bash
tailscale ssh botuser@<hostname>-polybot
```

On the VPS, as `botuser`:

```bash
cd ~/polymarket-bot
git clone git@github.com:<you>/polymarket-bot.git .   # use a deploy key
cp .env.weather.example .env.weather
cp .env.dashboard.example .env.dashboard
nano .env.weather    # fill in TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, etc.
nano .env.dashboard
docker compose up -d --build
```

Verify:

```bash
docker compose ps                                      # both services healthy
docker compose logs -f weather-bot                     # scan loop heartbeat
curl -s http://localhost:8765/health                   # internal health
curl -s http://localhost:8766/health                   # dashboard health
```

> **Heads-up: `.env.example` currently has unresolved git merge conflict
> markers** (`<<<<<<< HEAD`, `=======`, `>>>>>>> feat/eml-node-research`).
> Resolve those in git before cloning, or the deploy will fail at config
> load. `.env.weather.example` and `.env.dashboard.example` look clean.

---

## 4. Access the dashboard from your laptop

The dashboard is bound to `127.0.0.1:8766` inside the VPS — not reachable
from the public internet, by design. To view it from your laptop, exploit
Tailscale's "the tailnet is the LAN" property:

**Option A — Tailscale Serve** (recommended, no port forwarding):

```bash
# On the VPS:
sudo tailscale serve --bg --https=443 --set-path / http://localhost:8766
# Then visit https://<hostname>-polybot.<tailnet>.ts.net on your laptop
```

**Option B — SSH port forward** (zero VPS config):

```bash
# On your laptop:
tailscale ssh -L 8766:localhost:8766 botuser@<hostname>-polybot
# Then open http://localhost:8766 on your laptop
```

Pick A for "always available," B for "one-off check."

---

## 5. Claude Code on the VPS

The point of putting Claude Code on the box is that the agent sees the live
state — running containers, real `.env`, actual trade log — instead of a
laptop-side guess.

```bash
# On the VPS, as botuser:
curl -fsSL https://claude.ai/install.sh | bash      # check current install path on docs.claude.com
exec $SHELL                                          # pick up new PATH
claude                                               # auth on first run
```

Dev loop from your laptop:

```bash
tailscale ssh botuser@<hostname>-polybot
cd ~/polymarket-bot
claude
```

Same UX as local Claude Code, but every Edit/Bash hits the production box.
Stage risky changes on a branch first:

```bash
git checkout -b experiment/<thing>
# ... claude makes changes ...
docker compose up -d --build     # rebuild affected services
# verify, then merge or revert
```

---

## 6. Backups

The only durable state is the trades volume. Cheapest reliable backup is a
nightly `restic` push to Backblaze B2 (~$0.005/GB/mo).

```bash
# One-time setup (on the VPS, as botuser):
sudo apt install -y restic
export B2_ACCOUNT_ID=<key-id>
export B2_ACCOUNT_KEY=<application-key>
export RESTIC_REPOSITORY="b2:polybot-backups:/"
export RESTIC_PASSWORD=<long-random-string-stored-in-1password>
restic init
```

Stick those env vars in `/etc/polybot-backup.env` (chmod 600, root-owned),
then add the cron:

```bash
sudo tee /etc/cron.daily/polybot-backup >/dev/null <<'CRON'
#!/bin/bash
set -a; source /etc/polybot-backup.env; set +a
restic backup /var/lib/docker/volumes/polymarket-bot_trades_data/_data \
              --tag trades --host polybot
restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 12 --prune
CRON
sudo chmod 755 /etc/cron.daily/polybot-backup
```

Test the restore path (the only backup that matters is the one you've
restored from):

```bash
restic snapshots
restic restore latest --target /tmp/restore-test
ls /tmp/restore-test/var/lib/docker/volumes/...
```

---

## 7. Ops cheatsheet

```bash
# Day-to-day, all run as botuser on the VPS:

docker compose ps                            # status
docker compose logs -f weather-bot           # tail scanner
docker compose logs --since 1h dashboard     # last hour of dashboard
docker compose restart weather-bot           # restart just the scanner
docker compose pull && docker compose up -d  # update + restart everything
docker compose down                          # stop everything (data persists)

# Disk:
df -h /                                      # root usage
docker system df                             # docker layer + volume usage
docker system prune -af --volumes            # nuke unused images/volumes
du -sh ~/polymarket-bot/data/trades/         # trade log size

# Tailscale:
tailscale status                             # who's on the tailnet
tailscale ip -4                              # this node's tailnet IP

# Updates:
sudo apt update && sudo apt upgrade -y
sudo reboot                                  # services come back via restart: unless-stopped
```

---

## 8. Troubleshooting

| Symptom                                  | First thing to check                         |
|------------------------------------------|----------------------------------------------|
| Bot exits immediately                    | `docker compose logs weather-bot` — likely .env |
| `403` from Polymarket API                | Wrong zone — verify with `curl ifconfig.me` then check geo |
| Healthcheck failing                      | `docker compose exec weather-bot wget -qO- localhost:8765/health` |
| Dashboard unreachable over Tailscale     | `sudo ufw status verbose` — tailscale0 must be allowed |
| `tailscale ssh` hangs                    | Check Tailscale ACLs allow SSH from your laptop |
| Disk full                                | `docker system prune -af` then check `/var/log` |
| Container restarting in a loop           | `docker compose logs --tail=200 <svc>` — usually config |
| Lost laptop SSH key                      | Use Exoscale web console (KVM) to add a new one |

---

## 9. Decommission

If you ever tear this down:

```bash
# On the VPS:
docker compose down -v                       # stops + drops volume
sudo tailscale down && sudo tailscale logout

# On your laptop:
tailscale admin → remove the node from the tailnet

# In Exoscale portal:
Compute → Instances → polybot → Destroy
Compute → Security Groups → polybot-sg → Delete
```

Backups in B2 are independent — keep or delete via the Backblaze console.

---

## Decision log

- **2026-06-02** — Switched zone from CH-GVA-2 (Geneva) to AT-VIE-1 (Vienna).
  Switzerland fully geoblocked by Polymarket since Nov 2024; Austria has no
  restrictions. Same provider, ~same latency, legal.
- **2026-06-02** — Adopted Tailscale SSH as primary access path; public
  port 22 firewalled off via UFW. Rationale: removes a public attack
  surface, replaces it with mTLS over WireGuard. Break-glass via Exoscale
  web console.
- **2026-06-02** — Picked Docker over the systemd-runs-python path
  (deleted `setup-systemd.sh`'s use case). Reasons: the Dockerfile already
  exists with non-root user + read-only FS + dropped caps; running both
  paths is two places to update on every change.
