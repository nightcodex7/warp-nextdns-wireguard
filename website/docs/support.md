---
sidebar_position: 10
---

# Support

Need help with WARP NextDNS Manager? You're in the right place!

## Getting Help

### 📚 Documentation
Start with our comprehensive documentation:
- [Installation Guide](./installation)
- [Quick Start](./usage/quick-start)
- [Command Reference](./usage/commands)
- [Troubleshooting](./advanced/troubleshooting)

### 🐛 Report Issues
Found a bug or have a feature request?
1. Check [existing issues](https://github.com/nightcodex7/warp-nextdns-wireguard/issues)
2. [Create a new issue](https://github.com/nightcodex7/warp-nextdns-wireguard/issues/new)
3. Include:
   - System information (OS, version)
   - Steps to reproduce
   - Error messages or logs
   - Expected vs actual behavior

### 💬 Community
- **GitHub Discussions**: Coming soon!
- **Wiki**: Community-contributed guides and tips

## Frequently Asked Questions

### General Questions

**Q: Is this tool free to use?**
A: Yes! The tool is open source and free. You'll need free accounts with Cloudflare WARP and NextDNS.

**Q: Which operating systems are supported?**
A: Linux (Ubuntu, Debian, Fedora, Arch), Windows 10/11, and macOS 10.15+

**Q: Do I need technical knowledge to use this?**
A: Basic command-line familiarity helps, but the auto-setup mode handles most complexity.

### Installation Issues

**Q: The installer says "permission denied"**
A: The tool should auto-elevate. If not, run with `sudo` on Linux/macOS or as Administrator on Windows.

**Q: Can't download wgcf binary**
A: Check your internet connection and firewall. You may need to use a proxy or VPN to access GitHub.

**Q: NextDNS installation fails**
A: Ensure you have curl installed and can access `https://nextdns.io`

### Configuration Problems

**Q: Where do I find my NextDNS profile ID?**
A: Log into [NextDNS dashboard](https://my.nextdns.io), it's shown at the top of your configuration.

**Q: Can I use multiple NextDNS profiles?**
A: Currently, one profile at a time. You can reconfigure by running `setup` again.

**Q: How do I change WARP settings?**
A: WARP uses standard settings. For advanced configuration, edit `/etc/wireguard/wgcf.conf`

### Connection Issues

**Q: WARP shows as disconnected**
A: Run these checks:
```bash
# Check WireGuard interface
sudo wg show

# Restart services
./warp-nextdns-* stop
./warp-nextdns-* start

# Check logs
./warp-nextdns-* logs
```

**Q: DNS not working after setup**
A: Verify NextDNS is running:
```bash
# Check NextDNS status
nextdns status

# Test DNS resolution
dig @127.0.0.1 example.com
```

**Q: Slow internet after enabling**
A: This might be due to:
- WARP routing through distant servers
- NextDNS blocking many requests
- Network congestion

Try disabling and re-enabling to test.

## Contributing

Want to help improve WARP NextDNS Manager?

### Ways to Contribute
- 🐛 Report bugs
- 💡 Suggest features
- 📝 Improve documentation
- 🌍 Add translations
- 👨‍💻 Submit code changes

### Development Setup
See our [Development Guide](./advanced/development) for:
- Setting up development environment
- Code style guidelines
- Testing procedures
- Pull request process

## Contact

- **GitHub**: [@nightcodex7](https://github.com/nightcodex7)
- **Project**: [warp-nextdns-wireguard](https://github.com/nightcodex7/warp-nextdns-wireguard)

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](https://github.com/nightcodex7/warp-nextdns-wireguard/blob/main/LICENSE) file for details.