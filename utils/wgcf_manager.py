"""WGCF (WireGuard Cloudflare) manager for WARP setup."""
import os
import requests
import subprocess
from pathlib import Path
from typing import Optional, Dict
from .platform_utils import PlatformUtils


class WGCFManager:
    """Manage wgcf installation and configuration."""
    
    def __init__(self):
        self.platform = PlatformUtils()
        self.wgcf_path = Path("./wgcf")
        self.account_file = Path("wgcf-account.toml")
        self.profile_file = Path("wgcf-profile.conf")
        self.wireguard_dir = Path("/etc/wireguard")
        self.config_file = self.wireguard_dir / "wgcf.conf"
        
    def download_wgcf(self) -> bool:
        """Download the latest wgcf binary."""
        arch_map = {
            "x86_64": "amd64",
            "aarch64": "arm64",
            "armv7l": "armv7",
        }
        
        machine = self.platform.run_command(["uname", "-m"]).stdout.strip()
        arch = arch_map.get(machine, "amd64")
        
        url = f"https://github.com/ViRb3/wgcf/releases/latest/download/wgcf_{arch}"
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(self.wgcf_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Make executable
            self.wgcf_path.chmod(0o755)
            return True
            
        except Exception as e:
            raise RuntimeError(f"Failed to download wgcf: {e}")
    
    def register_account(self) -> bool:
        """Register a new WARP account."""
        if not self.wgcf_path.exists():
            raise RuntimeError("wgcf binary not found. Run download_wgcf() first.")
        
        try:
            self.platform.run_command([str(self.wgcf_path), "register"])
            return self.account_file.exists()
        except Exception as e:
            raise RuntimeError(f"Failed to register WARP account: {e}")
    
    def generate_profile(self) -> bool:
        """Generate WireGuard profile from account."""
        if not self.account_file.exists():
            raise RuntimeError("Account file not found. Run register_account() first.")
        
        try:
            self.platform.run_command([str(self.wgcf_path), "generate"])
            return self.profile_file.exists()
        except Exception as e:
            raise RuntimeError(f"Failed to generate profile: {e}")
    
    def modify_profile_for_nextdns(self) -> bool:
        """Modify WireGuard profile to use NextDNS."""
        if not self.profile_file.exists():
            raise RuntimeError("Profile file not found. Run generate_profile() first.")
        
        try:
            with open(self.profile_file, "r") as f:
                content = f.read()
            
            # Comment out Cloudflare DNS
            content = content.replace("DNS = 1.1.1.1", "#DNS = 1.1.1.1")
            content = content.replace("DNS = 1.0.0.1", "#DNS = 1.0.0.1")
            
            # Add NextDNS localhost
            if "#DNS = " in content and "DNS = 127.0.0.1" not in content:
                content = content.replace("#DNS = 1.1.1.1", "#DNS = 1.1.1.1\nDNS = 127.0.0.1")
            
            with open(self.profile_file, "w") as f:
                f.write(content)
            
            return True
            
        except Exception as e:
            raise RuntimeError(f"Failed to modify profile: {e}")
    
    def install_profile(self) -> bool:
        """Install WireGuard profile to system directory."""
        if not self.profile_file.exists():
            raise RuntimeError("Profile file not found.")
        
        if not self.platform.check_root_access():
            raise RuntimeError("Root access required to install profile.")
        
        try:
            # Create wireguard directory if it doesn't exist
            self.wireguard_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy profile to system directory
            self.platform.run_command([
                "cp", str(self.profile_file), str(self.config_file)
            ])
            
            # Secure the config file
            self.config_file.chmod(0o600)
            
            return True
            
        except Exception as e:
            raise RuntimeError(f"Failed to install profile: {e}")
    
    def is_installed(self) -> bool:
        """Check if wgcf profile is installed."""
        return self.config_file.exists()
    
    def get_status(self) -> Dict[str, bool]:
        """Get current status of wgcf setup."""
        return {
            "wgcf_binary": self.wgcf_path.exists(),
            "account_registered": self.account_file.exists(),
            "profile_generated": self.profile_file.exists(),
            "profile_installed": self.config_file.exists(),
        }