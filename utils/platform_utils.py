"""Platform-specific utilities for cross-platform support."""
import os
import platform
import subprocess
import sys
from typing import Dict, Optional, Tuple


class PlatformUtils:
    """Handle platform-specific operations."""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.is_linux = self.system == "linux"
        self.is_windows = self.system == "windows"
        self.is_macos = self.system == "darwin"  # For detection only - not supported
        
        # Check if running on macOS and warn user
        if self.is_macos:
            print("⚠️  WARNING: macOS is not supported by this project!")
            print("   This software is designed for Linux and Windows only.")
            print("   Attempting to continue may cause system issues.")
            print("   Please use a supported platform.\n")
        
    def check_root_access(self) -> bool:
        """Check if running with root/admin privileges."""
        if self.is_linux:
            return os.geteuid() == 0
        elif self.is_windows:
            try:
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            except:
                return False
        elif self.is_macos:
            print("⚠️  macOS detected - root access check not supported")
            return False
        return False
    
    def get_package_manager(self) -> Optional[str]:
        """Detect the system package manager."""
        if not self.is_linux:
            return None
            
        managers = ["apt", "yum", "dnf", "pacman", "zypper"]
        for manager in managers:
            if self.command_exists(manager):
                return manager
        return None
    
    def command_exists(self, command: str) -> bool:
        """Check if a command exists in PATH."""
        try:
            subprocess.run(
                ["which", command] if not self.is_windows else ["where", command],
                capture_output=True,
                check=True
            )
            return True
        except subprocess.CalledProcessError:
            return False
    
    def run_command(
        self, 
        command: list,
        capture_output: bool = True,
        check: bool = True
    ) -> subprocess.CompletedProcess:
        """Run a system command with proper error handling."""
        try:
            return subprocess.run(
                command,
                capture_output=capture_output,
                text=True,
                check=check
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Command failed: {' '.join(command)}\n{e.stderr}")
    
    def get_system_info(self) -> Dict[str, str]:
        """Get system information."""
        return {
            "os": self.system,
            "platform": platform.platform(),
            "version": platform.version(),
            "machine": platform.machine(),
            "python": sys.version,
        }