# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Core Commands

### Server Management

**Start the FastAPI server (main):**
```bash
python main.py
```

**Alternative server startup methods:**
```bash
python start.py start        # With management commands
./dev.py                     # Interactive menu with options
```

**Server with specific configuration:**
```bash
python start.py start --host 0.0.0.0 --port 8000
```

**Kill running server:**
```bash
pkill -f "uvicorn.*main:app"
```

### Development Tasks

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Setup environment (initial setup):**
```bash
cp .env.example .env         # Create env file
python start.py setup        # Install deps & setup
python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"  # Generate secret key
```

**Run tests:**
```bash
# Quick API health check
python test_server.py

# Test authentication flow
python test_auth_comprehensive.py

# Test Copilot discovery
python test_complete_discovery.py

# Demo complete workflow
python demo_complete_workflow.py
```

### VSCode Extension Development

**Build the extension:**
```bash
cd vscode-extension
npm install
npm run build               # Production build
npm run build-dev          # Development build
```

**Watch mode for development:**
```bash
cd vscode-extension
npm run watch
```

**Package extension:**
```bash
cd vscode-extension
npm run package            # Creates .vsix file
```

## Architecture Overview

### System Components

1. **FastAPI Server (`main.py`)** - Core REST API server
   - JWT authentication with Bearer tokens
   - Copilot command queue system for mobile-to-VSCode communication
   - Request polling mechanism for VSCode extension
   - CORS configured for remote access (ngrok, Tailscale)

2. **VSCode Extension (`vscode-extension/`)** - Bridge to GitHub Copilot
   - Auto-connects to FastAPI server on startup
   - Polls for pending Copilot requests every 3 seconds
   - Executes real GitHub Copilot commands via VSCode API
   - Instance discovery for multi-workspace support

3. **Frontend Dashboard (`frontend/`)** - Web control interface
   - Real-time server status monitoring
   - Multi-instance VSCode management
   - Interactive Copilot request testing
   - Mobile-responsive design

### Request Flow Architecture

```
Mobile Device → FastAPI Server → Request Queue → VSCode Extension → GitHub Copilot
                      ↓                              ↓
                Response Storage ← Status Update ← Command Execution
                      ↓
              Mobile Notification
```

### Key API Endpoints

**Authentication:**
- `POST /auth/login` - Get JWT token (username: admin, password: changeme123 by default)

**Copilot Control (Real Integration):**
- `POST /copilot/trigger-suggestion` - Trigger inline suggestions
- `POST /copilot/explain-code` - Get code explanations
- `POST /copilot/fix-code` - Request code fixes
- `POST /copilot/create-file` - Generate new files
- `GET /copilot/pending-requests` - Poll for mobile requests (VSCode extension uses this)
- `POST /copilot/complete-request` - Mark request as completed

**Instance Discovery:**
- `POST /vscode/register-instance` - Register VSCode instance
- `GET /vscode/instances` - List all connected instances
- `POST /vscode/update-instance` - Update instance status

### Authentication & Security

The system uses JWT Bearer token authentication. Default credentials:
- Username: `admin`
- Password: `changeme123` (change via ADMIN_PASSWORD in .env)

All API requests except `/`, `/health` require authentication header:
```
Authorization: Bearer <JWT_TOKEN>
```

Token expires after 60 minutes (configurable via ACCESS_TOKEN_EXPIRE_MINUTES).

### Mobile Remote Access

The system supports remote access through:

1. **ngrok** - For public internet access
2. **Tailscale** - For secure private network access
3. **Direct LAN** - For local network testing

CORS is configured to accept requests from:
- Local development (localhost:3000, localhost:8080)
- ngrok tunnels (*.ngrok.io, *.ngrok-free.app)
- Tailscale network (*.ts.net)

### Module System

**Core Modules (`modules/`):**
- `api_tester.py` - API endpoint testing utilities
- `auth_manager.py` - Authentication management
- `health_monitor.py` - System health checks
- `request_manager.py` - Request queue management
- `system_monitor.py` - System status monitoring

### Configuration Files

- `.env` - Environment variables (create from .env.example)
- `.vscode/settings.json` - VSCode workspace settings
- `vscode-extension/package.json` - Extension manifest
- `requirements.txt` - Python dependencies

### Testing Approach

The codebase includes comprehensive test scripts for different components:

1. **Server Testing** - `test_server.py` tests all API endpoints
2. **Auth Testing** - `test_auth_comprehensive.py` validates authentication flow
3. **Discovery Testing** - `test_complete_discovery.py` tests VSCode instance discovery
4. **Integration Testing** - `demo_complete_workflow.py` demonstrates end-to-end flow

### Quick Debugging

**Check server status:**
```bash
curl http://localhost:8000/health | python3 -m json.tool
```

**Get auth token quickly:**
```bash
TOKEN=$(curl -s -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "changeme123"}' | \
  python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
```

**Test Copilot endpoint:**
```bash
curl -X POST "http://localhost:8000/copilot/trigger-suggestion" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Test prompt", "language": "python"}'
```

### Production Deployment Notes

1. **Change default credentials** in production
2. **Generate strong SECRET_KEY** for JWT signing
3. **Restrict CORS origins** in `main.py` (remove "*")
4. **Use HTTPS** with proper certificates
5. **Enable rate limiting** (currently TODO)
6. **Set DEBUG=False** in .env
7. **Use production database** instead of in-memory storage
