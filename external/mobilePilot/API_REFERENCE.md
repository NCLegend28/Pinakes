# mobilePilot API Quick Reference

## 🚀 Getting Started

### Start Server
```bash
python main.py
# or
python start.py start
# or
./dev.py  # Interactive menu
```

### Access Points
- **API Base**: `http://localhost:8000`
- **Documentation**: `http://localhost:8000/docs`
- **Alternative Docs**: `http://localhost:8000/redoc`

## 🔐 Authentication

### Login (Get Token)
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "changeme123"}'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### Use Token in Requests
```bash
# Add to all authenticated requests:
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 📋 API Endpoints

### Health & Status

#### Root Check
```bash
curl http://localhost:8000/
```

#### Detailed Health
```bash
curl http://localhost:8000/health
```

### Copilot Integration

#### Send Prompt
```bash
curl -X POST "http://localhost:8000/copilot/prompt" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a function to calculate fibonacci",
    "action_type": "suggestion",
    "context": "Python function needed",
    "file_path": "/path/to/file.py"
  }'
```

#### Get All Responses
```bash
curl -H "Authorization: Bearer TOKEN" \
  "http://localhost:8000/copilot/responses"
```

#### Get Filtered Responses
```bash
# Filter by status: pending, approved, rejected, executed
curl -H "Authorization: Bearer TOKEN" \
  "http://localhost:8000/copilot/responses?status_filter=pending"
```

#### Execute Action
```bash
curl -X POST "http://localhost:8000/copilot/execute" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "response_id": "uuid-here",
    "approved": true
  }'
```

### Notifications

#### Send Notification
```bash
curl -X POST "http://localhost:8000/notifications/send" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Test notification",
    "title": "mobilePilot",
    "user_id": "user123",
    "data": {"key": "value"}
  }'
```

## 🧪 Testing

### Run All Tests
```bash
python test_api.py
```

### Quick Health Check
```bash
curl -s http://localhost:8000/health | python3 -m json.tool
```

### Test Authentication Flow
```bash
# 1. Login and save token
TOKEN=$(curl -s -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "changeme123"}' | \
  python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

# 2. Use token to send prompt
curl -X POST "http://localhost:8000/copilot/prompt" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello Copilot!", "action_type": "suggestion"}'
```

## 📱 Mobile Integration Workflow

### Typical Flow:
1. **Mobile app sends prompt** → `POST /copilot/prompt`
2. **Server processes with Copilot** → Returns response_id
3. **Background notification sent** → Mobile receives notification
4. **User approves/rejects** → `POST /copilot/execute`
5. **Action executed on desktop** → Result returned

### Example Mobile Session:
```bash
# 1. Authenticate
TOKEN="your-token-here"

# 2. Send prompt from mobile
RESPONSE=$(curl -s -X POST "http://localhost:8000/copilot/prompt" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Add error handling to this function", "action_type": "suggestion"}')

# 3. Extract response ID
RESPONSE_ID=$(echo $RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")

# 4. User receives notification, approves action
curl -X POST "http://localhost:8000/copilot/execute" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"response_id\": \"$RESPONSE_ID\", \"approved\": true}"
```

## ⚙️ Configuration

### Environment Variables (.env)
```bash
SECRET_KEY=your-secure-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

### Change Default Password
Edit `users_db` in `main.py`:
```python
users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("your-new-password"),
        "is_active": True
    }
}
```

## 🔧 Development

### Start Development Server
```bash
python main.py  # Auto-reload enabled
```

### Generate New Secret Key
```bash
python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"
```

### Check Server Status
```bash
# Check if running
curl -f http://localhost:8000/health > /dev/null && echo "Server is running" || echo "Server is down"

# Kill server
pkill -f "uvicorn.*main:app"
```

## 📊 Response Formats

### Success Response
```json
{
  "message": "Action executed successfully",
  "response_id": "uuid-here",
  "status": "executed"
}
```

### Error Response
```json
{
  "detail": "Could not validate credentials"
}
```

### Copilot Response
```json
{
  "id": "uuid-here",
  "prompt": "Original user prompt",
  "response": "Copilot's suggestion",
  "action_type": "suggestion",
  "timestamp": "2025-06-19T19:30:53.435706",
  "status": "pending"
}
```

## 🚨 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
lsof -ti:8000 | xargs kill -9
```

#### Authentication Errors
- Check token expiration (60 minutes default)
- Verify token format: `Bearer <token>`
- Ensure correct username/password

#### Server Not Responding
- Check if server is running: `curl http://localhost:8000/`
- Check logs for errors
- Restart server: `python main.py`

#### Module Import Errors
```bash
# Activate virtual environment
source .venv/bin/activate
# Install dependencies
pip install -r requirements.txt
```

---

**Next**: Implement VSCode extension integration for real Copilot interaction!
