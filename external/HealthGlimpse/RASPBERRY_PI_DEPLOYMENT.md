# 🍓 HealthGlimpse+ Raspberry Pi Deployment Guide

## Hardware Configuration Detected
- **Model**: Generic ARM Device
- **Architecture**: arm64
- **RAM**: 4096MB
- **CPU Cores**: 10
- **Recommended Config**: cpu_optimized

## Quick Deployment Steps

### 1. System Preparation
```bash
# Run system setup
chmod +x setup_system.sh
./setup_system.sh

# Reboot after setup
sudo reboot
```

### 2. Deploy Application
```bash
# Copy application files to Pi
scp -r HealthGlimpse/ pi@your-pi-ip:/tmp/

# On Raspberry Pi, move to final location
sudo mv /tmp/HealthGlimpse /opt/healthglimpse
sudo chown -R pi:pi /opt/healthglimpse
cd /opt/healthglimpse

# Make scripts executable
chmod +x *.sh
chmod +x *.py
```

### 3. Download Model
```bash
# Download appropriate model for your Pi
python3 download_model_rpi.py
```

### 4. Start Application
```bash
# Start manually for testing
./start_healthglimpse.sh

# Or install as service
sudo cp supervisor_healthglimpse.conf /etc/supervisor/conf.d/
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start healthglimpse
```

### 5. Configure Web Access (Optional)
```bash
# Install nginx reverse proxy
sudo cp nginx_healthglimpse.conf /etc/nginx/sites-available/healthglimpse
sudo ln -s /etc/nginx/sites-available/healthglimpse /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo systemctl restart nginx
```

## Access Your Application

### Direct Access
- **URL**: http://your-pi-ip:3000
- **Health Check**: http://your-pi-ip:3000/health
- **API**: http://your-pi-ip:3000/api/analyze-symptoms

### Through Nginx (if configured)
- **URL**: http://your-pi-ip
- **Health Check**: http://your-pi-ip/health

## Performance Expectations

### With 4096MB RAM:
- **Model Loading**: 5-15 minutes (first time)
- **Subsequent Loads**: <30 seconds (cached)
- **Inference Time**: 2-10 minutes per analysis
- **Concurrent Users**: 1-2 maximum

### Optimization Tips:
1. **Enable Swap**: Increases available memory for model loading
2. **Response Caching**: Repeated queries return instantly
3. **Close Unused Services**: Free up RAM and CPU
4. **Use Ethernet**: More stable than WiFi for remote access

## Remote Access Setup

### SSH Configuration
```bash
# On your main computer, create SSH config
cat >> ~/.ssh/config << EOF
Host healthglimpse-pi
    HostName your-pi-ip
    User pi
    Port 22
    ServerAliveInterval 60
EOF

# Connect with: ssh healthglimpse-pi
```

### Display Configuration
```bash
# On Raspberry Pi with display
# Add to ~/.bashrc for auto-start browser
if [ "\$DISPLAY" = ":0" ]; then
    sleep 10
    chromium-browser --kiosk --no-sandbox http://localhost:3000 &
fi
```

## Monitoring and Maintenance

### Check Application Status
```bash
# View logs
tail -f /var/log/healthglimpse/app.log

# Check supervisor status
sudo supervisorctl status healthglimpse

# Monitor system resources
htop
```

### Troubleshooting

#### Model Loading Issues
```bash
# Check available memory
free -h

# Check model cache
ls -la /var/cache/healthglimpse/models_cache/

# Clear cache if corrupted
rm -rf /var/cache/healthglimpse/models_cache/
python3 download_model_rpi.py
```

#### Performance Issues
```bash
# Increase swap if needed
sudo dphys-swapfile swapoff
sudo sed -i 's/CONF_SWAPSIZE=2048/CONF_SWAPSIZE=4096/' /etc/dphys-swapfile
sudo dphys-swapfile setup
sudo dphys-swapfile swapon

# Monitor temperature
vcgencmd measure_temp

# Check for thermal throttling
vcgencmd get_throttled
```

## Security Considerations

### Basic Security
```bash
# Change default password
passwd

# Update system regularly
sudo apt update && sudo apt upgrade

# Configure firewall
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 3000
sudo ufw enable
```

### Advanced Security (Production)
- Use HTTPS with Let's Encrypt
- Configure VPN access instead of direct internet exposure
- Set up fail2ban for SSH protection
- Regular security updates

## Scaling Options

### For Better Performance:
1. **Raspberry Pi 5**: 8GB model for best performance
2. **USB 3.0 SSD**: Faster storage improves loading times
3. **Active Cooling**: Prevents thermal throttling
4. **Ethernet Connection**: More stable than WiFi

### For Multiple Users:
1. **Load Balancer**: Multiple Pi units behind nginx
2. **Cloud Hybrid**: Fall back to cloud API for heavy loads
3. **Response Caching**: Redis for persistent cache across restarts

## Configuration Files Generated

- `rpi_config.json`: Main application configuration
- `setup_system.sh`: System preparation script
- `start_healthglimpse.sh`: Application startup script
- `download_model_rpi.py`: Model download utility
- `app_rpi.py`: Optimized Flask application
- `requirements_rpi.txt`: Python dependencies
- `nginx_healthglimpse.conf`: Web server configuration
- `supervisor_healthglimpse.conf`: Process management

This deployment is optimized for Raspberry Pi's ARM architecture and limited resources while maintaining the core functionality of HealthGlimpse+.
