# Troubleshooting Guide

> **Solve common issues with WARP + NextDNS Manager**

This guide helps you diagnose and resolve common problems with the WARP + NextDNS Manager.

## 🔍 Quick Diagnosis

### Check System Status

```bash
# Get overall status
python cli.py status

# Test connectivity
python cli.py test

# View recent logs
python cli.py logs
```

### Common Status Indicators

| Status | Meaning | Action |
|--------|---------|--------|
| ✅ All Green | Everything working | No action needed |
| ⚠️ Partial Issues | Some services down | Check specific services |
| ❌ All Red | Complete failure | Follow troubleshooting steps |

## 🚨 Common Issues

### 1. Permission Denied Errors

#### Symptoms
```bash
Error: Permission denied
Error: Root access required
Error: Elevated privileges needed
```

#### Solutions

**Linux/macOS:**
```bash
# Run with sudo
sudo python cli.py setup

# Or use auto-elevation
python cli.py setup --auto-elevate
```

**Windows:**
```powershell
# Run PowerShell as Administrator
# Then run:
python cli.py setup
```

**Check Permissions:**
```bash
# Verify file permissions
ls -la /etc/wireguard/wgcf.conf
ls -la /etc/nextdns.conf

# Fix permissions if needed
sudo chmod 600 /etc/wireguard/wgcf.conf
sudo chmod 644 /etc/nextdns.conf
```

### 2. WGCF Installation Failures

#### Symptoms
```bash
Error: Failed to download WGCF
Error: WGCF binary not found
Error: WGCF registration failed
```

#### Solutions

**Manual WGCF Installation:**
```bash
# Download WGCF manually
wget -O wgcf https://github.com/ViRb3/wgcf/releases/latest/download/wgcf_amd64
chmod +x wgcf

# Register manually
./wgcf register
./wgcf generate

# Then run setup
python cli.py setup
```

**Check Network Connectivity:**
```bash
# Test internet connection
curl -I https://github.com

# Test GitHub API
curl https://api.github.com/repos/ViRb3/wgcf/releases/latest
```

**Use Custom WGCF Path:**
```bash
python cli.py setup --wgcf-path /path/to/custom/wgcf
```

### 3. NextDNS Configuration Issues

#### Symptoms
```bash
Error: NextDNS not installed
Error: NextDNS configuration failed
Error: DNS resolution not working
```

#### Solutions

**Manual NextDNS Installation:**
```bash
# Install NextDNS manually
curl -sSL https://nextdns.io/install | sh

# Configure manually
nextdns install -config YOUR_PROFILE_ID

# Then run setup
python cli.py setup
```

**Check NextDNS Status:**
```bash
# Check if NextDNS is running
nextdns status

# Test DNS resolution
nslookup google.com 127.0.0.1

# Check NextDNS logs
nextdns log
```

**Reset NextDNS Configuration:**
```bash
# Remove existing config
sudo rm -f /etc/nextdns.conf

# Reinstall NextDNS
python cli.py setup --nextdns-only
```

### 4. Network Connectivity Issues

#### Symptoms
```bash
Error: No internet connection
Error: WARP tunnel not established
Error: DNS resolution failed
```

#### Solutions

**Check Network Interfaces:**
```bash
# List network interfaces
ip link show
ip addr show

# Check WireGuard interface
ip link show wgcf
ip addr show wgcf
```

**Test Network Connectivity:**
```bash
# Test basic connectivity
ping 1.1.1.1
ping 8.8.8.8

# Test DNS resolution
nslookup google.com
dig google.com

# Test WARP connectivity
curl https://www.cloudflare.com/cdn-cgi/trace
```

**Check Firewall Rules:**
```bash
# Linux iptables
sudo iptables -L -n | grep -E "(53|51820)"

# Windows firewall
netsh advfirewall firewall show rule name=all | findstr "WireGuard\|NextDNS"
```

### 5. Service Startup Failures

#### Symptoms
```bash
Error: Service failed to start
Error: systemctl start failed
Error: Service not found
```

#### Solutions

**Check Service Status:**
```bash
# Linux systemd
sudo systemctl status wgcf
sudo systemctl status nextdns

# View service logs
sudo journalctl -u wgcf -f
sudo journalctl -u nextdns -f
```

**Reload Systemd:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable wgcf
sudo systemctl enable nextdns
```

**Manual Service Start:**
```bash
# Start WireGuard manually
sudo wg-quick up wgcf

# Start NextDNS manually
sudo nextdns start
```

### 6. Configuration File Issues

#### Symptoms
```bash
Error: Configuration file not found
Error: Invalid configuration
Error: Configuration parse error
```

#### Solutions

**Check Configuration Files:**
```bash
# Verify files exist
ls -la /etc/wireguard/wgcf.conf
ls -la /etc/nextdns.conf

# Check file contents
sudo cat /etc/wireguard/wgcf.conf
sudo cat /etc/nextdns.conf
```

**Regenerate Configuration:**
```bash
# Regenerate WGCF config
python cli.py setup --regenerate-wgcf

# Regenerate NextDNS config
python cli.py setup --regenerate-nextdns

# Full reset
python cli.py setup --reset-config
```

**Validate Configuration:**
```bash
# Test WGCF config
sudo wg-quick up wgcf --dry-run

# Test NextDNS config
nextdns config --test
```

## 🔧 Advanced Troubleshooting

### Diagnostic Commands

```bash
# Full system diagnostic
python cli.py diagnose

