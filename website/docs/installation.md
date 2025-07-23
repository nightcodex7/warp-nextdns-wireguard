---
sidebar_position: 2
---

# Installation

This guide will help you install and set up WARP NextDNS Manager on your system.

## Prerequisites

Before installing, ensure you have:

- A supported operating system (Linux, Windows, or macOS)
- Administrative/root access
- An active internet connection
- A [NextDNS](https://nextdns.io) account with your profile ID

## Quick Install (Recommended)

### Download the Latest Release

1. Visit the [Releases page](https://github.com/nightcodex7/warp-nextdns-wireguard/releases)
2. Download the appropriate file for your system:
   - **Linux**: `warp-nextdns-vX.X.X-linux-amd64.tar.gz`
   - **Windows**: `warp-nextdns-vX.X.X-windows-amd64.zip`
   - **macOS**: `warp-nextdns-vX.X.X-darwin-amd64.tar.gz`

### Extract and Run

#### Linux/macOS
```bash
# Extract the archive
tar -xzf warp-nextdns-*.tar.gz
cd warp-nextdns-*

# Make executable
chmod +x warp-nextdns-*

# Run the setup (will auto-elevate)
./warp-nextdns-linux-amd64 setup --auto
```

#### Windows
1. Extract the ZIP file
2. Open Command Prompt as Administrator
3. Navigate to the extracted folder
4. Run:
```cmd
warp-nextdns-windows-amd64.exe setup --auto
```

## Manual Installation from Source

### Clone the Repository
```bash
git clone https://github.com/nightcodex7/warp-nextdns-wireguard.git
cd warp-nextdns-wireguard
```

### Install Python Dependencies
```bash
# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Setup
```bash
# The script will auto-elevate if needed
python main.py setup --auto
```

## Configuration

During setup, you'll need to provide:

1. **NextDNS Profile ID**: Found in your NextDNS dashboard (e.g., `abc123`)
2. **Installation options**: The tool will handle most settings automatically

### Environment Variables

You can pre-configure settings using environment variables:

```bash
export NEXTDNS_ID="your-profile-id"
```

## Verification

After installation, verify everything is working:

```bash
# Check status
./warp-nextdns-* status

# View logs
./warp-nextdns-* logs
```

You should see:
- ✅ WARP: Active
- ✅ NextDNS: Running
- ✅ WireGuard: Connected

## Auto-Start Configuration

The installer automatically configures your system to start services on boot:

- **Linux**: Uses systemd services
- **Windows**: Creates scheduled tasks
- **macOS**: Uses launchd

## Troubleshooting

If you encounter issues:

1. Run with verbose logging:
   ```bash
   ./warp-nextdns-* logs
   ```

2. Check service status:
   ```bash
   # Linux
   systemctl status wgcf-start
   systemctl status nextdns
   
   # Windows (as admin)
   sc query warp-nextdns
   ```

3. Restart services:
   ```bash
   ./warp-nextdns-* stop
   ./warp-nextdns-* start
   ```

## Next Steps

- Learn about [available commands](./usage/commands)
- Configure [advanced settings](./usage/configuration)
- Read [troubleshooting guide](./advanced/troubleshooting)