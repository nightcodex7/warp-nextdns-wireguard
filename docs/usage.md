# Usage Guide

> **Complete guide to using WARP + NextDNS Manager**

Learn how to use all features of the WARP + NextDNS Manager effectively.

## 🚀 Getting Started

After installation, you can start using the tool immediately. The setup wizard configures everything automatically, but you can also use individual commands for more control.

## 📋 Available Commands

### Basic Commands

```bash
# Interactive setup wizard
python cli.py setup

# Check system status
python cli.py status

# Start all services
python cli.py start

# Stop all services
python cli.py stop

# Test connectivity
python cli.py test

# View service logs
python cli.py logs

# Uninstall (remove configuration)
python cli.py uninstall
```

### Advanced Commands

```bash
# Setup with specific options
python cli.py setup --profile-id YOUR_PROFILE_ID --non-interactive

# Start with auto-elevation
python cli.py start --auto-elevate

# Check detailed status
python cli.py status --verbose

# Test specific components
python cli.py test --warp-only
python cli.py test --nextdns-only
```

## 🔧 Interactive Setup

The setup wizard guides you through the entire configuration process:

```bash
python cli.py setup
```

### Setup Process

1. **System Detection**: Automatically detects your OS and architecture
2. **Dependency Installation**: Installs required system packages
3. **WGCF Configuration**: Downloads and configures WGCF for WARP
4. **NextDNS Setup**: Configures NextDNS with your profile ID
5. **Service Creation**: Creates system services for auto-start
6. **Testing**: Verifies the installation and connectivity

### Setup Options

```bash
# Non-interactive setup (for automation)
python cli.py setup --non-interactive --profile-id YOUR_PROFILE_ID

# Auto-elevation (automatic privilege escalation)
python cli.py setup --auto-elevate

# Verbose output
python cli.py setup --verbose
```

## 📊 Status Monitoring

### Check Overall Status

```bash
python cli.py status
```

Output example:
```json
{
  "platform": {
    "os": "linux",
    "platform": "Linux-5.15.0-x86_64",
    "machine": "x86_64"
  },
  "services": {
    "warp": {
      "status": "running",
      "interface": "wgcf0",
      "ip": "172.16.0.2"
    },
    "nextdns": {
      "status": "active",
      "profile": "abc123",
      "dns": "45.90.28.0"
    }
  },
  "connectivity": {
    "internet": true,
    "warp_ip": "104.28.xxx.xxx",
    "dns_leak": false
  }
}
```

### Real-time Monitoring

```bash
# Monitor with auto-refresh (every 5 seconds)
python cli.py monitor

# Custom refresh interval
python cli.py monitor --refresh 10
```

## 🔄 Service Management

### Starting Services

```bash
# Start all services
python cli.py start

# Start with auto-elevation
python cli.py start --auto-elevate

# Start specific service
python cli.py start --warp-only
python cli.py start --nextdns-only
```

### Stopping Services

```bash
# Stop all services
python cli.py stop

# Stop specific service
python cli.py stop --warp-only
python cli.py stop --nextdns-only
```

### Restarting Services

```bash
# Restart all services
python cli.py restart

# Restart specific service
python cli.py restart --warp-only
```

## 🧪 Testing and Diagnostics

### Connection Testing

```bash
# Test all components
python cli.py test

# Test specific components
python cli.py test --warp-only
python cli.py test --nextdns-only
python cli.py test --dns-leak
```

### Test Results

```bash
$ python cli.py test

✅ WARP Connection: PASS
✅ NextDNS Resolution: PASS
✅ IP Leak Test: PASS
✅ DNS Leak Test: PASS
✅ Speed Test: 150 Mbps
```

### Network Diagnostics

```bash
# Run comprehensive diagnostics
python cli.py diagnose

# Check specific aspects
python cli.py diagnose --connectivity
python cli.py diagnose --dns
python cli.py diagnose --warp
```

## 📝 Logging and Monitoring

### View Logs

```bash
# View recent logs
python cli.py logs

# Follow logs in real-time
python cli.py logs --follow

# Filter logs by service
python cli.py logs --warp
python cli.py logs --nextdns

# Filter by log level
python cli.py logs --level error
python cli.py logs --level warning
```

