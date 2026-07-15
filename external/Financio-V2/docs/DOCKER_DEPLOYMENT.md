# Financio-V2 Alpha Docker Deployment

This document describes how to deploy Financio-V2 as a containerized alpha release.

## 🚀 Quick Start

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- 4GB+ RAM
- 10GB+ free disk space

### Alpha Release Deployment

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd Financio-V2
   ```

2. **Environment Configuration**
   ```bash
   # Copy environment template
   cp financio_src/.env.example financio_src/.env
   
   # Edit with your API keys
   nano financio_src/.env
   ```

3. **Build and Run**
   ```bash
   # Build and start the application
   docker-compose up -d
   
   # Check status
   docker-compose ps
   
   # View logs
   docker-compose logs -f
   ```

4. **Access the Application**
   - **Dashboard**: http://localhost:8080
   - **API Documentation**: http://localhost:10000/docs
   - **Health Check**: http://localhost:10000/api/dashboard-data

## 📦 Deployment Profiles

### Production (Default)
```bash
docker-compose up -d
```
- Runs backend API only
- Serves built frontend from backend
- Optimized for production

### With Live Trading
```bash
docker-compose --profile trading up -d
```
- Includes trading bot container
- **⚠️ WARNING**: Uses real money in live trading

### Development Mode
```bash
docker-compose --profile development up -d
```
- Runs frontend in development mode with hot reload
- Frontend available on port 8081
- Backend on port 10000

## 🔧 Configuration

### Environment Variables

Required in `financio_src/.env`:
```bash
# Alpaca Trading API
ALPACA_API_KEY=your_alpaca_api_key
ALPACA_SECRET_KEY=your_alpaca_secret_key
ALPACA_BASE_URL=https://paper-api.alpaca.markets  # Paper trading

# Email notifications (optional)
EMAIL_ADDRESS=your_email@example.com
EMAIL_PASSWORD=your_app_password
```

### Volume Mounts

- `./financio_src/logs:/app/financio_src/logs` - Trading logs
- `./models:/app/models` - ML model files
- `./financio_src/.env:/app/financio_src/.env` - Environment config

## 🛠️ Management Commands

### Application Management
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart specific service
docker-compose restart financio-app

# View live logs
docker-compose logs -f financio-app

# Scale services (if needed)
docker-compose up -d --scale financio-app=2
```

### Debugging
```bash
# Access container shell
docker-compose exec financio-app bash

# Check API health
curl http://localhost:10000/api/dashboard-data

# Monitor resource usage
docker stats
```

### Backup and Maintenance
```bash
# Backup trading data
docker-compose exec financio-app cp -r /app/financio_src/logs /backup/

# Update application
docker-compose pull
docker-compose up -d

# Clean up old images
docker image prune -f
```

## 📊 Monitoring and Health Checks

### Built-in Health Checks
- HTTP health check on `/api/dashboard-data`
- Automatic container restart on failure
- 30-second health check interval

### Monitoring URLs
- **API Status**: http://localhost:10000/api/dashboard-data
- **Live Signals**: http://localhost:10000/api/live-signals
- **Model Status**: http://localhost:10000/api/model-status

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Kill processes using ports
   sudo lsof -ti:10000 | xargs kill -9
   sudo lsof -ti:8080 | xargs kill -9
   ```

2. **Permission Denied**
   ```bash
   # Fix file permissions
   chmod +x docker-entrypoint.sh
   sudo chown -R $USER:$USER ./financio_src/logs
   ```

3. **Build Failures**
   ```bash
   # Clean build
   docker-compose down
   docker system prune -f
   docker-compose build --no-cache
   ```

4. **API Connection Issues**
   ```bash
   # Check container logs
   docker-compose logs financio-app
   
   # Test API directly
   docker-compose exec financio-app curl http://localhost:10000/api/dashboard-data
   ```

### Log Locations
- Container logs: `docker-compose logs`
- Trading logs: `./financio_src/logs/`
- Application logs: Container stdout/stderr

## 🔒 Security Considerations

### Alpha Release Security
- **Paper Trading Only**: Configured for Alpaca paper trading by default
- **Local Network**: Exposed only to localhost (modify docker-compose.yml for external access)
- **Environment Variables**: Store sensitive data in `.env` file
- **No HTTPS**: HTTP only (add reverse proxy for production HTTPS)

### Production Security Checklist
- [ ] Use HTTPS with reverse proxy (nginx/traefik)
- [ ] Implement proper authentication
- [ ] Secure API endpoints
- [ ] Use secrets management
- [ ] Enable container security scanning
- [ ] Regular security updates

## 📈 Performance Tuning

### Resource Limits
Add to docker-compose.yml services:
```yaml
deploy:
  resources:
    limits:
      memory: 2G
      cpus: '1.0'
    reservations:
      memory: 1G
      cpus: '0.5'
```

### Optimization Tips
- Use Docker multi-stage builds (already implemented)
- Enable container restart policies (already configured)
- Monitor memory usage with `docker stats`
- Use SSD storage for model files

## 🚀 Next Steps

1. **Test the alpha release thoroughly**
2. **Monitor trading performance**
3. **Set up automated backups**
4. **Plan production deployment with HTTPS**
5. **Implement monitoring and alerting**

## 📞 Support

For issues with the alpha release:
1. Check container logs: `docker-compose logs`
2. Verify API endpoints are responding
3. Check environment configuration
4. Review troubleshooting section above

---

**⚠️ Alpha Release Warning**: This is an alpha version intended for testing and evaluation. Do not use with real money without thorough testing in paper trading mode.
