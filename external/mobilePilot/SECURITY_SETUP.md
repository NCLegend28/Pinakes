# 🔐 Security Setup Guide

This guide helps you secure your mobilePilot installation before running it in production.

## ⚠️ Critical Security Steps

### 1. Change Default Password
```bash
# Copy the environment template
cp .env.example .env

# Edit .env and change the admin password
ADMIN_PASSWORD=your-new-secure-password-here
```

### 2. Generate Secure Secret Key
```bash
# Generate a secure secret key
python start.py keygen

# Copy the generated key to your .env file
SECRET_KEY=your-generated-secret-key-here
```

### 3. Restrict CORS Origins
Edit your `.env` file and update CORS settings:
```bash
# Remove the wildcard (*) and specify exact origins
ALLOWED_ORIGINS=https://yourdomain.com,https://api.yourdomain.com
```

### 4. Update Production Settings
```bash
# In .env for production
DEBUG=False
RELOAD=False
LOG_LEVEL=WARNING
```

## 🚨 Security Warnings

The server will show warnings on startup if you haven't addressed these issues:

- ⚠️ **Default SECRET_KEY**: Change the JWT signing key
- ⚠️ **Default password**: Change the admin password  
- ⚠️ **Open CORS**: Restrict allowed origins

## ✅ Verification

After making changes, run:
```bash
python start.py start
```

Check the startup logs - you should see no security warnings.

## 📋 Security Checklist

- [ ] Changed admin password in `.env`
- [ ] Generated and set secure SECRET_KEY
- [ ] Restricted CORS origins 
- [ ] Set DEBUG=False for production
- [ ] Using HTTPS in production
- [ ] Regular password rotation policy
- [ ] Monitoring and logging enabled

## 🔒 Additional Security Measures

### Rate Limiting
Enable rate limiting in production:
```bash
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=60
```

### HTTPS Only
Always use HTTPS in production environments.

### Database Security
When implementing database storage:
- Use connection pooling
- Enable SQL injection protection
- Regular security updates

## 🚨 Emergency Response

If you suspect a security breach:
1. Immediately change all passwords
2. Regenerate SECRET_KEY (invalidates all tokens)
3. Review access logs
4. Update and restart the service
