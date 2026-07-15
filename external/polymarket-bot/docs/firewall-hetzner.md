# VPS Setup & Firewall — Hetzner

This guide covers everything from a fresh Hetzner server to a running polymarket-bot deployment.

**Port map for this project:**

| Port | Service | Exposure |
|------|---------|----------|
| 22 | SSH | Your laptop's public IP only |
| 8765 | weather-bot WebSocket | Internal Docker only — never public |
| 8766 | dashboard browser UI | Localhost only — access via SSH tunnel |

---

## Part 1 — Find your laptop's public IP

Your SSH allowlist needs your **public** IP — the one the internet sees, not your local `192.168.x.x` address.

```bash
# Run this on your laptop
curl ifconfig.me
```

> **Dynamic IP warning:** residential internet changes your IP when your router reboots. If that happens you'll be locked out of SSH. Two options:
> - Use Hetzner's browser-based console (Cloud Console → Server → Console) as a recovery path — it bypasses SSH entirely.
> - Or allow your ISP's full IP range (e.g. `/24`) instead of a single `/32` — less strict but survivable.

---

## Part 2 — Create the Hetzner server

1. **Cloud Console → Servers → Create Server**
2. Choose a location (Nuremberg/Falkenstein for EU, Ashburn for US)
3. Image: **Ubuntu 24.04**
4. Type: **CX22** (2 vCPU, 4 GB RAM) — sufficient for the weather bot
5. SSH keys: paste your public key (`cat ~/.ssh/id_ed25519.pub`)
6. Name it something recognisable (e.g. `polybot-prod`)
7. **Do not attach a firewall yet** — do that after the server is up

Note the server's public IP.

---

## Part 3 — Firewall setup

### Layer 1 — Hetzner Cloud Firewall (network level, primary)

This is the outer gate. Traffic that doesn't match a rule is silently dropped at Hetzner's network edge — the server never sees it, Docker never sees it.

**Cloud Console → Security → Firewalls → Create Firewall**

Name: `polymarket-bot`

**Inbound rules:**

| Protocol | Port | Source | Purpose |
|----------|------|--------|---------|
| TCP | 22 | `your.public.ip/32` | SSH — your laptop only |

Leave everything else at the default (blocked). Ports 8765 and 8766 are never exposed publicly — the dashboard is accessed via SSH tunnel only (see Part 4.8).

**Outbound rules** — allow all (scanner needs to reach Polymarket, OpenMeteo, ESPN, etc.):

| Protocol | Port | Destination |
|----------|------|-------------|
| TCP | Any | `0.0.0.0/0, ::/0` |
| UDP | Any | `0.0.0.0/0, ::/0` |

**Attach the firewall:**
Firewall page → Apply to Resources → Add Server → select `polybot-prod`.

---

### Layer 2 — UFW on the server (OS level, backstop)

UFW is a second independent layer. SSH into the server first, then run:

```bash
# Install if not present
sudo apt install ufw -y

# Defaults
sudo ufw default deny incoming
sudo ufw default allow outgoing

# SSH — do this BEFORE enabling, or you lock yourself out
sudo ufw allow from YOUR.PUBLIC.IP to any port 22 proto tcp

# Enable
sudo ufw enable    # type 'y' to confirm
sudo ufw status verbose
```

Expected output:
```
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW IN    YOUR.PUBLIC.IP
```

Ports 8765 and 8766 should **not** appear — both are bound to `127.0.0.1` in `docker-compose.yml` and never reach the public network.

**The Docker/UFW conflict:** Docker writes its own iptables rules for `ports:` bindings that bypass UFW. For this project it is not an issue because port 8765 uses `expose:` (internal Docker network only, never bound to the host). The Hetzner Cloud Firewall blocks it at the network edge regardless.

---

## Part 4 — Server setup

### 4.1 Create a non-root user

```bash
# Still as root (first login)
adduser botuser
usermod -aG sudo botuser
usermod -aG docker botuser   # add after Docker is installed (step 4.2)

# Copy your SSH key to the new user
rsync --archive --chown=botuser:botuser ~/.ssh /home/botuser
```

Log out and log back in as `botuser` for everything from here.

### 4.2 Install Docker

```bash
sudo apt update && sudo apt upgrade -y

# Install Docker via the official script
curl -fsSL https://get.docker.com | sudo sh

# Add botuser to the docker group (then re-login for it to take effect)
sudo usermod -aG docker botuser
newgrp docker   # or log out/in

# Verify
docker version
docker compose version
```

