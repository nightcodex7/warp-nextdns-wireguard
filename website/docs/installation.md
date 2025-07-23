---
sidebar_position: 2
---

# Installation

This guide will help you install WARP + NextDNS Manager on your system.

## Prerequisites

Before installing, ensure you have:

- **Python 3.8 or higher**
- **Administrator/root privileges** (for installation)
- **Internet connection** (for downloading dependencies)
- **Git** (for cloning the repository)

### System Requirements

- **Linux**: Ubuntu 18.04+, Debian 10+, CentOS 8+, Fedora 30+, Arch Linux
- **Windows**: Windows 10/11 (64-bit)
- **macOS**: 10.15+ (Catalina and newer)

## Quick Installation

### Option 1: Web Interface (Recommended)

```bash
# Clone the repository
git clone https://github.com/nightcodex7/warp-nextdns-wireguard.git
cd warp-nextdns-wireguard

# Install dependencies
pip install -r requirements.txt
pip install -r requirements_enhanced.txt

# Run the web interface
python app.py
```

Then open your browser to `http://localhost:5000`

### Option 2: Enterprise GUI

```bash
# Install and run the enterprise GUI
python gui_enterprise.py
```

### Option 3: Command Line Interface

```bash
# Run interactive setup
python cli.py interactive
```

## Detailed Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/nightcodex7/warp-nextdns-wireguard.git
cd warp-nextdns-wireguard
```

### Step 2: Install Python Dependencies

```bash
# Install basic dependencies
pip install -r requirements.txt

# Install enhanced dependencies (recommended)
pip install -r requirements_enhanced.txt
```

### Step 3: Run the Application

Choose your preferred interface:

#### Web Interface
```bash
python app.py
```

#### Enterprise GUI
```bash
python gui_enterprise.py
```

#### CLI Interface
```bash
python cli.py interactive
```

## Platform-Specific Instructions

### Linux Installation

#### Ubuntu/Debian
```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip python3-venv

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements_enhanced.txt
```

#### CentOS/RHEL/Fedora
```bash
# Install Python and pip
sudo dnf install python3 python3-pip python3-venv

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements_enhanced.txt
```

#### Arch Linux
```bash
# Install Python and pip
sudo pacman -S python python-pip

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements_enhanced.txt
```

### Windows Installation

#### Using Python from python.org
1. Download Python 3.8+ from [python.org](https://python.org)
2. Install with "Add to PATH" option checked
3. Open Command Prompt or PowerShell
4. Run the installation commands:

```cmd
git clone https://github.com/nightcodex7/warp-nextdns-wireguard.git
cd warp-nextdns-wireguard
pip install -r requirements.txt
pip install -r requirements_enhanced.txt
python app.py
```

#### Using WSL2 (Recommended)
```bash
# Install WSL2 with Ubuntu
wsl --install

# Follow Linux installation instructions above
```

### macOS Installation

#### Using Homebrew
```bash
# Install Python
brew install python

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements_enhanced.txt
```

#### Using Python.org
1. Download Python 3.8+ from [python.org](https://python.org)
2. Install the package
3. Open Terminal and run:

```bash
git clone https://github.com/nightcodex7/warp-nextdns-wireguard.git
cd warp-nextdns-wireguard
pip3 install -r requirements.txt
pip3 install -r requirements_enhanced.txt
python3 app.py
```

## Verification

After installation, verify everything is working:

```bash
# Check Python version
python --version

# Check if dependencies are installed
python -c "import flask, psutil, requests; print('Dependencies OK')"

# Run a quick test
python cli.py status
```

## Troubleshooting

### Common Issues

#### Permission Denied
```bash
# On Linux/macOS, ensure you have proper permissions
sudo chmod +x *.py
```

#### Python Not Found
```bash
# Ensure Python is in your PATH
which python
python --version
```

#### Dependencies Installation Failed
```bash
# Try upgrading pip
pip install --upgrade pip

# Install with verbose output
pip install -v -r requirements.txt
```

#### Port Already in Use
```bash
# Check what's using port 5000
lsof -i :5000  # Linux/macOS
netstat -an | findstr :5000  # Windows

# Kill the process or use a different port
python app.py --port 5001
```

### Getting Help

If you encounter issues:

1. **Check the logs**: Look for error messages in the console
2. **Verify prerequisites**: Ensure all requirements are met
3. **Search issues**: Check [GitHub Issues](https://github.com/nightcodex7/warp-nextdns-wireguard/issues)
4. **Ask for help**: Use [GitHub Discussions](https://github.com/nightcodex7/warp-nextdns-wireguard/discussions)

## Next Steps

After successful installation:

1. **Configure NextDNS**: Set up your NextDNS profile
2. **Setup WARP**: Configure Cloudflare WARP tunneling
3. **Test the setup**: Verify everything is working
4. **Explore features**: Try different interfaces and features

See the [Configuration Guide](configuration.md) for detailed setup instructions. 