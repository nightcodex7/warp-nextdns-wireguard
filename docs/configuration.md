# Configuration Guide

> **Advanced configuration options for WARP + NextDNS Manager**

Learn how to customize and configure the WARP + NextDNS Manager for your specific needs.

## 🔧 Configuration Overview

The WARP + NextDNS Manager uses several configuration files and options to customize its behavior. Most settings are automatically configured during setup, but you can modify them for advanced use cases.

## 📁 Configuration Files

### Main Configuration Files

| File | Purpose | Location |
|------|---------|----------|
| **WGCF Config** | WARP WireGuard configuration | `/etc/wireguard/wgcf.conf` |
| **NextDNS Config** | NextDNS client configuration | `/etc/nextdns.conf` |
| **System Services** | Auto-start service definitions | `/etc/systemd/system/` |
| **Log Files** | Application and service logs | `/var/log/` |

### User Configuration

| File | Purpose | Location |
|------|---------|----------|
| **User Config** | User-specific settings | `~/.warp-nextdns/config.yaml` |
| **Cache Directory** | Temporary files and cache | `~/.warp-nextdns/cache/` |
| **Backup Directory** | Configuration backups | `~/.warp-nextdns/backups/` |

## ⚙️ WGCF Configuration

### Basic WGCF Settings

The WGCF configuration is automatically generated but can be customized:

```ini
# /etc/wireguard/wgcf.conf
[Interface]
PrivateKey = YOUR_PRIVATE_KEY
Address = 172.16.0.2/32
DNS = 127.0.0.1
MTU = 1280

[Peer]
PublicKey = CLOUDFLARE_PUBLIC_KEY
AllowedIPs = 0.0.0.0/0
Endpoint = 162.159.193.10:2408
PersistentKeepalive = 25
```

### Customizing WGCF

```bash
# Edit WGCF configuration
sudo nano /etc/wireguard/wgcf.conf

# Regenerate WGCF configuration
python cli.py setup --regenerate-wgcf

# Apply changes
python cli.py restart
```

### WGCF Options

```bash
# Use specific WGCF version
python cli.py setup --wgcf-version 2.2.15

# Custom WGCF binary path
python cli.py setup --wgcf-path /custom/path/wgcf

# Force WGCF re-registration
python cli.py setup --force-wgcf-register
```

## 🌐 NextDNS Configuration

### Basic NextDNS Settings

```yaml
# /etc/nextdns.conf
config YOUR_PROFILE_ID
report-client-info true
auto-activate true
listen 127.0.0.1:53
max-ttl 5s
bogus-priv true
use-hosts true
timeout 5s
```

### Advanced NextDNS Options

```bash
# Configure NextDNS with custom settings
python cli.py setup --nextdns-args "--listen 0.0.0.0:53 --max-ttl 10s"

# Use custom NextDNS configuration
python cli.py setup --nextdns-config /path/to/custom/nextdns.conf

# Enable NextDNS analytics
python cli.py setup --enable-nextdns-analytics
```

### NextDNS Filtering Options

```yaml
# Custom filtering rules
blocklist https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts
blocklist https://raw.githubusercontent.com/pi-hole/pi-hole/master/gravity.list

# Whitelist domains
whitelist google.com
whitelist github.com

# Custom DNS servers
upstream 1.1.1.1
upstream 8.8.8.8
```

## 🔄 System Service Configuration

### Linux Systemd Services

#### WGCF Service
```ini
# /etc/systemd/system/wgcf.service
[Unit]
Description=WGCF WARP WireGuard Interface
After=network-online.target
Wants=network-online.target
ConditionPathExists=/etc/wireguard/wgcf.conf

[Service]
Type=oneshot
ExecStartPre=/sbin/modprobe wireguard
ExecStart=/usr/bin/wg-quick up wgcf
ExecStop=/usr/bin/wg-quick down wgcf
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

#### NextDNS Service
```ini
# /etc/systemd/system/nextdns.service
[Unit]
Description=NextDNS DNS over HTTPS proxy
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/usr/bin/nextdns start
ExecStop=/usr/bin/nextdns stop
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### Windows Service Configuration

```powershell
# Create Windows service
sc create "WARPNextDNS" binPath="C:\path\to\warp-nextdns.exe start" start=auto

# Configure service
sc config "WARPNextDNS" start=auto
sc config "WARPNextDNS" obj="LocalSystem"
```

### macOS Launchd Configuration

```xml
<!-- /Library/LaunchDaemons/com.warp-nextdns.manager.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.warp-nextdns.manager</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/usr/local/bin/warp-nextdns</string>
        <string>start</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

## 🔐 Security Configuration

### Firewall Rules

#### Linux (iptables)
```bash
# Allow WireGuard traffic
sudo iptables -A INPUT -p udp --dport 51820 -j ACCEPT
sudo iptables -A OUTPUT -p udp --sport 51820 -j ACCEPT

# Allow DNS traffic
sudo iptables -A INPUT -p udp --dport 53 -j ACCEPT
sudo iptables -A OUTPUT -p udp --dport 53 -j ACCEPT
```

#### Windows (Firewall)
```powershell
# Allow WireGuard
New-NetFirewallRule -DisplayName "WARP WireGuard" -Direction Inbound -Protocol UDP -LocalPort 51820 -Action Allow

