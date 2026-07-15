# HealthGlimpse+ Deployment Guide

## Overview

This guide covers deploying HealthGlimpse+ in various environments, from local development to production systems. The application is designed to work offline-first, making it suitable for deployment in areas with limited or no internet connectivity.

## Quick Start (Local Development)

### Prerequisites
- Python 3.8 or higher
- 4GB RAM minimum (8GB recommended)
- 2GB free disk space
- Microphone access (for distress monitoring)

### Installation

1. **Download and extract the application**
   ```bash
   # Extract the HealthGlimpse+ files to a directory
   cd healthglimpse_plus
   ```

2. **Run the setup script**
   ```bash
   python setup.py
   ```

3. **Start the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   Open your browser and go to: `http://localhost:5000`

## Production Deployment

### System Requirements

**Minimum Requirements:**
- CPU: 2 cores, 2GHz
- RAM: 4GB
- Storage: 10GB free space
- OS: Linux (Ubuntu 18.04+), Windows 10+, or macOS 10.14+

**Recommended Requirements:**
- CPU: 4 cores, 2.5GHz
- RAM: 8GB
- Storage: 20GB SSD
- Network: Offline capability required

### Security Considerations

1. **Change default secret key**
   ```bash
   export SECRET_KEY="your-secure-random-key-here"
   ```

2. **Enable HTTPS in production**
   ```bash
   # Use reverse proxy (nginx/Apache) or configure Flask-SSLify
   pip install Flask-SSLify
   ```

3. **Restrict file permissions**
   ```bash
   chmod 600 config.py
   chmod 700 data/
   chmod 755 static/
   ```

4. **Configure firewall**
   ```bash
   # Only allow necessary ports
   sudo ufw allow 5000/tcp  # Application port
   sudo ufw enable
   ```

### Production Setup Options

## Option 1: Standalone Server

### Using Gunicorn (Recommended for Linux)

1. **Install Gunicorn**
   ```bash
   pip install gunicorn
   ```

2. **Create Gunicorn configuration**
   ```python
   # gunicorn.conf.py
   bind = "0.0.0.0:5000"
   workers = 4
   worker_class = "sync"
   worker_connections = 1000
   timeout = 30
   keepalive = 2
   max_requests = 1000
   max_requests_jitter = 100
   preload_app = True
   
   # Logging
   accesslog = "logs/access.log"
   errorlog = "logs/error.log"
   loglevel = "info"
   
   # Process naming
   proc_name = "healthglimpse"
   
   # Security
   limit_request_line = 4094
   limit_request_fields = 100
   limit_request_field_size = 8190
   ```

3. **Start with Gunicorn**
   ```bash
   mkdir logs
   gunicorn -c gunicorn.conf.py app:app
   ```

4. **Create systemd service (Linux)**
   ```ini
   # /etc/systemd/system/healthglimpse.service
   [Unit]
   Description=HealthGlimpse+ Offline Health Assistant
   After=network.target
   
   [Service]
   Type=notify
   User=healthglimpse
   Group=healthglimpse
   WorkingDirectory=/opt/healthglimpse
   ExecStart=/opt/healthglimpse/venv/bin/gunicorn -c gunicorn.conf.py app:app
   ExecReload=/bin/kill -s HUP $MAINPID
   Restart=always
   RestartSec=10
   
   [Install]
   WantedBy=multi-user.target
   ```

5. **Enable and start service**
   ```bash
   sudo systemctl enable healthglimpse
   sudo systemctl start healthglimpse
   sudo systemctl status healthglimpse
   ```

