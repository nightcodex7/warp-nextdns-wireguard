"""Core module for WARP NextDNS WireGuard Manager."""
import os
import sys
import subprocess
import time
from pathlib import Path
from typing import Dict, Optional, List
from rich.console import Console
from rich.panel import Panel

from utils.platform_utils import PlatformUtils
from utils.installer_manager import InstallerManager
from utils.wgcf_manager import WGCFManager
from utils.nextdns_manager import NextDNSManager
from utils.navigation_manager import NavigationManager


class WarpNextDNSManager:
    """Main application class for managing WARP + NextDNS setup."""
    
    def __init__(self, auto_mode: bool = False):
        self.platform = PlatformUtils()
        self.installer = InstallerManager()
        self.wgcf = WGCFManager()
        self.nextdns = NextDNSManager()
        self.nav = NavigationManager(auto_mode=auto_mode)
        self.console = Console()
        
        # Auto elevate on initialization
        if not self.platform.check_root_access():
            self.installer.auto_elevate()
    
    def check_prerequisites(self) -> Dict[str, bool]:
        """Check all prerequisites."""
        return {
            "root_access": self.platform.check_root_access(),
            "wireguard_installed": self.platform.command_exists("wg"),
            "curl_installed": self.platform.command_exists("curl"),
            "nextdns_installed": self.nextdns.is_installed(),
            "systemd_available": self.platform.is_linux and Path("/run/systemd/system").exists(),
        }
    
    def install_prerequisites(self) -> bool:
        """Install missing prerequisites."""
        prereqs = self.check_prerequisites()
        
        steps = []
        
        if not prereqs["root_access"]:
            self.console.print("[red]Root access required. Please run with sudo or as administrator.[/red]")
            return False
        
        if not prereqs["wireguard_installed"] or not prereqs["curl_installed"]:
            steps.append({
                "name": "Install WireGuard and tools",
                "action": self.installer.install_wireguard_tools
            })
        
        if not prereqs["nextdns_installed"]:
            steps.append({
                "name": "Install NextDNS",
                "action": self.nextdns.install
            })
        
        if steps:
            return self.nav.display_progress("Installing prerequisites", steps)
        
        return True
    
    def setup_warp(self) -> bool:
        """Complete WARP setup process."""
        steps = [
            {
                "name": "Download wgcf binary",
                "action": self.wgcf.download_wgcf
            },
            {
                "name": "Register WARP account",
                "action": self.wgcf.register_account
            },
            {
                "name": "Generate WireGuard profile",
                "action": self.wgcf.generate_profile
            },
            {
                "name": "Modify profile for NextDNS",
                "action": self.wgcf.modify_profile_for_nextdns
            },
            {
                "name": "Install profile to system",
                "action": self.wgcf.install_profile
            }
        ]
        
        return self.nav.display_progress("Setting up WARP", steps)
    
    def configure_nextdns(self) -> bool:
        """Configure NextDNS."""
        if not self.nextdns.is_installed():
            self.console.print("[red]NextDNS is not installed.[/red]")
            return False
        
        # Check if already configured
        if self.nextdns.is_configured():
            if not self.nav.auto_confirm("NextDNS is already configured. Reconfigure?", default=False):
                return True
        
        # Get profile ID
        profile_id = self.nav.auto_prompt(
            "Enter your NextDNS profile ID (e.g., abc123)",
            default=os.environ.get("NEXTDNS_ID", "")
        )
        
        if not profile_id:
            self.console.print("[red]Profile ID is required.[/red]")
            return False
        
        # Configure NextDNS
        try:
            self.nextdns.configure(profile_id, "-listen :53 -report-client-info")
            self.console.print("[green]NextDNS configured successfully.[/green]")
            return True
        except Exception as e:
            self.console.print(f"[red]Failed to configure NextDNS: {e}[/red]")
            return False
    
    def setup_systemd_services(self) -> bool:
        """Setup systemd services for auto-start."""
        if not self.platform.is_linux:
            return True
        
        # Create wgcf-start service
        service_content = """[Unit]
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
"""
        
        try:
            # Create service file
            service_path = Path("/etc/systemd/system/wgcf-start.service")
            with open(service_path, 'w') as f:
                f.write(service_content)
            
            # Enable services
            commands = [
                ["systemctl", "daemon-reload"],
                ["systemctl", "enable", "wgcf-start"],
                ["systemctl", "disable", "wg-quick@wgcf"],  # Prevent race condition
                ["systemctl", "enable", "nextdns"],
                ["modprobe", "wireguard"],  # Load WireGuard kernel module
            ]
            
            for cmd in commands:
                self.platform.run_command(cmd)
            
            # Add wireguard to modules-load.d
            with open("/etc/modules-load.d/wireguard.conf", "w") as f:
                f.write("wireguard\n")
            
            self.console.print("[green]Systemd services configured successfully.[/green]")
            return True
            
        except Exception as e:
            self.console.print(f"[red]Failed to setup systemd services: {e}[/red]")
            return False
    
    def start_services(self) -> bool:
        """Start WARP and NextDNS services."""
        try:
            # Start NextDNS first
            if not self.nextdns.get_status().get("running", False):
                self.nextdns.start()
                time.sleep(2)  # Wait for NextDNS to initialize
            
            # Start WireGuard
            if self.platform.is_linux:
                self.platform.run_command(["systemctl", "start", "wg-quick@wgcf"], check=False)
            else:
                self.platform.run_command(["wg-quick", "up", "wgcf"], check=False)
            
            # Verify connection
            time.sleep(3)
            return self.verify_connection()
            
        except Exception as e:
            self.console.print(f"[red]Failed to start services: {e}[/red]")
            return False
    
    def stop_services(self) -> bool:
        """Stop WARP and NextDNS services."""
        try:
            # Stop WireGuard
            if self.platform.is_linux:
                self.platform.run_command(["systemctl", "stop", "wg-quick@wgcf"], check=False)
            else:
                self.platform.run_command(["wg-quick", "down", "wgcf"], check=False)
            
            self.console.print("[green]Services stopped successfully.[/green]")
            return True
            
        except Exception as e:
            self.console.print(f"[red]Failed to stop services: {e}[/red]")
            return False
    
    def verify_connection(self) -> bool:
        """Verify WARP and NextDNS connection."""
        results = {}
        
        # Check WARP connection
        try:
            result = self.platform.run_command(
                ["curl", "-s", "https://www.cloudflare.com/cdn-cgi/trace"],
                check=False
            )
            results["warp_active"] = "warp=on" in result.stdout
        except:
            results["warp_active"] = False
        
        # Check NextDNS
        results["nextdns_running"] = self.nextdns.get_status().get("running", False)
        results["nextdns_working"] = self.nextdns.test_connection()
        
        # Check WireGuard interface
        try:
            result = self.platform.run_command(["wg", "show", "wgcf"], check=False)
            results["wireguard_active"] = result.returncode == 0
        except:
            results["wireguard_active"] = False
        
        # Display results
        self.nav.display_status("Connection Status", results)
        
        return all(results.values())
    
    def quick_setup(self) -> bool:
        """Perform quick automated setup."""
        self.console.print(Panel("Starting Quick Setup", style="bold blue"))
        
        # Check and install prerequisites
        if not self.install_prerequisites():
            return False
        
        # Setup WARP
        if not self.wgcf.is_installed():
            if not self.setup_warp():
                return False
        
        # Configure NextDNS
        if not self.nextdns.is_configured():
            if not self.configure_nextdns():
                return False
        
        # Setup systemd services
        if self.platform.is_linux:
            self.setup_systemd_services()
        
        # Start services
        if self.nav.auto_confirm("Start services now?", default=True):
            return self.start_services()
        
        return True
    
    def uninstall(self) -> bool:
        """Uninstall WARP NextDNS setup."""
        if not self.nav.auto_confirm("Are you sure you want to uninstall?", default=False):
            return False
        
        steps = []
        
        # Stop services
        steps.append({
            "name": "Stop services",
            "action": self.stop_services
        })
        
        # Remove systemd services
        if self.platform.is_linux:
            steps.append({
                "name": "Remove systemd services",
                "action": lambda: self._remove_systemd_services()
            })
        
        # Remove WireGuard config
        steps.append({
            "name": "Remove WireGuard configuration",
            "action": lambda: self._remove_wireguard_config()
        })
        
        # Optionally remove NextDNS
        if self.nav.auto_confirm("Also uninstall NextDNS?", default=False):
            steps.append({
                "name": "Uninstall NextDNS",
                "action": lambda: self.platform.run_command(["nextdns", "uninstall"], check=False)
            })
        
        return self.nav.display_progress("Uninstalling", steps)
    
    def _remove_systemd_services(self) -> bool:
        """Remove systemd service files."""
        try:
            service_files = [
                "/etc/systemd/system/wgcf-start.service",
                "/etc/modules-load.d/wireguard.conf"
            ]
            
            for file in service_files:
                Path(file).unlink(missing_ok=True)
            
            self.platform.run_command(["systemctl", "daemon-reload"])
            return True
        except:
            return False
    
    def _remove_wireguard_config(self) -> bool:
        """Remove WireGuard configuration files."""
        try:
            files_to_remove = [
                "/etc/wireguard/wgcf.conf",
                "wgcf-account.toml",
                "wgcf-profile.conf",
                "wgcf"
            ]
            
            for file in files_to_remove:
                Path(file).unlink(missing_ok=True)
            
            return True
        except:
            return False
    
    def show_logs(self):
        """Show system logs."""
        if self.platform.is_linux:
            # Show systemd logs
            self.console.print("\n[cyan]WireGuard logs:[/cyan]")
            self.platform.run_command(["journalctl", "-u", "wg-quick@wgcf", "-n", "20", "--no-pager"], check=False)
            
            self.console.print("\n[cyan]NextDNS logs:[/cyan]")
            try:
                logs = self.nextdns.get_logs(20)
                self.console.print(logs)
            except:
                self.console.print("[yellow]Could not retrieve NextDNS logs[/yellow]")
    
    def export_config(self, output_file: Optional[Path] = None) -> bool:
        """Export current configuration."""
        if not output_file:
            output_file = Path("warp-nextdns-backup.tar.gz")
        
        try:
            import tarfile
            
            with tarfile.open(output_file, "w:gz") as tar:
                # Add WireGuard config
                if Path("/etc/wireguard/wgcf.conf").exists():
                    tar.add("/etc/wireguard/wgcf.conf", arcname="wgcf.conf")
                
                # Add NextDNS config
                if Path("/etc/nextdns.conf").exists():
                    tar.add("/etc/nextdns.conf", arcname="nextdns.conf")
                
                # Add account files
                for file in ["wgcf-account.toml", "wgcf-profile.conf"]:
                    if Path(file).exists():
                        tar.add(file, arcname=file)
            
            self.console.print(f"[green]Configuration exported to {output_file}[/green]")
            return True
            
        except Exception as e:
            self.console.print(f"[red]Failed to export configuration: {e}[/red]")
            return False