# Network diagnostic
python cli.py diagnose --network

# Service diagnostic
python cli.py diagnose --services

# Generate diagnostic report
python cli.py diagnose --report diagnostic-report.txt
```

### Debug Mode

```bash
# Enable debug logging
python cli.py setup --debug
python cli.py start --debug
python cli.py test --debug

# View debug logs
python cli.py logs --debug
```

### Recovery Procedures

```bash
# Reset to factory defaults
python cli.py reset --full

# Reinstall components
python cli.py reinstall --wgcf
python cli.py reinstall --nextdns

# Backup and restore
python cli.py backup --output backup.tar.gz
python cli.py restore --input backup.tar.gz
```

## 📊 Platform-Specific Issues

### Linux Issues

#### Systemd Service Problems
```bash
# Check systemd status
sudo systemctl status wgcf
sudo systemctl status nextdns

# Enable services
sudo systemctl enable wgcf
sudo systemctl enable nextdns

# Start services
sudo systemctl start wgcf
sudo systemctl start nextdns
```

#### Kernel Module Issues
```bash
# Load WireGuard module
sudo modprobe wireguard

# Check if module is loaded
lsmod | grep wireguard

# Install WireGuard tools
sudo apt install wireguard-tools  # Ubuntu/Debian
sudo dnf install wireguard-tools  # Fedora
sudo pacman -S wireguard-tools    # Arch
```

#### Network Manager Conflicts
```bash
# Disable NetworkManager for WireGuard
sudo systemctl stop NetworkManager
sudo systemctl disable NetworkManager

# Or configure NetworkManager to ignore WireGuard
echo "unmanaged-devices=interface-name:wgcf" | sudo tee -a /etc/NetworkManager/conf.d/10-globally-managed-devices.conf
```

### Windows Issues

#### UAC Problems
```powershell
# Run as Administrator
Start-Process PowerShell -Verb RunAs

# Or use auto-elevation
python cli.py setup --auto-elevate
```

#### Windows Firewall
```powershell
# Allow WireGuard through firewall
New-NetFirewallRule -DisplayName "WARP WireGuard" -Direction Inbound -Protocol UDP -LocalPort 51820 -Action Allow

# Allow NextDNS through firewall
New-NetFirewallRule -DisplayName "NextDNS" -Direction Inbound -Protocol UDP -LocalPort 53 -Action Allow
```

#### Windows Service Issues
```powershell
# Check service status
Get-Service -Name "*WARP*"
Get-Service -Name "*NextDNS*"

# Start services manually
Start-Service -Name "WARPNextDNS"
```

### macOS Issues

#### Permission Issues
```bash
# Grant full disk access
# System Preferences > Security & Privacy > Privacy > Full Disk Access
# Add Terminal or your terminal app

# Grant network access
# System Preferences > Security & Privacy > Privacy > Network
# Add Terminal or your terminal app
```

#### Homebrew Issues
```bash
# Update Homebrew
brew update

# Install/update WireGuard tools
brew install wireguard-tools
brew upgrade wireguard-tools

# Check Homebrew status
brew doctor
```

#### Launchd Issues
```bash
# Check launchd services
launchctl list | grep warp
launchctl list | grep nextdns

# Load services manually
sudo launchctl load /Library/LaunchDaemons/com.warp-nextdns.manager.plist
```

## 🆘 Getting Help

### Before Asking for Help

1. **Check the logs**: `python cli.py logs`
2. **Run diagnostics**: `python cli.py diagnose`
3. **Test connectivity**: `python cli.py test`
4. **Check status**: `python cli.py status`

### Information to Include

When reporting issues, include:

- **Operating System**: Version and architecture
- **Python Version**: `python --version`
- **Error Messages**: Complete error output
- **Logs**: Relevant log entries
- **Steps to Reproduce**: Exact commands run
- **Expected vs Actual Behavior**: What you expected vs what happened

### Support Channels

1. **[GitHub Issues](https://github.com/nightcodex7/warp-nextdns-wireguard/issues)** - Bug reports and feature requests
2. **[GitHub Discussions](https://github.com/nightcodex7/warp-nextdns-wireguard/discussions)** - General questions and help
3. **[Documentation](https://nightcodex7.github.io/warp-nextdns-wireguard/)** - Complete documentation

### Creating a Good Issue Report

```markdown
## Issue Description
Brief description of the problem

## Steps to Reproduce
1. Run `python cli.py setup`
2. Enter profile ID
3. See error message

## Expected Behavior
What you expected to happen

## Actual Behavior
What actually happened

## System Information
- OS: Ubuntu 22.04 LTS
- Python: 3.11.0
- Architecture: x86_64

## Error Messages
```
Error: Permission denied
Traceback (most recent call last):
  File "cli.py", line 123, in <module>
    main()
```

## Logs
```
2024-12-19 10:30:00 - ERROR - Failed to start WGCF service
```

## Additional Information
Any other relevant information
```

## 📚 Related Documentation

- **[Installation Guide](installation.md)** - Installation instructions
- **[Usage Guide](usage.md)** - How to use the tool
- **[Configuration Guide](configuration.md)** - Advanced configuration
- **[API Reference](api.md)** - Developer documentation

---

**Still having issues?** [Create an issue](https://github.com/nightcodex7/warp-nextdns-wireguard/issues) with the information above. 