### Using Docker

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.9-slim
   
   # Set working directory
   WORKDIR /app
   
   # Install system dependencies
   RUN apt-get update && apt-get install -y \
       portaudio19-dev \
       gcc \
       && rm -rf /var/lib/apt/lists/*
   
   # Copy requirements and install Python dependencies
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   # Copy application code
   COPY . .
   
   # Create necessary directories
   RUN mkdir -p uploads logs data
   
   # Set permissions
   RUN chmod 755 app.py
   
   # Expose port
   EXPOSE 5000
   
   # Health check
   HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
     CMD curl -f http://localhost:5000/api/health-check || exit 1
   
   # Run application
   CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]
   ```

2. **Create docker-compose.yml**
   ```yaml
   version: '3.8'
   
   services:
     healthglimpse:
       build: .
       container_name: healthglimpse-app
       restart: always
       ports:
         - "5000:5000"
       volumes:
         - ./data:/app/data:ro
         - ./uploads:/app/uploads
         - ./logs:/app/logs
       environment:
         - FLASK_ENV=production
         - SECRET_KEY=${SECRET_KEY}
       healthcheck:
         test: ["CMD", "curl", "-f", "http://localhost:5000/api/health-check"]
         interval: 30s
         timeout: 10s
         retries: 3
         start_period: 40s
   ```

3. **Deploy with Docker**
   ```bash
   # Build and start
   docker-compose up -d
   
   # Check status
   docker-compose ps
   
   # View logs
   docker-compose logs -f healthglimpse
   ```

## Option 2: Reverse Proxy Setup

### Using Nginx

1. **Install Nginx**
   ```bash
   sudo apt update
   sudo apt install nginx
   ```

2. **Configure Nginx**
   ```nginx
   # /etc/nginx/sites-available/healthglimpse
   server {
       listen 80;
       server_name your-domain.com;
       
       # Redirect to HTTPS
       return 301 https://$server_name$request_uri;
   }
   
   server {
       listen 443 ssl http2;
       server_name your-domain.com;
       
       # SSL configuration
       ssl_certificate /path/to/certificate.crt;
       ssl_certificate_key /path/to/private.key;
       ssl_protocols TLSv1.2 TLSv1.3;
       ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256;
       ssl_prefer_server_ciphers off;
       
       # Security headers
       add_header X-Frame-Options DENY;
       add_header X-Content-Type-Options nosniff;
       add_header X-XSS-Protection "1; mode=block";
       add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";
       
       # Gzip compression
       gzip on;
       gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
       
       # Static files
       location /static/ {
           alias /opt/healthglimpse/static/;
           expires 1y;
           add_header Cache-Control "public, immutable";
       }
       
       # Application
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
           
           # WebSocket support (for future features)
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           
           # Timeouts
           proxy_connect_timeout 30s;
           proxy_send_timeout 30s;
           proxy_read_timeout 30s;
       }
       
       # File upload size
       client_max_body_size 16M;
       
       # Logging
       access_log /var/log/nginx/healthglimpse_access.log;
       error_log /var/log/nginx/healthglimpse_error.log;
   }
   ```

3. **Enable and start Nginx**
   ```bash
   sudo ln -s /etc/nginx/sites-available/healthglimpse /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

## Option 3: Embedded/Edge Deployment

For deployment on embedded systems or edge devices:

### Raspberry Pi Setup

1. **Install Raspberry Pi OS**
   ```bash
   # Use Raspberry Pi Imager or manual installation
   ```

2. **Install dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv portaudio19-dev
   ```

3. **Optimize for Pi**
   ```python
   # config.py modifications for Pi
   class RaspberryPiConfig(Config):
       # Reduce memory usage
       AUDIO_SAMPLE_RATE = 16000
       AUDIO_CHUNK_SIZE = 512
       
       # Limit concurrent connections
       THREADS_PER_PAGE = 2
       
       # Disable heavy features if needed
       ENABLE_IMAGE_ANALYSIS = False
       ENABLE_ADVANCED_AUDIO = False
   ```

4. **Auto-start on boot**
   ```bash
   # Add to /etc/rc.local
   cd /home/pi/healthglimpse
   python3 app.py &
   ```

### Android Deployment (using Termux)

1. **Install Termux**
   Download from F-Droid or GitHub

2. **Setup Python environment**
   ```bash
   pkg update
   pkg install python clang make libjpeg-turbo libpng
   pip install --upgrade pip
   ```

3. **Install HealthGlimpse+**
   ```bash
   cd ~/healthglimpse
   pip install -r requirements.txt
   python app.py
   ```

## Monitoring and Maintenance

### Log Management

1. **Configure log rotation**
   ```bash
   # /etc/logrotate.d/healthglimpse
   /opt/healthglimpse/logs/*.log {
       daily
       missingok
       rotate 52
       compress
       delaycompress
       notifempty
       create 644 healthglimpse healthglimpse
       postrotate
           systemctl reload healthglimpse
       endscript
   }
   ```

2. **Monitor application health**
   ```bash
   # Health check script
   #!/bin/bash
   curl -f http://localhost:5000/api/health-check || {
       echo "Application unhealthy, restarting..."
       systemctl restart healthglimpse
   }
   ```

### Backup Strategy

1. **Backup data files**
   ```bash
   #!/bin/bash
   # backup.sh
   DATE=$(date +%Y%m%d_%H%M%S)
   tar -czf "backup_$DATE.tar.gz" data/ uploads/ config.py
   ```

2. **Automated backups**
   ```bash
   # Crontab entry
   0 2 * * * /opt/healthglimpse/backup.sh
   ```

### Performance Monitoring

1. **System metrics**
   ```bash
   # Install monitoring tools
   sudo apt install htop iotop nethogs
   ```

2. **Application metrics**
   ```python
   # Add to app.py for production
   from flask import request
   import time
   import psutil
   
   @app.before_request
   def before_request():
       request.start_time = time.time()
   
   @app.after_request
   def after_request(response):
       duration = time.time() - request.start_time
       app.logger.info(f"Request: {request.path} - {response.status_code} - {duration:.3f}s")
       return response
   ```

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Find process using port 5000
   sudo lsof -i :5000
   # Kill process if needed
   sudo kill -9 <PID>
   ```

2. **Permission denied errors**
   ```bash
   # Fix file permissions
   sudo chown -R healthglimpse:healthglimpse /opt/healthglimpse
   sudo chmod -R 755 /opt/healthglimpse
   ```

3. **Audio device errors**
   ```bash
   # Check audio devices
   arecord -l
   # Test microphone
   arecord -d 5 test.wav
   ```

4. **Memory issues**
   ```bash
   # Monitor memory usage
   free -h
   # Increase swap if needed
   sudo swapon --show
   ```

### Performance Optimization

1. **Database optimization**
   ```python
   # Use more efficient data structures
   import sqlite3
   # Consider SQLite for larger datasets
   ```

2. **Caching**
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=100)
   def expensive_analysis(symptoms):
       # Cache analysis results
       pass
   ```

3. **Resource limits**
   ```bash
   # Limit resource usage
   ulimit -v 1048576  # Limit virtual memory to 1GB
   ```

## Security Hardening

### Application Security

1. **Input validation**
   ```python
   from marshmallow import Schema, fields
   
   class SymptomSchema(Schema):
       symptoms = fields.Str(required=True, validate=Length(min=1, max=1000))
       image = fields.Str(missing=None)
   ```

2. **Rate limiting**
   ```python
   from flask_limiter import Limiter
   from flask_limiter.util import get_remote_address
   
   limiter = Limiter(
       app,
       key_func=get_remote_address,
       default_limits=["100 per hour"]
   )
   ```

### System Security

1. **User isolation**
   ```bash
   # Create dedicated user
   sudo useradd -r -s /bin/false healthglimpse
   sudo usermod -L healthglimpse
   ```

2. **File system protection**
   ```bash
   # Mount with noexec
   sudo mount -o remount,noexec /tmp
   ```

## Scaling Considerations

For high-traffic deployments:

1. **Load balancing**
   ```nginx
   upstream healthglimpse_backend {
       server 127.0.0.1:5000;
       server 127.0.0.1:5001;
       server 127.0.0.1:5002;
   }
   ```

2. **Database replication**
   ```python
   # Consider database clustering for large-scale deployment
   ```

3. **Content delivery**
   ```nginx
   # Cache static content
   location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
       expires 1y;
       add_header Cache-Control "public, immutable";
   }
   ```

This deployment guide provides comprehensive instructions for various deployment scenarios. Choose the option that best fits your environment and requirements.