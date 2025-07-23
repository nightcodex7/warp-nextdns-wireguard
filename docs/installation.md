# Installation Guide

> **Complete installation guide for WARP + NextDNS Manager**

This guide covers installation on all supported platforms with step-by-step instructions.

## 📋 Prerequisites

Before installing, ensure your system meets these requirements:

### System Requirements

| Platform | Minimum Version | Architecture | Notes |
|----------|----------------|--------------|-------|
| **Linux** | Ubuntu 18.04+ | x86_64, ARM64 | Most distributions supported |
| **Windows** | Windows 10/11 | x86_64 | 64-bit only |
| **macOS** | macOS 10.15+ | x86_64, ARM64 | Intel and Apple Silicon |

### Software Requirements

- **Python**: 3.7 or higher
- **Internet Connection**: Required for downloads and configuration
- **Elevated Privileges**: Admin/root access for installation
- **NextDNS Profile**: Active NextDNS account with profile ID

## 🚀 Quick Installation

### Option 1: Using the Executable (Recommended)

1. **Download the executable** for your platform from the [releases page](https://github.com/nightcodex7/warp-nextdns-wireguard/releases)

2. **Run with elevated privileges**:
   ```bash
   # Linux/macOS
   sudo ./warp-nextdns setup
   
   # Windows (Run as Administrator)
   warp-nextdns.exe setup
   ```

3. **Follow the setup wizard** and enter your NextDNS profile ID when prompted

### Option 2: From Source

```bash
# Clone the repository
git clone https://github.com/nightcodex7/warp-nextdns-wireguard.git
cd warp-nextdns-wireguard

# Install dependencies
pip install -r requirements.txt

# Run setup
python cli.py setup
```

## 📦 Platform-Specific Installation

### Linux Installation

#### Ubuntu/Debian
```bash
# Update package list
sudo apt update

# Install Python dependencies
sudo apt install python3 python3-pip python3-venv

# Clone and setup
git clone https://github.com/nightcodex7/warp-nextdns-wireguard.git
cd warp-nextdns-wireguard
python3 cli.py setup
```

#### Fedora/CentOS/RHEL
```bash
# Install Python dependencies
sudo dnf install python3 python3-pip

# Clone and setup
git clone https://github.com/nightcodex7/warp-nextdns-wireguard.git
cd warp-nextdns-wireguard
python3 cli.py setup
```

#### Arch Linux
```bash
# Install Python dependencies
sudo pacman -S python python-pip

# Clone and setup
git clone https://github.com/nightcodex7/warp-nextdns-wireguard.git
cd warp-nextdns-wireguard
python cli.py setup
```

### Windows Installation

#### Using PowerShell (Recommended)
```powershell
# Install Python from Microsoft Store or python.org
# Clone the repository
git clone https://github.com/nightcodex7/warp-nextdns-wireguard.git
cd warp-nextdns-wireguard

# Run as Administrator
python cli.py setup
```

#### Using Command Prompt
```cmd
# Install Python from python.org
# Clone the repository
git clone https://github.com/nightcodex7/warp-nextdns-wireguard.git
cd warp-nextdns-wireguard

# Run as Administrator
python cli.py setup
```

### macOS Installation

#### Using Homebrew (Recommended)
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python

# Clone and setup
git clone https://github.com/nightcodex7/warp-nextdns-wireguard.git
cd warp-nextdns-wireguard
python3 cli.py setup
```

#### Using Python.org
```bash
# Download Python from python.org
# Clone the repository
git clone https://github.com/nightcodex7/warp-nextdns-wireguard.git
cd warp-nextdns-wireguard
python3 cli.py setup
```

## 🔧 Installation Process

The installation process automatically handles:

1. **System Detection**: Identifies your OS and architecture
2. **Dependency Installation**: Installs required system packages
3. **WGCF Setup**: Downloads and configures WGCF for WARP
4. **NextDNS Configuration**: Sets up NextDNS CLI and configuration
5. **Service Creation**: Creates system services for auto-start
6. **Network Configuration**: Configures WireGuard interfaces
7. **Testing**: Verifies the installation and connectivity

### What Gets Installed

- **WGCF**: WireGuard Cloudflare client for WARP
- **NextDNS CLI**: NextDNS command-line interface
- **WireGuard Tools**: System WireGuard utilities
- **System Services**: Auto-start services for Linux/Windows/macOS
- **Configuration Files**: WARP and NextDNS configuration

## ✅ Verification

After installation, verify everything is working:

```bash
# Check status
python cli.py status

# Test connectivity
python cli.py test

# View logs
python cli.py logs
```

Expected output:
```json
{
  "warp": true,
  "nextdns": true,
  "internet": true
}
```

## 🔄 Updating

To update to the latest version:

```bash
# Pull latest changes
git pull origin testing

# Reinstall dependencies
pip install -r requirements.txt

# Restart services
python cli.py stop
python cli.py start
```

## 🗑️ Uninstallation

To completely remove the installation:

```bash
# Stop services
python cli.py stop

# Remove configuration
sudo rm -rf /etc/wireguard/wgcf.conf
sudo rm -rf /etc/nextdns.conf

# Remove system services
sudo systemctl disable wgcf
sudo systemctl disable nextdns

# Remove from package manager (if installed)
# Linux: sudo apt remove wireguard-tools
# macOS: brew uninstall wireguard-tools
```

## 🆘 Troubleshooting

### Common Issues

#### Permission Denied
```bash
# Ensure you're running with elevated privileges
sudo python cli.py setup
```

#### Python Not Found
```bash
# Install Python first
# Ubuntu/Debian: sudo apt install python3
# Fedora: sudo dnf install python3
# macOS: brew install python
```

#### Network Issues
```bash
# Check firewall settings
# Ensure ports 53 (DNS) and 51820 (WireGuard) are open
```

#### Service Failures
```bash
# Check service status
sudo systemctl status wgcf
sudo systemctl status nextdns

# View detailed logs
sudo journalctl -u wgcf -f
sudo journalctl -u nextdns -f
```

### Getting Help

If you encounter issues:

1. **Check the logs**: `python cli.py logs`
2. **Review troubleshooting guide**: [Troubleshooting](troubleshooting.md)
3. **Search existing issues**: [GitHub Issues](https://github.com/nightcodex7/warp-nextdns-wireguard/issues)
4. **Create a new issue**: Include system information and error logs

## 📚 Next Steps

After successful installation:

1. **[Usage Guide](usage.md)** - Learn how to use the tool
2. **[Configuration](configuration.md)** - Advanced configuration options
3. **[Troubleshooting](troubleshooting.md)** - Solve common issues

---

**Need help?** Check our [troubleshooting guide](troubleshooting.md) or [create an issue](https://github.com/nightcodex7/warp-nextdns-wireguard/issues). 