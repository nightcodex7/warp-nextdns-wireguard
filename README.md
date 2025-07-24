# WARP + NextDNS Manager

> **Enterprise-Grade Cloudflare WARP + NextDNS Integration**  
> **Project by** [@nightcodex7](https://github.com/nightcodex7)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0.0-orange.svg)](VERSION)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-lightgrey.svg)](https://github.com/nightcodex7/warp-nextdns-wireguard)
[![Buy Me a Coffee](https://img.shields.io/badge/☕-Buy%20Me%20a%20Coffee-orange?style=for-the-badge)](https://buymeacoffee.com/nightcode)
[![Ko-fi](https://img.shields.io/badge/💙-Support%20on%20Ko--fi-blue?style=for-the-badge)](https://ko-fi.com/nightcode)

---

## 🌟 Overview

**WARP + NextDNS Manager** is a comprehensive, enterprise-grade CLI application that enables full Cloudflare WARP tunneling via WireGuard **with advanced NextDNS integration** — providing you with:

- 🔐 **Encrypted Internet traffic** through Cloudflare WARP  
- 🛡️ **Private, customizable DNS filtering** via your own [NextDNS](https://nextdns.io) profile  
- 📶 **Cross-platform support**: Linux, Windows (macOS not supported)
- 💻 **Rich CLI interface** with dynamic status updates
- 🎯 **Enterprise features**: Advanced monitoring, backup, and security
- 🛠️ **Comprehensive error handling** with automatic recovery
- 📊 **Real-time status monitoring** and detailed logging
- 🔧 **Automated setup and configuration**

### 🎯 Perfect For

- **Privacy-conscious users** wanting more control over their internet traffic
- **Power users, developers, and system administrators**
- **Organizations** requiring secure, monitored network access
- **Anyone** who wants **WARP + custom DNS** without relying on Cloudflare DNS

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/nightcodex7/warp-nextdns-wireguard.git
cd warp-nextdns-wireguard

# Choose your branch
git checkout testing  # For development/testing (latest features)
# OR
git checkout main     # For stable releases

# Install dependencies
pip install -r requirements.txt

# Run the CLI
python cli.py
```

### 🌿 Branching Strategy

This project uses a **testing→main** workflow:

- **`testing`**: Development branch with latest features and documentation
- **`main`**: Stable production releases only
- **Documentation**: Automatically deployed from `testing` branch to GitHub Pages

For detailed information, see [BRANCHING_STRATEGY.md](BRANCHING_STRATEGY.md).

### Basic Usage

```bash
# Interactive setup (recommended for first-time users)
python cli.py setup

# Check system status
python cli.py status

# Live status monitoring
python cli.py logs

# Individual commands
python cli.py install
python cli.py start
python cli.py stop
python cli.py test
```

### 🌐 Website Documentation

Visit our [modern documentation website](https://nightcodex7.github.io/warp-nextdns-wireguard/) for:
- **Interactive installation guides** with platform-specific instructions
- **Live terminal demos** showing the application in action
- **Comprehensive feature documentation**
- **Troubleshooting guides** and FAQs

---

## 🎨 Features

### 💻 Command Line Interface
- **Interactive mode** with guided setup and menu-driven interface
- **Live status monitoring** with dynamic updates
- **Individual commands** for automation and scripting
- **JSON output** for integration with other tools
- **Rich terminal interface** with progress indicators and tables
- **Comprehensive error handling** with recovery suggestions
- **Real-time network diagnostics** and speed testing
- **Security reporting** and backup management

### 🛠️ System Management
- **Automatic tool detection** and installation
- **Service management** with start/stop capabilities
- **Configuration backup and restore**
- **Network monitoring** with performance metrics
- **Security validation** and certificate management
- **Log management** with filtering and analysis

### 🔧 Core Functionality
- **WARP registration** and WireGuard configuration
- **NextDNS integration** with custom profiles
- **Cross-platform compatibility** (Linux, Windows only - macOS not supported)
- **Real-time status updates** with live monitoring
- **Error recovery** and automatic retry mechanisms
- **Comprehensive logging** and debugging support

---

## 📋 Commands

### Main Commands

| Command | Description |
|---------|-------------|
| `status` | Show current system status |
| `setup` | Interactive setup wizard |
| `install` | Install WARP + NextDNS services |
| `start` | Start WARP and NextDNS services |
| `stop` | Stop WARP and NextDNS services |
| `logs` | View application logs |
| `test` | Run connection and leak tests |
| `version` | Display version information |

### Setup Wizard Features

The setup wizard provides a comprehensive guided process with:

1. **System Detection** - Automatic platform and tool detection
2. **WARP Registration** - Cloudflare WARP account setup
3. **NextDNS Configuration** - DNS profile configuration
4. **Service Installation** - Automatic service setup
5. **Configuration Backup** - Secure backup creation
6. **Testing & Validation** - Connection and leak testing
7. **Status Monitoring** - Real-time service monitoring

### Options

| Option | Description |
|--------|-------------|
| `--json` | Output in JSON format |
| `--verbose` | Verbose output |
| `--refresh <seconds>` | Refresh interval for monitor mode |

---

## 🛠️ Installation

### Prerequisites

- **Python 3.8+**
- **Administrator/root privileges** (for service management)
- **Internet connection** (for initial setup)

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/nightcodex7/warp-nextdns-wireguard.git
   cd warp-nextdns-wireguard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run setup wizard**
   ```bash
   python cli.py setup
   ```

4. **Follow the setup wizard**
   - Automatic platform detection
   - WARP registration and configuration
   - NextDNS profile setup
   - Service installation and testing

---

## 🔧 Configuration

### WARP Configuration

The application automatically handles:
- **wgcf installation** and setup
- **WARP registration** with Cloudflare
- **WireGuard configuration** generation
- **Service management** and monitoring

### NextDNS Configuration

NextDNS integration provides:
- **Custom DNS filtering** rules
- **Privacy protection** and ad blocking
- **Performance optimization**
- **Real-time statistics** and monitoring

### Backup and Recovery

The application includes:
- **Automatic backup** creation
- **Configuration versioning**
- **One-click restore** functionality
- **Backup verification** and validation

---

## 📊 Monitoring

### Live Status Monitoring

```bash
# View real-time logs
python cli.py logs

# Check current status
python cli.py status

# Run connection tests
python cli.py test
```

### Status Information

The status command provides:
- **System information** (platform, architecture, Python version)
- **Service status** (WARP, NextDNS active/inactive)
- **Tool availability** (wgcf, wg, nextdns)
- **Network status** (internet connectivity, WARP IP, DNS servers)

### Network Diagnostics

```bash
# Run connection tests
python cli.py test

# Check system status
python cli.py status
```

---

## 🔒 Security

### Security Features

- **Encryption key management** with secure storage
- **SSL certificate validation** and management
- **File permission** security checks
- **Secure backup** creation and storage
- **Error logging** with sensitive data protection

### Security Reports

```bash
# Run security tests
python cli.py test

# Check system status
python cli.py status
```

---

## 📝 Logging

### Log Management

The application maintains comprehensive logs:
- **Application logs** with detailed error information
- **Service logs** for WARP and NextDNS
- **Security logs** for access and permission events
- **Network logs** for connectivity and performance

### Viewing Logs

```bash
# View recent logs
python cli.py logs

# Check system status
python cli.py status
```

---

## 🚨 Troubleshooting

### Common Issues

1. **Permission Errors**
   - Ensure you're running with administrator/root privileges
   - Check file permissions in the configuration directory

2. **Network Connectivity**
   - Verify internet connection
   - Check firewall settings
   - Ensure DNS resolution is working

3. **Service Failures**
   - Check service logs for detailed error information
   - Verify tool installation (wgcf, wg, nextdns)
   - Ensure proper configuration files exist

### Getting Help

1. **Check the logs**
   ```bash
   python main.py logs
   ```

2. **Run diagnostics**
   ```bash
   python cli.py test
   ```

3. **Verify installation**
   ```bash
   python cli.py status
   ```

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/nightcodex7/warp-nextdns-wireguard.git
cd warp-nextdns-wireguard

# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Run linting
python -m flake8 .
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Cloudflare** for WARP and WireGuard integration
- **NextDNS** for DNS filtering and privacy features
- **Python community** for excellent libraries and tools
- **Contributors** who help improve this project

---

## 📞 Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/nightcodex7/warp-nextdns-wireguard/issues)
- **Documentation**: [Wiki and guides](https://github.com/nightcodex7/warp-nextdns-wireguard/wiki)
- **Discussions**: [Community discussions](https://github.com/nightcodex7/warp-nextdns-wireguard/discussions)

---

**Made with ❤️ by [@nightcodex7](https://github.com/nightcodex7)**

