# 🍓 HealthGlimpse+ Raspberry Pi Complete Deployment Guide

## Overview

This guide provides a complete solution for deploying HealthGlimpse+ to a Raspberry Pi with automatic display setup for kiosk mode. The application will run locally on the Pi and display the interface full-screen on a connected monitor.

## Prerequisites

### Hardware Requirements
- **Raspberry Pi 4** (4GB+ RAM recommended)
- **MicroSD card** (32GB+ Class 10)
- **Display** (HDMI monitor/TV or official Pi touchscreen)
- **Stable internet connection** (for model download)
- **Keyboard/Mouse** (for initial setup)

### Software Requirements
- **Raspberry Pi OS** (latest version)
- **SSH enabled** on the Pi
- **Development machine** with SSH access

## Quick Start Deployment

### Option 1: Automatic Complete Deployment

```bash
# 1. Generate deployment files (run once)
python3 deploy_raspberry_pi.py

# 2. Deploy everything with display setup
./deploy_complete.sh <raspberry-pi-ip>

# 3. After Pi reboots, continue deployment
./deploy_complete.sh <raspberry-pi-ip> --continue

# 4. Verify deployment
python3 verify_pi_deployment.py <raspberry-pi-ip>
```

### Option 2: Step-by-Step Deployment

```bash
# 1. Generate deployment configuration
python3 deploy_raspberry_pi.py

# 2. Deploy application only (no display setup)
./deploy_complete.sh <raspberry-pi-ip> --no-display

# 3. Continue after reboot
./deploy_complete.sh <raspberry-pi-ip> --continue

# 4. Setup display separately (optional)
./deploy_complete.sh <raspberry-pi-ip> --display-only
```

## Display Features

### Kiosk Mode Configuration
- **Auto-login**: Pi automatically logs in on boot
- **Full-screen browser**: HealthGlimpse+ displays in kiosk mode
- **Screen always on**: Prevents display from going to sleep
- **Auto-restart**: Monitors and restarts services if needed

### Remote Display Control
The deployment includes a display control API running on port 3001:

```bash
# Check display status
curl http://<pi-ip>:3001/display/status

# Control display power
curl http://<pi-ip>:3001/display/on
curl http://<pi-ip>:3001/display/off

# Adjust brightness (0-255)
curl http://<pi-ip>:3001/display/brightness/150

# Browser controls
curl http://<pi-ip>:3001/browser/refresh
curl http://<pi-ip>:3001/browser/reload
```

## Deployment Process Details

### Phase 1: System Setup
1. **File Transfer**: Copies all application files to Pi
2. **System Dependencies**: Installs Python, PyTorch, and system packages
3. **Directory Structure**: Creates proper directory layout
4. **Service Configuration**: Sets up supervisor and nginx

### Phase 2: Model Download
1. **AI Model**: Downloads the google/gemma-3n-e4b-it model (~12GB)
2. **Caching**: Stores model in optimized cache location
3. **Verification**: Validates model integrity

### Phase 3: Display Setup (if enabled)
1. **Desktop Environment**: Configures auto-login and display
2. **Kiosk Browser**: Sets up Chromium in full-screen mode
3. **Display Control**: Installs remote control API
4. **Monitoring**: Sets up automatic service monitoring

### Phase 4: Service Installation
1. **System Services**: Installs supervisor and nginx services
2. **Auto-start**: Configures application to start on boot
3. **Process Management**: Sets up automatic restart on failure

## Access Points

After successful deployment:

### Primary Access
- **Main Application**: `http://<pi-ip>:3000`
- **Health Check**: `http://<pi-ip>:3000/health`
- **API Endpoint**: `http://<pi-ip>:3000/api/analyze-symptoms`

### Via Nginx Proxy (if installed)
- **Main Application**: `http://<pi-ip>`
- **Health Check**: `http://<pi-ip>/health`

### Display Control
- **Control API**: `http://<pi-ip>:3001`
- **Status Check**: `http://<pi-ip>:3001/display/status`

