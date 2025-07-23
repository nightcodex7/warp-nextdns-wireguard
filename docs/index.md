# WARP + NextDNS Manager

> **Secure internet with Cloudflare WARP and NextDNS**

A powerful, cross-platform tool that combines Cloudflare WARP's encrypted tunneling with NextDNS's customizable DNS filtering for maximum privacy and security.

## 🌟 Features

- **🔐 Encrypted Internet Traffic** - All traffic routed through Cloudflare WARP
- **🛡️ Custom DNS Filtering** - NextDNS integration for ad/tracker blocking
- **⚡ Automatic Setup** - One-command installation and configuration
- **🔄 Cross-Platform** - Works on Linux, Windows, and macOS
- **🚀 Auto-Start** - Automatic service management and boot-time startup
- **📊 Real-time Monitoring** - Live status and connection testing

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Elevated privileges (sudo/admin)
- Internet connection
- NextDNS profile ID

### Installation

```bash
# Clone the repository
git clone https://github.com/nightcodex7/warp-nextdns-wireguard.git
cd warp-nextdns-wireguard

# Install dependencies
pip install -r requirements.txt

# Run setup
python cli.py setup
```

### Usage

```bash
# Interactive setup
python cli.py setup

# Check status
python cli.py status

# Start services
python cli.py start

# Stop services
python cli.py stop

# Test connectivity
python cli.py test

# View logs
python cli.py logs
```

## 📋 System Requirements

| Platform | Requirements |
|----------|-------------|
| **Linux** | Ubuntu 18.04+, Debian 10+, Fedora 30+, Arch Linux |
| **Windows** | Windows 10/11 (64-bit) |
| **macOS** | macOS 10.15+ |

## 🔧 Configuration

The tool automatically handles:

- ✅ WGCF installation and WARP registration
- ✅ WireGuard configuration
- ✅ NextDNS CLI installation and setup
- ✅ System service creation
- ✅ Auto-start configuration
- ✅ Network interface management

## 📊 What You Get

After setup, your internet traffic flows like this:

```
Your Device → WARP Tunnel → Cloudflare → Internet
                ↓
            NextDNS Filtering
```

This provides:

- **Privacy**: Your IP is masked through Cloudflare's network
- **Security**: All traffic is encrypted end-to-end
- **Filtering**: DNS-level ad/tracker blocking via NextDNS
- **Performance**: Low-latency routing through Cloudflare's global network

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](contributing.md) for details.

## 📄 License

This project is licensed under the GNU General Public License v3 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [WGCF](https://github.com/ViRb3/wgcf) by [@ViRb3](https://github.com/ViRb3)
- [NextDNS](https://nextdns.io) for DNS filtering
- [WireGuard](https://www.wireguard.com/) for VPN tunneling
- [Cloudflare](https://www.cloudflare.com/) for WARP service

---

**Made with ❤️ by [@nightcodex7](https://github.com/nightcodex7)** 