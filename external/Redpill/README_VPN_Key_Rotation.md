# VPN Key Rotation System

A comprehensive solution for automatically rotating VPN server keys to enhance security.

## 🔐 Features

- **Automated Key Rotation**: Schedule regular rotation of VPN keys and certificates
- **Multiple VPN Support**: OpenVPN, WireGuard, and strongSwan
- **Secure Backup & Recovery**: Automatic backups with integrity verification
- **Service Management**: Automatic VPN service restart with health checks
- **Monitoring & Alerts**: Comprehensive logging and notification system
- **Security-First Design**: Secure file deletion and permission management

## 📋 Requirements

### System Requirements
- Linux server with systemd
- Python 3.6+
- OpenSSL toolkit
- Root privileges (for key management)

### For OpenVPN:
```bash
sudo apt update
sudo apt install openvpn openssl python3 python3-pip
```

### For WireGuard:
```bash
sudo apt update  
sudo apt install wireguard-tools python3 python3-pip
```

### Optional Dependencies:
```bash
# For email notifications
sudo apt install mailutils

# For enhanced logging
sudo apt install rsyslog
```

## 🚀 Installation

1. **Copy the scripts to your server:**
```bash
sudo mkdir -p /opt/vpn-key-rotation
sudo cp vpn_key_rotation.py /opt/vpn-key-rotation/
sudo cp vpn_scheduler.sh /opt/vpn-key-rotation/
sudo chmod +x /opt/vpn-key-rotation/*.py
sudo chmod +x /opt/vpn-key-rotation/*.sh
```

2. **Create configuration directory:**
```bash
sudo mkdir -p /etc/vpn-key-rotation
```

3. **Generate initial configuration:**
```bash
cd /opt/vpn-key-rotation
sudo python3 vpn_key_rotation.py --config /etc/vpn-key-rotation/config.json
```

## ⚙️ Configuration

Edit `/etc/vpn-key-rotation/config.json` to match your setup:

```json
{
    "vpn_type": "openvpn",
    "server_config_path": "/etc/openvpn/server.conf",
    "ca_path": "/etc/openvpn/ca.crt",
    "server_cert_path": "/etc/openvpn/server.crt",
    "server_key_path": "/etc/openvpn/server.key",
    "dh_path": "/etc/openvpn/dh.pem",
    "ta_key_path": "/etc/openvpn/ta.key",
    "backup_directory": "/opt/vpn-backups",
    "rotation_interval_days": 30,
    "service_name": "openvpn@server",
    "restart_service": true,
    "notify_clients": false,
    "max_backups": 10,
    "logging": {
        "level": "INFO",
        "file": "/var/log/vpn-key-rotation.log",
        "max_size_mb": 10,
        "backup_count": 5
    },
    "security": {
        "key_size": 2048,
        "cert_validity_days": 365,
        "require_sudo": true,
        "secure_delete": true
    }
}
```

### Key Configuration Options:

- **`vpn_type`**: VPN software type (`openvpn`, `wireguard`, `strongswan`)
- **`rotation_interval_days`**: How often to rotate keys (default: 30 days)
- **`backup_directory`**: Where to store key backups
- **`service_name`**: systemd service name for your VPN
- **`key_size`**: RSA key size for certificate generation
- **`cert_validity_days`**: How long new certificates are valid

## 🔧 Usage

### Manual Key Rotation

```bash
# Perform immediate key rotation
sudo python3 /opt/vpn-key-rotation/vpn_key_rotation.py

# Dry run (show what would be done)
sudo python3 /opt/vpn-key-rotation/vpn_key_rotation.py --dry-run

# Force rotation even if not due
sudo python3 /opt/vpn-key-rotation/vpn_key_rotation.py --force

# Restore from backup
sudo python3 /opt/vpn-key-rotation/vpn_key_rotation.py --restore /opt/vpn-backups/vpn_keys_backup_20231201_120000
```

### Automated Scheduling

```bash
# Install automatic weekly rotation
sudo /opt/vpn-key-rotation/vpn_scheduler.sh --install-cron

# Check VPN health
sudo /opt/vpn-key-rotation/vpn_scheduler.sh --health-check

# Force rotation via scheduler
sudo /opt/vpn-key-rotation/vpn_scheduler.sh --force

# Remove automatic rotation
sudo /opt/vpn-key-rotation/vpn_scheduler.sh --remove-cron
```

## 📊 Monitoring & Notifications

### Log Files
- **Main log**: `/var/log/vpn-key-rotation.log`
- **Scheduler log**: `/var/log/vpn-key-rotation-scheduler.log`
- **System log**: Check `journalctl -u openvpn@server`

### Email Notifications
Configure email notifications by installing `mailutils`:
```bash
sudo apt install mailutils
# Configure as prompted for your email setup
```

### Slack Integration
Set environment variable for Slack webhook:
```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

### Health Check Monitoring
```bash
# Check VPN service status
sudo systemctl status openvpn@server

# View active connections
sudo cat /var/log/openvpn/status.log

