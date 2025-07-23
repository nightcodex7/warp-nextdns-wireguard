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
  "elevated": true,
  "wgcf": {
    "wgcf_binary": true,
    "account_registered": true,
    "profile_generated": true,
    "profile_installed": true,
    "running": true
  },
  "nextdns": {
    "installed": true,
    "running": true,
    "configured": true
  },
  "timestamp": "2024-12-19T10:30:00"
}
```

### Detailed Status Information

```bash
# Verbose status with all details
python cli.py status --verbose

# Check specific components
python cli.py status --wgcf-only
python cli.py status --nextdns-only
```

## 🔄 Service Management

### Starting Services

```bash
# Start all services
python cli.py start

# Start with auto-elevation
python cli.py start --auto-elevate

# Start specific services
python cli.py start --wgcf-only
python cli.py start --nextdns-only
```

### Stopping Services

```bash
# Stop all services
python cli.py stop

# Stop specific services
python cli.py stop --wgcf-only
python cli.py stop --nextdns-only
```

### Service Status

```bash
# Check if services are running
python cli.py status

# View service logs
python cli.py logs

# Monitor services in real-time
python cli.py logs --follow
```

## 🧪 Connectivity Testing

### Basic Testing

```bash
# Test all connectivity
python cli.py test
```

Output example:
```json
{
  "internet": true,
  "warp": true,
  "nextdns": true
}
```

### Advanced Testing

```bash
# Test specific components
python cli.py test --warp-only
python cli.py test --nextdns-only
python cli.py test --internet-only

# Verbose testing with details
python cli.py test --verbose

# Continuous testing
python cli.py test --continuous --interval 30
```

## 📝 Logging and Debugging

### View Logs

```bash
# View recent logs
python cli.py logs

# View logs with specific number of lines
python cli.py logs --lines 100

# Follow logs in real-time
python cli.py logs --follow

# View logs for specific service
python cli.py logs --service wgcf
python cli.py logs --service nextdns
```

### Debug Mode

```bash
# Enable debug logging
python cli.py setup --debug
python cli.py start --debug
python cli.py test --debug
```

## 🔧 Configuration Management

### Manual Configuration

If you need to configure manually:

```bash
# Configure WGCF only
python cli.py setup --wgcf-only

# Configure NextDNS only
python cli.py setup --nextdns-only

# Update configuration
python cli.py setup --update-config
```

### Configuration Files

The tool creates these configuration files:

- **WGCF**: `/etc/wireguard/wgcf.conf`
- **NextDNS**: `/etc/nextdns.conf`
- **System Services**: `/etc/systemd/system/wgcf.service`, `/etc/systemd/system/nextdns.service`

### Backup and Restore

```bash
# Backup current configuration
python cli.py backup --output backup.tar.gz

# Restore from backup
python cli.py restore --input backup.tar.gz
```

## 🚀 Automation and Scripting

### Non-Interactive Usage

For automation and scripting:

```bash
# Non-interactive setup
python cli.py setup --non-interactive --profile-id YOUR_PROFILE_ID

# Non-interactive start/stop
python cli.py start --non-interactive
python cli.py stop --non-interactive

# JSON output for parsing
python cli.py status --json
python cli.py test --json
```

### Integration Examples

#### Systemd Service Integration
```bash
# Create systemd service
sudo systemctl enable warp-nextdns

# Start on boot
sudo systemctl start warp-nextdns

# Check status
sudo systemctl status warp-nextdns
```

#### Cron Job Integration
```bash
# Add to crontab for periodic testing
*/30 * * * * /usr/local/bin/warp-nextdns test --json > /var/log/warp-test.log
```

#### Monitoring Integration
```bash
# Health check script
#!/bin/bash
if ! python cli.py test --json | grep -q '"warp": true'; then
    echo "WARP is down, restarting..."
    python cli.py restart
fi
```

## 🔍 Troubleshooting Commands

### Diagnostic Commands

```bash
# Full system diagnostic
python cli.py diagnose

# Check network connectivity
python cli.py diagnose --network

# Check service health
python cli.py diagnose --services

# Generate diagnostic report
python cli.py diagnose --report diagnostic-report.txt
```

### Recovery Commands

```bash
# Reset configuration
python cli.py reset --config

# Reinstall components
python cli.py reinstall --wgcf
python cli.py reinstall --nextdns

# Full reset and reinstall
python cli.py reset --full
```

## 📱 Mobile and Remote Usage

### Remote Management

```bash
# Enable remote management
python cli.py setup --remote --port 8080

# Access web interface
# http://your-server:8080
```

### Mobile App Integration

The tool can be integrated with mobile apps through:

- **REST API**: JSON endpoints for status and control
- **WebSocket**: Real-time status updates
- **CLI**: Command-line interface for scripting

## 🔐 Security Considerations

### Privilege Management

```bash
# Run with minimal privileges
python cli.py setup --minimal-privileges

# Use specific user
python cli.py setup --user warp-user

# Secure configuration
python cli.py setup --secure-mode
```

### Network Security

```bash
# Configure firewall rules
python cli.py setup --configure-firewall

# Enable logging
python cli.py setup --enable-logging

# Set up monitoring
python cli.py setup --enable-monitoring
```

## 📚 Examples and Use Cases

### Basic Home Setup

```bash
# Simple home setup
python cli.py setup --profile-id YOUR_PROFILE_ID
python cli.py start
```

### Server Setup

```bash
# Server setup with monitoring
python cli.py setup --profile-id YOUR_PROFILE_ID --server-mode
python cli.py start --auto-start
```

### Development Environment

```bash
# Development setup
python cli.py setup --dev-mode --debug
python cli.py start --dev-mode
```

## 🔗 Integration with Other Tools

### Docker Integration

```dockerfile
FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "cli.py", "start"]
```

### Ansible Integration

```yaml
- name: Install WARP NextDNS Manager
  hosts: servers
  tasks:
    - name: Clone repository
      git:
        repo: https://github.com/nightcodex7/warp-nextdns-wireguard.git
        dest: /opt/warp-nextdns-wireguard
    
    - name: Run setup
      command: python cli.py setup --non-interactive --profile-id "{{ nextdns_profile_id }}"
      become: yes
```

## 📖 Next Steps

After learning the basics:

1. **[Configuration Guide](configuration.md)** - Advanced configuration options
2. **[Troubleshooting Guide](troubleshooting.md)** - Solve common issues
3. **[API Reference](api.md)** - Developer documentation

---

**Need help?** Check our [troubleshooting guide](troubleshooting.md) or [create an issue](https://github.com/nightcodex7/warp-nextdns-wireguard/issues). 