## Performance Optimization

### Hardware Recommendations
- **Raspberry Pi 5** (8GB) for best performance
- **USB 3.0 SSD** for faster storage
- **Active cooling** to prevent throttling
- **Ethernet connection** for stability

### Software Optimizations
- **Model Caching**: First load takes 5-15 minutes, subsequent loads <30 seconds
- **Response Caching**: Repeated queries return instantly
- **Memory Management**: Automatic garbage collection
- **Swap Space**: Configured for model loading

### Expected Performance
- **Model Loading**: 5-15 minutes (first time), <30 seconds (cached)
- **Inference Time**: 2-10 minutes per analysis
- **Concurrent Users**: 1-2 maximum
- **Memory Usage**: 3-6GB during inference

## Monitoring and Maintenance

### System Monitoring
```bash
# View application logs
ssh pi@<pi-ip> 'tail -f /var/log/healthglimpse/app.log'

# Check service status
ssh pi@<pi-ip> 'sudo supervisorctl status healthglimpse'

# Monitor system resources
ssh pi@<pi-ip> 'htop'

# Check temperature and throttling
ssh pi@<pi-ip> 'vcgencmd measure_temp && vcgencmd get_throttled'
```

### Automated Monitoring
The deployment includes automatic monitoring scripts:
- **Service Monitor**: Restarts application if it becomes unresponsive
- **WiFi Monitor**: Reconnects WiFi if connection is lost
- **Display Monitor**: Keeps display active and responsive

### Manual Commands
```bash
# Restart application
ssh pi@<pi-ip> 'sudo supervisorctl restart healthglimpse'

# Restart display service
ssh pi@<pi-ip> 'sudo systemctl restart display-control'

# Refresh browser on display
curl http://<pi-ip>:3001/browser/refresh

# Reboot Pi
ssh pi@<pi-ip> 'sudo reboot'
```

## Troubleshooting

### Common Issues

#### Application Won't Start
```bash
# Check logs
ssh pi@<pi-ip> 'tail -50 /var/log/healthglimpse/app.log'

# Check model cache
ssh pi@<pi-ip> 'ls -la /var/cache/healthglimpse/models_cache/'

# Re-download model if corrupted
ssh pi@<pi-ip> 'cd /opt/healthglimpse && python3 download_model_rpi.py'
```

#### Display Issues
```bash
# Check if display is detected
ssh pi@<pi-ip> 'tvservice -s'

# Restart display service
ssh pi@<pi-ip> 'sudo systemctl restart display-control'

# Check browser process
ssh pi@<pi-ip> 'ps aux | grep chromium'
```

#### Performance Issues
```bash
# Check memory usage
ssh pi@<pi-ip> 'free -h'

# Check temperature
ssh pi@<pi-ip> 'vcgencmd measure_temp'

# Check for throttling
ssh pi@<pi-ip> 'vcgencmd get_throttled'

# Increase swap space
ssh pi@<pi-ip> 'sudo dphys-swapfile swapoff'
ssh pi@<pi-ip> 'sudo sed -i "s/CONF_SWAPSIZE=2048/CONF_SWAPSIZE=4096/" /etc/dphys-swapfile'
ssh pi@<pi-ip> 'sudo dphys-swapfile setup && sudo dphys-swapfile swapon'
```

#### Network Issues
```bash
# Check network connectivity
ssh pi@<pi-ip> 'ping -c 3 8.8.8.8'

# Check WiFi status
ssh pi@<pi-ip> 'iwconfig wlan0'

# Restart networking
ssh pi@<pi-ip> 'sudo systemctl restart networking'
```

## Security Considerations

### Basic Security
```bash
# Change default password
ssh pi@<pi-ip> 'passwd'

# Update system
ssh pi@<pi-ip> 'sudo apt update && sudo apt upgrade -y'

# Configure firewall
ssh pi@<pi-ip> 'sudo ufw allow ssh && sudo ufw allow 3000 && sudo ufw enable'
```