### 4.3 Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.local/bin/env   # or open a new shell
uv --version
```

### 4.4 Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/polymarket-bot.git
cd polymarket-bot
```

### 4.5 Set up environment files

```bash
cp .env.weather.example .env.weather
cp .env.dashboard.example .env.dashboard
```

Edit `.env.weather` with your real values:

```bash
nano .env.weather
```

Minimum required fields:
```
HEADLESS=true
WEB_ENABLED=true
WEB_PORT=8765

# Only needed for live trading — leave blank to paper-trade
WALLET_PRIVATE_KEY=
WALLET_ADDRESS=

# Optional Telegram alerts
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

`.env.dashboard` needs only one change from the example — the scanner URL is already correct for Docker Compose:
```
SCANNER_WS_URL=ws://weather-bot:8765/ws
DASHBOARD_PORT=8766
```

### 4.6 Build and start

```bash
# Build both images (takes ~2 min first time)
docker compose build

# Start in the background
docker compose up -d

# Watch logs
docker compose logs -f
```

### 4.7 Verify everything is running

```bash
# Both services should show 'healthy' after ~30s
docker compose ps

# Check scanner is up (from inside the Docker network)
docker compose exec dashboard python -c "import urllib.request; print(urllib.request.urlopen('http://weather-bot:8765/health').read().decode())"

# Check dashboard is up (from the server)
python3 -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8766/health').read().decode())"
```

From your laptop (both should hang or be refused — that's correct):
```bash
curl -v http://YOUR_VPS_IP:8765/health   # filtered — expected
curl -v http://YOUR_VPS_IP:8766/health   # filtered — expected
```

Access the dashboard via SSH tunnel (see Part 4.8).

### 4.8 Access the dashboard via SSH tunnel

The dashboard is bound to `127.0.0.1` on the server — it is never reachable directly from the internet. Open an SSH tunnel from your laptop:

```bash
ssh -N -L 8766:localhost:8766 botuser@YOUR_VPS_IP
```

Then open `http://localhost:8766` in your browser. The tunnel forwards your local port 8766 to the server's `localhost:8766` over the encrypted SSH connection.

To run the tunnel in the background:
```bash
ssh -fN -L 8766:localhost:8766 botuser@YOUR_VPS_IP
```

To kill it later:
```bash
pkill -f "ssh -fN -L 8766"
```

---

## Part 5 — Keeping it running

### Restart policy

Both services already have `restart: unless-stopped` in `docker-compose.yml`. If the server reboots, Docker starts automatically and brings both containers back up.

Make sure Docker starts on boot:
```bash
sudo systemctl enable docker
```

### Useful commands

```bash
# View live logs
docker compose logs -f weather-bot
docker compose logs -f dashboard

# Restart a single service without downtime on the other
docker compose restart weather-bot
docker compose restart dashboard

# Pull code updates and rebuild
git pull
docker compose build
docker compose up -d   # rolls containers with zero config change

# Stop everything
docker compose down

# View trade logs (persisted in Docker volume)
docker compose exec weather-bot cat data/trades/weather.log
```

### If you get locked out of SSH

1. Go to **Hetzner Cloud Console → Server → Console** (browser-based terminal, bypasses SSH)
2. Log in as `botuser`
3. Update the Hetzner firewall allowlist with your new IP
4. Update UFW: `sudo ufw delete allow from OLD.IP && sudo ufw allow from NEW.IP to any port 22 proto tcp`

---

## Part 6 — Optional: HTTPS with nginx

Rather than hitting port 8766 directly, put nginx in front with a Let's Encrypt cert.
Requires a domain name pointed at your VPS IP.

```bash
sudo apt install nginx certbot python3-certbot-nginx -y
```

`/etc/nginx/sites-available/polybot`:
```nginx
server {
    listen 80;
    server_name dashboard.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8766;
        proxy_http_version 1.1;

        # Required for WebSocket connections
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;

        proxy_read_timeout 86400s;   # keep WebSocket alive
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/polybot /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
sudo certbot --nginx -d dashboard.yourdomain.com
```

Update the **Hetzner firewall** to replace the 8766 rule:

| Protocol | Port | Source |
|----------|------|--------|
| TCP | 22 | `your.public.ip/32` |
| TCP | 80 | `0.0.0.0/0` |
| TCP | 443 | `0.0.0.0/0` |

Update **UFW** to match:
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

The dashboard is now at `https://dashboard.yourdomain.com`.
