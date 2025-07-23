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
# Enable execution policy (if needed)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install Python (if not already installed)
winget install Python.Python.3.11

# Clone and setup
git clone https://github.com/nightcodex7/warp-nextdns-wireguard.git
cd warp-nextdns-wireguard
python cli.py setup
```

#### Using Command Prompt
```cmd
# Install Python (if not already installed)
winget install Python.Python.3.11

# Clone and setup
git clone https://github.com/nightcodex7/warp-nextdns-wireguard.git
cd warp-nextdns-wireguard
python cli.py setup
```

### macOS Installation

#### Using Homebrew (Recommended)
```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python

# Clone and setup
git clone https://github.com/nightcodex7/warp-nextdns-wireguard.git
cd warp-nextdns-wireguard
python3 cli.py setup
```

#### Using MacPorts
```bash
# Install Python
sudo port install python311

# Clone and setup
git clone https://github.com/nightcodex7/warp-nextdns-wireguard.git
cd warp-nextdns-wireguard
python3 cli.py setup
```

## 🔧 Setup Process

### 1. Initial Setup

The setup process will guide you through:

1. **System detection** - Automatically detects your OS and architecture
2. **Dependency installation** - Installs required tools (wgcf, WireGuard, NextDNS)
3. **WARP registration** - Creates WARP account and generates WireGuard config
4. **NextDNS configuration** - Sets up DNS filtering with your profile
5. **Service creation** - Creates system services for automatic startup

### 2. Interactive Setup

```bash
python cli.py setup
```

You'll be prompted for:
- **NextDNS Profile ID** - Your NextDNS profile identifier
- **Auto-elevation** - Whether to automatically handle privilege escalation
- **Service creation** - Whether to create system services

### 3. Non-Interactive Setup

```bash
python cli.py setup --non-interactive --profile-id YOUR_PROFILE_ID
```

Perfect for automation and scripting.

## 🔐 NextDNS Configuration

### Getting Your Profile ID

1. **Sign up** at [NextDNS.io](https://nextdns.io)
2. **Create a profile** in your dashboard
3. **Copy the profile ID** from the profile settings

### Profile ID Format

Your NextDNS profile ID looks like: `abc123` or `def456-ghi789`

## 🚨 Troubleshooting Installation

### Common Issues

#### Permission Errors
```bash
# Linux/macOS - Ensure elevated privileges
sudo python3 cli.py setup

# Windows - Run as Administrator
# Right-click PowerShell/CMD and select "Run as Administrator"
```

#### Python Version Issues
```bash
# Check Python version
python --version
python3 --version

# Install specific version if needed
# Ubuntu/Debian
sudo apt install python3.11

# macOS
brew install python@3.11
```

#### Network Connectivity
```bash
# Test internet connection
ping 1.1.1.1

# Test DNS resolution
nslookup google.com
```

#### Dependency Installation Failures
```bash
# Update package lists
sudo apt update  # Ubuntu/Debian
sudo dnf update  # Fedora
brew update      # macOS

# Retry installation
python cli.py setup
```

## ✅ Verification

After installation, verify everything is working:

```bash
# Check status
python cli.py status

# Test connection
python cli.py test

# View logs
python cli.py logs
```

## 🔄 Updating

To update to the latest version:

```bash
# Pull latest changes
git pull origin main

# Reinstall dependencies
pip install -r requirements.txt

# Restart services
python cli.py restart
```

## 🗑️ Uninstallation

To completely remove WARP + NextDNS Manager:

```bash
# Stop services
python cli.py stop

# Uninstall
python cli.py uninstall

# Remove configuration files
rm -rf ~/.warp-nextdns
```

## 📞 Support

If you encounter issues during installation:

1. **Check the logs**: `python cli.py logs`
2. **Run diagnostics**: `python cli.py test`
3. **Review this guide** for common solutions
4. **Open an issue** on GitHub with detailed information

---

**Next Steps**: [Usage Guide](usage.md) | [Configuration](configuration.md) | [Troubleshooting](troubleshooting.md) 