### Log Output

```bash
$ python cli.py logs

[2024-01-15 10:30:15] INFO: WARP service started successfully
[2024-01-15 10:30:16] INFO: NextDNS service activated
[2024-01-15 10:30:17] INFO: DNS resolution working correctly
[2024-01-15 10:30:18] INFO: All services running normally
```

## 🔧 Configuration Management

### Backup Configuration

```bash
# Create backup
python cli.py backup

# Backup to specific location
python cli.py backup --output /path/to/backup.tar.gz
```

### Restore Configuration

```bash
# Restore from backup
python cli.py restore --input /path/to/backup.tar.gz
```

### Update Configuration

```bash
# Update NextDNS profile
python cli.py config --nextdns-profile NEW_PROFILE_ID

# Update WARP configuration
python cli.py config --warp-refresh
```

## 🚨 Troubleshooting Commands

### Quick Diagnostics

```bash
# Check system health
python cli.py health

# Verify installation
python cli.py verify

# Check dependencies
python cli.py deps
```

### Advanced Troubleshooting

```bash
# Reset configuration
python cli.py reset

# Clean installation
python cli.py clean

# Force reinstall
python cli.py reinstall
```

## 📊 Performance Monitoring

### Speed Testing

```bash
# Run speed test
python cli.py speedtest

# Test specific servers
python cli.py speedtest --server cloudflare
python cli.py speedtest --server nextdns
```

### Performance Metrics

```bash
# View performance stats
python cli.py stats

# Monitor resource usage
python cli.py monitor --resources
```

## 🔐 Security Features

### Security Audit

```bash
# Run security audit
python cli.py audit

# Check specific security aspects
python cli.py audit --dns-leak
python cli.py audit --ip-leak
python cli.py audit --webrtc
```

### Privacy Testing

```bash
# Test privacy protection
python cli.py privacy

# Check fingerprinting protection
python cli.py privacy --fingerprint
```

## 🎯 Use Cases and Examples

### Daily Usage

```bash
# Start your day
python cli.py start

# Check status throughout the day
python cli.py status

# Monitor performance
python cli.py monitor

# Stop at end of day
python cli.py stop
```

### Automation

```bash
# Add to startup scripts
python cli.py start --auto-elevate

# Create monitoring script
while true; do
    python cli.py status
    sleep 300
done
```

### Development Workflow

```bash
# Quick setup for development
python cli.py setup --non-interactive --profile-id dev-profile

# Test changes
python cli.py test

# Monitor during development
python cli.py monitor --refresh 2
```

## 📱 Mobile and Remote Usage

### Remote Management

```bash
# Check status remotely
ssh user@server "python cli.py status"

# Remote monitoring
ssh user@server "python cli.py monitor"
```

### Mobile Integration

```bash
# Quick status check
python cli.py status --json

# Mobile-friendly output
python cli.py status --compact
```

## 🔄 Updates and Maintenance

### Check for Updates

```bash
# Check for new versions
python cli.py update --check

# Update to latest version
python cli.py update
```

### Maintenance Mode

```bash
# Enter maintenance mode
python cli.py maintenance --enable

# Perform maintenance tasks
python cli.py maintenance --clean-logs
python cli.py maintenance --optimize

# Exit maintenance mode
python cli.py maintenance --disable
```

## 📚 Advanced Usage

### Scripting and Automation

```bash
#!/bin/bash
# Example automation script

# Start services
python cli.py start

# Wait for services to be ready
sleep 10

# Verify connectivity
if python cli.py test --quiet; then
    echo "Services started successfully"
else
    echo "Service startup failed"
    python cli.py logs --level error
fi
```

### Integration with Other Tools

```bash
# Export status for monitoring tools
python cli.py status --json > status.json

# Pipe logs to log aggregation
python cli.py logs --follow | tee -a /var/log/warp-nextdns.log

# Use with system monitoring
python cli.py status --prometheus > /var/lib/prometheus/warp-nextdns.prom
```

---

**Next Steps**: [Configuration](configuration.md) | [Troubleshooting](troubleshooting.md) | [API Reference](api.md) 