# Monitor rotation logs
sudo tail -f /var/log/vpn-key-rotation.log
```

## 🔒 Security Best Practices

### File Permissions
```bash
# Secure the configuration directory
sudo chmod 700 /etc/vpn-key-rotation
sudo chown root:root /etc/vpn-key-rotation/config.json
sudo chmod 600 /etc/vpn-key-rotation/config.json

# Secure backup directory
sudo chmod 700 /opt/vpn-backups
sudo chown root:root /opt/vpn-backups
```

### Network Security
- Run VPN on non-standard ports
- Use strong DH parameters (2048-bit minimum)
- Enable TLS-Auth for additional security layer
- Regularly review VPN logs for anomalies

### Key Management
- Keep CA private key on separate, secure system
- Use strong passphrases for CA key
- Regularly audit backup integrity
- Test restoration procedures

## 🛠️ Troubleshooting

### Common Issues

**1. Permission Denied Errors**
```bash
# Ensure script runs as root
sudo python3 /opt/vpn-key-rotation/vpn_key_rotation.py

# Check file permissions
ls -la /etc/openvpn/
```

**2. Service Restart Failures**
```bash
# Check service status
sudo systemctl status openvpn@server

# Manual restart
sudo systemctl restart openvpn@server

# Check configuration
sudo openvpn --config /etc/openvpn/server.conf --test-crypto
```

**3. Certificate Generation Errors**
```bash
# Verify OpenSSL installation
openssl version

# Check CA certificate and key
openssl x509 -in /etc/openvpn/ca.crt -text -noout
openssl rsa -in /etc/openvpn/ca.key -check
```

**4. Backup/Restore Issues**
```bash
# Check backup directory permissions
ls -la /opt/vpn-backups/

# Verify backup integrity
sudo python3 /opt/vpn-key-rotation/vpn_key_rotation.py --verify-backup /opt/vpn-backups/latest
```

### Debug Mode
Enable debug logging by modifying config:
```json
{
    "logging": {
        "level": "DEBUG"
    }
}
```

## 📅 Maintenance

### Regular Tasks

**Weekly:**
- Review rotation logs
- Check VPN service health
- Monitor backup disk usage

**Monthly:**
- Test backup restoration procedure
- Review and rotate admin access logs
- Update system packages

**Quarterly:**
- Review security configurations
- Test emergency procedures
- Audit client certificate status

### Backup Management
```bash
# List all backups
ls -la /opt/vpn-backups/

# Check backup ages
find /opt/vpn-backups/ -name "vpn_keys_backup_*" -type d -printf "%T@ %Tc %p\n" | sort -n

# Manual cleanup (keeps last 5 backups)
cd /opt/vpn-backups && ls -t | tail -n +6 | xargs rm -rf
```

## 🔄 Migration & Updates

### Updating the Scripts
```bash
# Backup current version
sudo cp -r /opt/vpn-key-rotation /opt/vpn-key-rotation.backup

# Install new version
sudo cp new_vpn_key_rotation.py /opt/vpn-key-rotation/
sudo chmod +x /opt/vpn-key-rotation/vpn_key_rotation.py

# Test with dry run
sudo python3 /opt/vpn-key-rotation/vpn_key_rotation.py --dry-run
```

### VPN Software Migration
When changing VPN software:
1. Update `vpn_type` in configuration
2. Update file paths to match new VPN structure
3. Test rotation with `--dry-run` first
4. Update service name in configuration

## 📞 Support

### Getting Help
- Check log files for error details
- Test with `--dry-run` option first
- Verify all dependencies are installed
- Ensure proper file permissions

### Error Reporting
When reporting issues, include:
- Configuration file (sanitized)
- Relevant log entries
- System information (OS, VPN software versions)
- Steps to reproduce the issue

## 📋 Example Workflow

### Initial Setup
```bash
# 1. Install and configure
sudo mkdir -p /opt/vpn-key-rotation
sudo cp vpn_*.py vpn_*.sh /opt/vpn-key-rotation/
sudo chmod +x /opt/vpn-key-rotation/*

# 2. Generate config
sudo python3 /opt/vpn-key-rotation/vpn_key_rotation.py

# 3. Edit configuration
sudo nano /etc/vpn-key-rotation/config.json

# 4. Test manually
sudo python3 /opt/vpn-key-rotation/vpn_key_rotation.py --dry-run

# 5. Perform first rotation
sudo python3 /opt/vpn-key-rotation/vpn_key_rotation.py --force

# 6. Setup automation
sudo /opt/vpn-key-rotation/vpn_scheduler.sh --install-cron
```

### Regular Operations
```bash
# Check status
sudo /opt/vpn-key-rotation/vpn_scheduler.sh --health-check

# View logs
sudo tail -f /var/log/vpn-key-rotation.log

# Manual rotation if needed
sudo /opt/vpn-key-rotation/vpn_scheduler.sh --force
```

This system provides enterprise-grade VPN key rotation with comprehensive security, monitoring, and recovery capabilities.