# Allow DNS
New-NetFirewallRule -DisplayName "NextDNS" -Direction Inbound -Protocol UDP -LocalPort 53 -Action Allow
```

### Network Security

```bash
# Configure secure DNS
python cli.py setup --secure-dns --dns-over-https

# Enable DNS filtering
python cli.py setup --enable-dns-filtering

# Configure network isolation
python cli.py setup --network-isolation
```

## 📊 Monitoring Configuration

### Logging Configuration

```yaml
# ~/.warp-nextdns/config.yaml
logging:
  level: INFO
  file: /var/log/warp-nextdns.log
  max_size: 10MB
  backup_count: 5
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

### Monitoring Setup

```bash
# Enable monitoring
python cli.py setup --enable-monitoring

# Configure monitoring interval
python cli.py setup --monitoring-interval 30

# Set up alerts
python cli.py setup --enable-alerts --alert-email your@email.com
```

### Health Checks

```bash
# Configure health check endpoints
python cli.py setup --health-check-urls "https://1.1.1.1,https://8.8.8.8"

# Set health check interval
python cli.py setup --health-check-interval 60

# Configure failure thresholds
python cli.py setup --health-check-threshold 3
```

## 🚀 Performance Configuration

### Network Optimization

```bash
# Optimize MTU settings
python cli.py setup --optimize-mtu

# Configure buffer sizes
python cli.py setup --buffer-size 65536

# Enable TCP optimization
python cli.py setup --tcp-optimization
```

### Resource Limits

```yaml
# Resource configuration
resources:
  max_memory: 512MB
  max_cpu_percent: 50
  max_connections: 1000
  timeout: 30s
```

## 🔧 Advanced Configuration

### Custom Scripts

```bash
# Pre-start script
python cli.py setup --pre-start-script /path/to/pre-start.sh

# Post-start script
python cli.py setup --post-start-script /path/to/post-start.sh

# Health check script
python cli.py setup --health-check-script /path/to/health-check.sh
```

### Environment Variables

```bash
# Set environment variables
export WARP_NEXTDNS_DEBUG=true
export WARP_NEXTDNS_LOG_LEVEL=DEBUG
export WARP_NEXTDNS_CONFIG_PATH=/custom/config/path

# Use in configuration
python cli.py setup --env-file /path/to/env.conf
```

### Custom Integrations

```bash
# Integrate with monitoring systems
python cli.py setup --prometheus-metrics
python cli.py setup --grafana-dashboard

# Webhook notifications
python cli.py setup --webhook-url https://your-webhook.com/notify

# Slack integration
python cli.py setup --slack-webhook https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

## 📝 Configuration Examples

### Home Network Setup

```bash
# Basic home setup
python cli.py setup \
  --profile-id YOUR_PROFILE_ID \
  --auto-start \
  --enable-logging \
  --monitoring-interval 300
```

### Server Setup

```bash
# Production server setup
python cli.py setup \
  --profile-id YOUR_PROFILE_ID \
  --server-mode \
  --enable-monitoring \
  --enable-alerts \
  --secure-mode \
  --health-check-interval 60
```

### Development Setup

```bash
# Development environment
python cli.py setup \
  --dev-mode \
  --debug \
  --log-level DEBUG \
  --disable-auto-start \
  --custom-config /path/to/dev/config.yaml
```

## 🔄 Configuration Management

### Backup Configuration

```bash
# Create backup
python cli.py backup --output config-backup-$(date +%Y%m%d).tar.gz

# List backups
python cli.py backup --list

# Restore from backup
python cli.py restore --input config-backup-20241219.tar.gz
```

### Version Control

```bash
# Track configuration changes
git add /etc/wireguard/wgcf.conf
git add /etc/nextdns.conf
git commit -m "Update WARP NextDNS configuration"

# Rollback configuration
python cli.py restore --git-commit HEAD~1
```

### Configuration Validation

```bash
# Validate configuration
python cli.py config --validate

# Test configuration
python cli.py config --test

# Generate configuration report
python cli.py config --report config-report.txt
```

## 🆘 Troubleshooting Configuration

### Common Issues

#### Configuration File Permissions
```bash
# Fix permissions
sudo chmod 600 /etc/wireguard/wgcf.conf
sudo chmod 644 /etc/nextdns.conf
sudo chown root:root /etc/wireguard/wgcf.conf
```

#### Service Configuration
```bash
# Reload systemd
sudo systemctl daemon-reload

# Restart services
sudo systemctl restart wgcf
sudo systemctl restart nextdns
```

#### Network Configuration
```bash
# Check network interfaces
ip link show
ip addr show

# Test connectivity
ping 1.1.1.1
nslookup google.com 127.0.0.1
```

## 📚 Next Steps

After configuring your setup:

1. **[Usage Guide](usage.md)** - Learn how to use the configured system
2. **[Troubleshooting Guide](troubleshooting.md)** - Solve configuration issues
3. **[API Reference](api.md)** - Advanced configuration via API

---

**Need help?** Check our [troubleshooting guide](troubleshooting.md) or [create an issue](https://github.com/nightcodex7/warp-nextdns-wireguard/issues). 