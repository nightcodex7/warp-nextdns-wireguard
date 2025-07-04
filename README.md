# WARP + NextDNS via WireGuard on Linux (Mint 22.1 Tested)

> **Project by** [@nightcodex7](https://github.com/nightcodex7)

---

## 🌐 Overview

This guide enables full Cloudflare WARP tunneling via WireGuard on Linux **with NextDNS integration** — giving you:

- 🔐 **Encrypted Internet traffic** through Cloudflare WARP  
- 🛡️ **Private, customizable DNS filtering** via your own [NextDNS](https://nextdns.io) profile  
- 📶 Works on Wi-Fi, Ethernet, and mobile tethering  
- ⚙️ Lightweight: No GUI needed, headless-friendly  

Tested and stable on **Linux Mint 22.1 (Ubuntu-based)**, but adaptable to most modern Linux distros.

---

## ⚠️ Prerequisites

Before starting this setup, make sure:

- You already have **NextDNS CLI installed and configured**
- Your `nextdns.conf` contains your **profile ID** and is working (test with `nextdns status`)
- You are using **Linux Mint 22.1** or another modern systemd-based Linux distro
- You have **basic terminal familiarity** and root/sudo access

---

## ❓ Why Use This

### ✅ WARP (Cloudflare)
- Free VPN-like tunnel over WireGuard  
- Encrypts traffic, bypasses basic firewalls, masks IP (somewhat)  
- Low latency, ideal for gaming or public Wi-Fi use

### ✅ NextDNS
- DNS-level ad/tracker blocking  
- Parental controls, analytics, and threat protection  
- Fully customizable from your NextDNS dashboard

### 💡 Combined Benefit

> You route traffic through Cloudflare’s WARP tunnel **while still resolving DNS via your own NextDNS profile** — best of both worlds.

---

## 🎯 Who This Is For

- Linux users (Mint, Ubuntu, Debian, Arch, etc.)
- Privacy-conscious users wanting more control
- Power users, developers, pentesters, students
- Anyone who wants **WARP + custom DNS** without relying on Cloudflare DNS

---

## 📋 Setup Instructions

### 🔧 1. Install & Register `wgcf`

```bash
sudo apt update
sudo apt install wireguard-tools curl
wget -O wgcf https://github.com/ViRb3/wgcf/releases/latest/download/wgcf_amd64
chmod +x wgcf
./wgcf register
./wgcf generate
```

➡️ This creates:

- `wgcf-account.toml`
- `wgcf-profile.conf`

---

### ✏️ 2. Edit the WireGuard Profile

The WireGuard config created by `wgcf` points to Cloudflare DNS by default.

Since we're using NextDNS instead, edit the config:

```bash
nano wgcf-profile.conf
```

Find and **comment out** the DNS line:

```ini
#DNS = 1.1.1.1
```

Or optionally, set it to:

```ini
DNS = 127.0.0.1
```

> ✅ This allows all DNS resolution to go through your already-configured `nextdns-cli` running locally.

---

### 📁 3. Move and Secure the Config

```bash
sudo mkdir -p /etc/wireguard
sudo cp wgcf-profile.conf /etc/wireguard/wgcf.conf
sudo chmod 600 /etc/wireguard/wgcf.conf
```

---

### 📦 4. Load WireGuard Kernel Module at Boot

```bash
echo wireguard | sudo tee /etc/modules-load.d/wireguard.conf
lsmod | grep wireguard  # confirm
```

---

### 🧩 5. Create a Boot-Safe systemd Wrapper

```bash
sudo nano /etc/systemd/system/wgcf-start.service
```

Paste:

```ini
[Unit]
Description=Safe WireGuard WARP Starter
After=network-online.target nextdns.service
Wants=network-online.target nextdns.service
ConditionPathExists=/etc/wireguard/wgcf.conf

[Service]
Type=oneshot
ExecStartPre=/sbin/modprobe wireguard
ExecStart=/usr/bin/systemctl start wg-quick@wgcf
ExecStartPost=/usr/bin/wg show wgcf
RemainAfterExit=true

[Install]
WantedBy=multi-user.target
```

---

### 🔄 6. Enable Services

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable wgcf-start
sudo systemctl disable wg-quick@wgcf  # prevent race condition
sudo systemctl enable nextdns
```

---

### 🔁 7. Reboot and Verify

```bash
sudo reboot
```

After reboot:

```bash
curl https://www.cloudflare.com/cdn-cgi/trace | grep warp
nextdns status
```

✅ Expected:

- `warp=on`
- running: NextDNS connected
- WireGuard handshake active

---

## 🙌 Credits

- [`wgcf`](https://github.com/ViRb3/wgcf) by [@ViRb3](https://github.com/ViRb3)
- [`nextdns`](https://nextdns.io)
- WireGuard project and Cloudflare
- Maintained by [@nightcodex7](https://github.com/nightcodex7)

---

## 📜 License

GNU General Public License v3
