# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-09

### Added
- Initial release of WARP NextDNS WireGuard Manager.
- Automatic elevation of privileges for installation.
- Cross-platform support (Linux, Windows, macOS).
- Intelligent OS and architecture detection.
- Automatic handling of compressed downloads.
- Enhanced navigation with auto-response capabilities.
- Comprehensive error handling and recovery.
- One-click setup with `--auto` flag.
- Service management (start, stop, status).
- Configuration backup and restore.
- Detailed logging and diagnostics.
- Beautiful CLI interface with Rich library.
- GitHub Actions for automated releases.
- Documentation website with Docusaurus.

### Features
- **WARP Integration**: Seamless Cloudflare WARP setup via WireGuard.
- **NextDNS Support**: Custom DNS filtering with your NextDNS profile.
- **Auto-Start**: System service configuration for boot persistence.
- **Multi-Platform**: Native support for major operating systems.
- **User-Friendly**: Interactive menus and automated workflows.

### Security
- Automatic privilege elevation without storing credentials.
- Secure configuration file permissions (600).
- No hardcoded sensitive data.
- Safe handling of system services.

### Technical Details
- Built with Python 3.8+.
- Uses PyInstaller for standalone executables.
- Implements systemd on Linux for service management.
- Windows Task Scheduler integration.
- macOS launchd support.

---

For more information, visit the [project repository](https://github.com/nightcodex7/warp-nextdns-wireguard).
