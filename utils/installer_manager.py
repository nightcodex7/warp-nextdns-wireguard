"""Enhanced installer manager with automatic elevation and OS-specific handling."""
import os
import sys
import subprocess
import platform
import tempfile
import tarfile
import zipfile
import requests
from pathlib import Path
from typing import Optional, Dict, Tuple
from .platform_utils import PlatformUtils


class InstallerManager:
    """Manage installation with automatic elevation and OS-specific handling."""
    
    def __init__(self):
        self.platform = PlatformUtils()
        self.temp_dir = Path(tempfile.gettempdir()) / "warp-nextdns-installer"
        self.temp_dir.mkdir(exist_ok=True)
        
    def auto_elevate(self) -> bool:
        """Automatically elevate privileges if not running as root/admin."""
        if self.platform.check_root_access():
            return True
            
        if self.platform.is_linux:
            # Try to re-run with sudo
            if os.environ.get('SUDO_ASKPASS'):
                # Non-interactive sudo
                cmd = ['sudo', '-A', sys.executable] + sys.argv
            else:
                # Check if we can use pkexec (GUI elevation)
                if self.platform.command_exists('pkexec'):
                    cmd = ['pkexec', sys.executable] + sys.argv
                else:
                    # Fall back to sudo with -S for stdin password
                    cmd = ['sudo', '-S', sys.executable] + sys.argv
            
            try:
                # Execute elevated and exit current process
                os.execvp(cmd[0], cmd)
            except Exception as e:
                print(f"Failed to elevate privileges: {e}")
                return False
                
        elif self.platform.is_windows:
            # Windows UAC elevation
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                # Re-run the program with admin rights
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, " ".join(sys.argv), None, 1
                )
                sys.exit(0)
            return True
            
        elif self.platform.is_macos:
            print("⚠️  macOS is not supported by this project!")
            print("   This software is designed for Linux and Windows only.")
            print("   Please use a supported platform.")
            return False
                
        return False
    
    def detect_architecture(self) -> str:
        """Detect system architecture for downloads."""
        machine = platform.machine().lower()
        
        # Map common architectures
        arch_map = {
            'x86_64': 'amd64',
            'amd64': 'amd64',
            'i386': '386',
            'i686': '386',
            'aarch64': 'arm64',
            'arm64': 'arm64',
            'armv7l': 'arm7',
            'armv6l': 'arm6',
        }
        
        return arch_map.get(machine, 'amd64')
    
    def download_with_progress(self, url: str, dest: Path) -> bool:
        """Download file with progress indication."""
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            block_size = 8192
            downloaded = 0
            
            with open(dest, 'wb') as f:
                for chunk in response.iter_content(block_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # Progress indication
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"\rDownloading: {percent:.1f}%", end='', flush=True)
            
            print()  # New line after progress
            return True
            
        except Exception as e:
            print(f"Download failed: {e}")
            return False
    
    def extract_if_compressed(self, file_path: Path) -> Optional[Path]:
        """Extract compressed files and return the extracted binary path."""
        file_str = str(file_path).lower()
        
        try:
            if file_str.endswith('.tar.gz') or file_str.endswith('.tgz'):
                with tarfile.open(file_path, 'r:gz') as tar:
                    tar.extractall(path=file_path.parent)
                    # Find the binary
                    for member in tar.getmembers():
                        if member.isfile() and 'bin' in member.name:
                            return file_path.parent / member.name
                            
            elif file_str.endswith('.tar'):
                with tarfile.open(file_path, 'r') as tar:
                    tar.extractall(path=file_path.parent)
                    for member in tar.getmembers():
                        if member.isfile() and 'bin' in member.name:
                            return file_path.parent / member.name
                            
            elif file_str.endswith('.zip'):
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(path=file_path.parent)
                    # Find the binary
                    for name in zip_ref.namelist():
                        if 'bin' in name and not name.endswith('/'):
                            return file_path.parent / name
            
            # If not compressed, return original
            return file_path
            
        except Exception as e:
            print(f"Extraction failed: {e}")
            return None
    
    def install_wireguard_tools(self) -> bool:
        """Install WireGuard tools based on the OS."""
        if not self.platform.check_root_access():
            if not self.auto_elevate():
                raise RuntimeError("Root/admin access required for WireGuard installation")
        
        try:
            if self.platform.is_linux:
                pm = self.platform.get_package_manager()
                
                if pm == "apt":
                    # Debian/Ubuntu
                    self.platform.run_command(["apt", "update", "-y"])
                    self.platform.run_command(["apt", "install", "-y", "wireguard", "wireguard-tools", "curl", "dnsutils"])
                    
                elif pm == "yum" or pm == "dnf":
                    # RHEL/CentOS/Fedora
                    self.platform.run_command([pm, "install", "-y", "wireguard-tools", "curl", "bind-utils"])
                    
                elif pm == "pacman":
                    # Arch Linux
                    self.platform.run_command(["pacman", "-Sy", "--noconfirm", "wireguard-tools", "curl", "bind"])
                    
                elif pm == "zypper":
                    # openSUSE
                    self.platform.run_command(["zypper", "install", "-y", "wireguard-tools", "curl", "bind-utils"])
                    
                else:
                    print("Warning: Unknown package manager. Please install WireGuard manually.")
                    return False
                    
            elif self.platform.is_windows:
                # Download WireGuard installer for Windows
                url = "https://download.wireguard.com/windows-client/wireguard-installer.exe"
                installer = self.temp_dir / "wireguard-installer.exe"
                
                if self.download_with_progress(url, installer):
                    # Silent installation
                    self.platform.run_command([str(installer), "/S"], check=False)
                    
            elif self.platform.is_macos:
                print("⚠️  macOS is not supported by this project!")
                print("   WireGuard tools installation not available on macOS.")
                return False
                    
            return True
            
        except Exception as e:
            print(f"Failed to install WireGuard tools: {e}")
            return False
    
    def create_systemd_service(self, service_name: str, service_content: str) -> bool:
        """Create a systemd service file."""
        if not self.platform.is_linux:
            return False
            
        service_path = Path(f"/etc/systemd/system/{service_name}.service")
        
        try:
            with open(service_path, 'w') as f:
                f.write(service_content)
            
            # Reload systemd and enable service
            self.platform.run_command(["systemctl", "daemon-reload"])
            self.platform.run_command(["systemctl", "enable", service_name])
            
            return True
            
        except Exception as e:
            print(f"Failed to create systemd service: {e}")
            return False
    
    def setup_auto_start(self, script_path: Path) -> bool:
        """Setup auto-start based on the OS."""
        try:
            if self.platform.is_linux:
                # Create systemd service
                service_content = f"""[Unit]
Description=WARP NextDNS WireGuard Manager
After=network-online.target
Wants=network-online.target

[Service]
Type=forking
ExecStart={sys.executable} {script_path} start
ExecStop={sys.executable} {script_path} stop
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
"""
                return self.create_systemd_service("warp-nextdns", service_content)
                
            elif self.platform.is_windows:
                # Create Windows scheduled task
                import win32com.client
                scheduler = win32com.client.Dispatch('Schedule.Service')
                scheduler.Connect()
                
                root_folder = scheduler.GetFolder('\\')
                task_def = scheduler.NewTask(0)
                
                # Create trigger
                start_trigger = task_def.Triggers.Create(8)  # TASK_TRIGGER_BOOT
                start_trigger.Enabled = True
                
                # Create action
                exec_action = task_def.Actions.Create(0)  # TASK_ACTION_EXEC
                exec_action.Path = sys.executable
                exec_action.Arguments = f'"{script_path}" start'
                
                # Set principal
                task_def.Principal.RunLevel = 1  # TASK_RUNLEVEL_HIGHEST
                
                # Register task
                root_folder.RegisterTaskDefinition(
                    'WARP NextDNS Manager',
                    task_def,
                    6,  # TASK_CREATE_OR_UPDATE
                    '',  # No user
                    '',  # No password
                    3)  # TASK_LOGON_SERVICE_ACCOUNT
                    
                return True
                
            elif self.platform.is_macos:
                print("⚠️  macOS is not supported by this project!")
                print("   Auto-start setup not available on macOS.")
                return False
                
        except Exception as e:
            print(f"Failed to setup auto-start: {e}")
            return False
    
    def cleanup_temp_files(self):
        """Clean up temporary files."""
        try:
            import shutil
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
        except:
            pass