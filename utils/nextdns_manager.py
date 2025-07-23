"""NextDNS manager for DNS configuration."""
import subprocess
from pathlib import Path
from typing import Optional, Dict
from .platform_utils import PlatformUtils


class NextDNSManager:
    """Manage NextDNS installation and configuration."""
    
    def __init__(self):
        self.platform = PlatformUtils()
        self.config_file = Path("/etc/nextdns.conf")
        
    def is_installed(self) -> bool:
        """Check if NextDNS is installed."""
        return self.platform.command_exists("nextdns")
    
    def is_configured(self) -> bool:
        """Check if NextDNS is configured."""
        return self.config_file.exists()
    
    def get_status(self) -> Dict[str, any]:
        """Get NextDNS status."""
        if not self.is_installed():
            return {"installed": False, "running": False, "configured": False}
        
        try:
            result = self.platform.run_command(["nextdns", "status"], check=False)
            is_running = "running" in result.stdout.lower()
            
            return {
                "installed": True,
                "running": is_running,
                "configured": self.is_configured(),
                "status_output": result.stdout
            }
        except Exception as e:
            return {
                "installed": True,
                "running": False,
                "configured": self.is_configured(),
                "error": str(e)
            }
    
    def install(self) -> bool:
        """Install NextDNS using the official script."""
        if not self.platform.check_root_access():
            raise RuntimeError("Root access required to install NextDNS.")
        
        try:
            # Download and run the official installer
            cmd = "sh -c 'curl -sSL https://nextdns.io/install | sh'"
            self.platform.run_command(["bash", "-c", cmd])
            return self.is_installed()
        except Exception as e:
            raise RuntimeError(f"Failed to install NextDNS: {e}")
    
    def configure(self, profile_id: str, arguments: Optional[str] = None) -> bool:
        """Configure NextDNS with profile ID."""
        if not self.is_installed():
            raise RuntimeError("NextDNS is not installed.")
        
        if not self.platform.check_root_access():
            raise RuntimeError("Root access required to configure NextDNS.")
        
        try:
            # Basic configuration command
            cmd = ["nextdns", "install", "-config", profile_id]
            
            # Add additional arguments if provided
            if arguments:
                cmd.extend(arguments.split())
            
            self.platform.run_command(cmd)
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to configure NextDNS: {e}")
    
    def start(self) -> bool:
        """Start NextDNS service."""
        if not self.is_installed():
            raise RuntimeError("NextDNS is not installed.")
        
        if not self.platform.check_root_access():
            raise RuntimeError("Root access required to start NextDNS.")
        
        try:
            self.platform.run_command(["nextdns", "start"])
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to start NextDNS: {e}")
    
    def stop(self) -> bool:
        """Stop NextDNS service."""
        if not self.is_installed():
            raise RuntimeError("NextDNS is not installed.")
        
        if not self.platform.check_root_access():
            raise RuntimeError("Root access required to stop NextDNS.")
        
        try:
            self.platform.run_command(["nextdns", "stop"])
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to stop NextDNS: {e}")
    
    def restart(self) -> bool:
        """Restart NextDNS service."""
        if not self.is_installed():
            raise RuntimeError("NextDNS is not installed.")
        
        if not self.platform.check_root_access():
            raise RuntimeError("Root access required to restart NextDNS.")
        
        try:
            self.platform.run_command(["nextdns", "restart"])
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to restart NextDNS: {e}")
    
    def get_logs(self, lines: int = 50) -> str:
        """Get NextDNS logs."""
        if not self.is_installed():
            raise RuntimeError("NextDNS is not installed.")
        
        try:
            result = self.platform.run_command(["nextdns", "log", "-n", str(lines)])
            return result.stdout
        except Exception as e:
            raise RuntimeError(f"Failed to get NextDNS logs: {e}")
    
    def test_connection(self) -> bool:
        """Test if NextDNS is working properly."""
        if not self.is_installed():
            return False
        
        status = self.get_status()
        if not status.get("running", False):
            return False
        
        # Test DNS resolution through NextDNS
        try:
            result = self.platform.run_command([
                "dig", "@127.0.0.1", "test.nextdns.io", "+short"
            ], check=False)
            return "success" in result.stdout.lower()
        except:
            return False