### Advanced Security (Production)
- Use HTTPS with Let's Encrypt certificates
- Set up VPN access instead of direct internet exposure
- Configure fail2ban for SSH protection
- Regular security updates via automated scripts

## Customization Options

### Display Configuration
Edit `/home/pi/.config/openbox/autostart` on the Pi to customize:
- Browser startup delay
- Kiosk mode options
- Screen saver settings
- Auto-refresh intervals

### Application Configuration
Edit `/opt/healthglimpse/rpi_config.json` to modify:
- Model selection (2B vs 4B)
- Generation parameters
- Memory limits
- Cache settings

### Service Configuration
- **Supervisor**: `/etc/supervisor/conf.d/supervisor_healthglimpse.conf`
- **Nginx**: `/etc/nginx/sites-available/healthglimpse`
- **Display Control**: `/etc/systemd/system/display-control.service`

## Backup and Recovery

### Create Backup
```bash
# Backup application directory
ssh pi@<pi-ip> 'sudo tar -czf /tmp/healthglimpse-backup.tar.gz /opt/healthglimpse'
scp pi@<pi-ip>:/tmp/healthglimpse-backup.tar.gz ./

# Backup configuration
ssh pi@<pi-ip> 'sudo tar -czf /tmp/healthglimpse-config.tar.gz /etc/supervisor/conf.d/ /etc/nginx/sites-available/'
scp pi@<pi-ip>:/tmp/healthglimpse-config.tar.gz ./
```

### Restore from Backup
```bash
# Restore application
scp ./healthglimpse-backup.tar.gz pi@<pi-ip>:/tmp/
ssh pi@<pi-ip> 'sudo tar -xzf /tmp/healthglimpse-backup.tar.gz -C /'

# Restore configuration
scp ./healthglimpse-config.tar.gz pi@<pi-ip>:/tmp/
ssh pi@<pi-ip> 'sudo tar -xzf /tmp/healthglimpse-config.tar.gz -C /'
```

## Scaling Options

### Single Pi Optimization
1. **Raspberry Pi 5 8GB**: Best performance for single-user deployment
2. **NVMe SSD**: Significantly faster model loading
3. **Active Cooling**: Prevents thermal throttling
4. **High-speed SD card**: Class 3 UHS-I for better I/O

### Multi-Pi Setup
1. **Load Balancer**: Multiple Pi units behind nginx load balancer
2. **Shared Model Cache**: NFS share for model files
3. **Database Backend**: PostgreSQL for user data and analytics
4. **Monitoring Stack**: Prometheus + Grafana for metrics

### Hybrid Cloud
1. **Local Priority**: Pi serves cached responses instantly
2. **Cloud Fallback**: API gateway routes heavy loads to cloud
3. **Smart Caching**: Popular queries cached locally
4. **Offline Mode**: Basic functionality without internet

## Files Generated

### Deployment Scripts
- `deploy_complete.sh` - Complete deployment automation
- `setup_pi_display.sh` - Display and kiosk mode setup
- `verify_pi_deployment.py` - Deployment verification and testing

### Configuration Files
- `rpi_config.json` - Pi-specific application configuration
- `app_rpi.py` - Optimized Flask application for Pi
- `requirements_rpi.txt` - Pi-specific Python dependencies

### System Services
- `supervisor_healthglimpse.conf` - Process management
- `nginx_healthglimpse.conf` - Reverse proxy configuration
- `display-control.service` - Display control API service

### Monitoring and Utilities
- `rpi_monitor.py` - System monitoring and diagnostics
- `download_model_rpi.py` - Pi-optimized model downloader
- `start_healthglimpse.sh` - Application startup script

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review deployment logs: `/var/log/healthglimpse/`
3. Use the verification script: `python3 verify_pi_deployment.py <pi-ip>`
4. Check system status with monitoring tools

The deployment is designed to be robust and self-healing, with automatic restart capabilities and comprehensive monitoring.
