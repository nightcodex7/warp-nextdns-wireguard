#!/usr/bin/env python3
"""
Enhanced WARP + NextDNS Manager
Manages Cloudflare WARP and NextDNS services via WireGuard with automatic elevation
"""

import os
import sys
import platform
import subprocess
import json
import time
import logging
import signal
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import requests

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from utils.platform_utils import PlatformUtils
from utils.installer_manager import InstallerManager
from utils.wgcf_manager import WGCFManager
from utils.nextdns_manager import NextDNSManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/warp-nextdns.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EnhancedWARPManager:
    """Enhanced WARP + NextDNS Manager with automatic elevation"""
    
    def __init__(self):
        self.platform = PlatformUtils()
        self.installer = InstallerManager()
        self.wgcf_manager = WGCFManager()
        self.nextdns_manager = NextDNSManager()
        
        self.config_dir = Path.home() / '.warp-nextdns'
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.status = {}
        self.is_elevated = False
        
        # Handle terminal interruptions gracefully
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
    def _signal_handler(self, signum, frame):
        """Handle interruption signals gracefully"""
        logger.info(f"Received signal {signum}, cleaning up...")
        self.cleanup()
        sys.exit(0)
    
    def auto_elevate_if_needed(self) -> bool:
        """Automatically elevate privileges if needed"""
        if self.platform.check_root_access():
            self.is_elevated = True
            return True
            
        logger.info("Elevated privileges required, attempting auto-elevation...")
        
        try:
            if self.installer.auto_elevate():
                self.is_elevated = True
                return True
        except Exception as e:
            logger.error(f"Auto-elevation failed: {e}")
            
        return False
    
    def ensure_elevation(self) -> bool:
        """Ensure we have elevated privileges, prompt if needed"""
        if self.is_elevated:
            return True
            
        if not self.auto_elevate_if_needed():
            logger.error("Elevated privileges required. Please run with sudo/admin rights.")
            return False
            
        return True
    
    def download_with_retry(self, url: str, dest: Path, max_retries: int = 3) -> bool:
        """Download file with retry logic and progress"""
        for attempt in range(max_retries):
            try:
                logger.info(f"Downloading {url} (attempt {attempt + 1}/{max_retries})")
                
                if self.installer.download_with_progress(url, dest):
                    logger.info("Download completed successfully")
                    return True
                    
            except Exception as e:
                logger.warning(f"Download attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    
        logger.error("All download attempts failed")
        return False
    
    def install_dependencies(self) -> Dict[str, bool]:
        """Install all required dependencies"""
        results = {}
        
        logger.info("Installing system dependencies...")
        
        # Install WireGuard tools
        try:
            results['wireguard'] = self.installer.install_wireguard_tools()
            logger.info("WireGuard tools installation: " + ("SUCCESS" if results['wireguard'] else "FAILED"))
        except Exception as e:
            logger.error(f"WireGuard installation failed: {e}")
            results['wireguard'] = False
        
        # Install NextDNS CLI
        try:
            if not self.nextdns_manager.is_installed():
                results['nextdns'] = self.nextdns_manager.install()
                logger.info("NextDNS installation: " + ("SUCCESS" if results['nextdns'] else "FAILED"))
            else:
                results['nextdns'] = True
                logger.info("NextDNS already installed")
        except Exception as e:
            logger.error(f"NextDNS installation failed: {e}")
            results['nextdns'] = False
        
        return results
    
    def setup_wgcf(self) -> Dict[str, any]:
        """Setup WGCF with automatic handling"""
        results = {'success': False, 'message': '', 'error': None}
        
        try:
            logger.info("Setting up WGCF...")
            
            # Download WGCF if needed
            if not self.wgcf_manager.wgcf_path.exists():
                logger.info("Downloading WGCF...")
                if not self.wgcf_manager.download_wgcf():
                    raise RuntimeError("Failed to download WGCF")
            
            # Register account if needed
            if not self.wgcf_manager.account_file.exists():
                logger.info("Registering WARP account...")
                if not self.wgcf_manager.register_account():
                    raise RuntimeError("Failed to register WARP account")
            
            # Generate profile if needed
            if not self.wgcf_manager.profile_file.exists():
                logger.info("Generating WireGuard profile...")
                if not self.wgcf_manager.generate_profile():
                    raise RuntimeError("Failed to generate profile")
            
            # Modify for NextDNS
            logger.info("Modifying profile for NextDNS...")
            if not self.wgcf_manager.modify_profile_for_nextdns():
                raise RuntimeError("Failed to modify profile")
            
            # Install profile
            logger.info("Installing WireGuard profile...")
            if not self.wgcf_manager.install_profile():
                raise RuntimeError("Failed to install profile")
            
            results['success'] = True
            results['message'] = "WGCF setup completed successfully"
            
        except Exception as e:
            results['error'] = str(e)
            logger.error(f"WGCF setup failed: {e}")
        
        return results
    
    def setup_nextdns_config(self, profile_id: str) -> Dict[str, any]:
        """Setup NextDNS configuration"""
        results = {'success': False, 'message': '', 'error': None}
        
        try:
            logger.info(f"Configuring NextDNS with profile: {profile_id}")
            
            if not self.nextdns_manager.configure(profile_id):
                raise RuntimeError("Failed to configure NextDNS")
            
            # Start NextDNS service
            if not self.nextdns_manager.start():
                raise RuntimeError("Failed to start NextDNS service")
            
            results['success'] = True
            results['message'] = "NextDNS configuration completed successfully"
            
        except Exception as e:
            results['error'] = str(e)
            logger.error(f"NextDNS configuration failed: {e}")
        
        return results
    
    def create_systemd_services(self) -> bool:
        """Create systemd services for auto-start"""
        if not self.platform.is_linux:
            return False
            
        try:
            # WGCF service
            wgcf_service = """[Unit]
Description=WGCF WARP WireGuard Interface
After=network-online.target
Wants=network-online.target
ConditionPathExists=/etc/wireguard/wgcf.conf

[Service]
Type=oneshot
ExecStartPre=/sbin/modprobe wireguard
ExecStart=/usr/bin/wg-quick up wgcf
ExecStop=/usr/bin/wg-quick down wgcf
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
"""
            
            # NextDNS service (if not already created by nextdns install)
            nextdns_service = """[Unit]
Description=NextDNS DNS over HTTPS proxy
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/usr/bin/nextdns start
ExecStop=/usr/bin/nextdns stop
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
"""
            
            # Create services
            self.installer.create_systemd_service("wgcf", wgcf_service)
            self.installer.create_systemd_service("nextdns", nextdns_service)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to create systemd services: {e}")
            return False
    
    def start_services(self) -> Dict[str, bool]:
        """Start all services"""
        results = {}
        
        try:
            # Start NextDNS first
            logger.info("Starting NextDNS service...")
            results['nextdns'] = self.nextdns_manager.start()
            
            # Start WGCF
            logger.info("Starting WGCF service...")
            if self.platform.is_linux:
                self.platform.run_command(["systemctl", "start", "wgcf"])
                results['wgcf'] = True
            else:
                # For non-Linux systems, use wg-quick directly
                self.platform.run_command(["wg-quick", "up", "wgcf"])
                results['wgcf'] = True
                
        except Exception as e:
            logger.error(f"Failed to start services: {e}")
            results['wgcf'] = False
        
        return results
    
    def stop_services(self) -> Dict[str, bool]:
        """Stop all services"""
        results = {}
        
        try:
            # Stop WGCF first
            logger.info("Stopping WGCF service...")
            if self.platform.is_linux:
                self.platform.run_command(["systemctl", "stop", "wgcf"])
                results['wgcf'] = True
            else:
                self.platform.run_command(["wg-quick", "down", "wgcf"])
                results['wgcf'] = True
            
            # Stop NextDNS
            logger.info("Stopping NextDNS service...")
            results['nextdns'] = self.nextdns_manager.stop()
            
        except Exception as e:
            logger.error(f"Failed to stop services: {e}")
            results['wgcf'] = False
            results['nextdns'] = False
        
        return results
    
    def get_status(self) -> Dict[str, any]:
        """Get comprehensive status of all services"""
        status = {
            'platform': self.platform.get_system_info(),
            'elevated': self.is_elevated,
            'wgcf': self.wgcf_manager.get_status(),
            'nextdns': self.nextdns_manager.get_status(),
            'timestamp': datetime.now().isoformat()
        }
        
        # Check if services are running
        try:
            if self.platform.is_linux:
                # Check systemd services
                wgcf_result = self.platform.run_command(["systemctl", "is-active", "wgcf"], check=False)
                status['wgcf']['running'] = wgcf_result.returncode == 0
                
                nextdns_result = self.platform.run_command(["systemctl", "is-active", "nextdns"], check=False)
                status['nextdns']['running'] = nextdns_result.returncode == 0
            else:
                # Check processes
                wg_result = self.platform.run_command(["wg", "show"], check=False)
                status['wgcf']['running'] = wg_result.returncode == 0
                
                status['nextdns']['running'] = self.nextdns_manager.get_status().get('running', False)
                
        except Exception as e:
            logger.error(f"Failed to check service status: {e}")
        
        return status
    
    def test_connection(self) -> Dict[str, any]:
        """Test WARP and NextDNS connectivity"""
        results = {
            'warp': False,
            'nextdns': False,
            'internet': False
        }
        
        try:
            # Test internet connectivity
            logger.info("Testing internet connectivity...")
            response = requests.get("https://www.google.com", timeout=10)
            results['internet'] = response.status_code == 200
            
            # Test WARP
            logger.info("Testing WARP connectivity...")
            response = requests.get("https://www.cloudflare.com/cdn-cgi/trace", timeout=10)
            if response.status_code == 200:
                trace_data = response.text
                results['warp'] = 'warp=on' in trace_data
            
            # Test NextDNS
            logger.info("Testing NextDNS connectivity...")
            results['nextdns'] = self.nextdns_manager.test_connection()
            
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
        
        return results
    
    def setup_auto_start(self) -> bool:
        """Setup auto-start for the manager"""
        try:
            script_path = Path(__file__).resolve()
            return self.installer.setup_auto_start(script_path)
        except Exception as e:
            logger.error(f"Failed to setup auto-start: {e}")
            return False
    
    def cleanup(self):
        """Cleanup temporary files and resources"""
        try:
            self.installer.cleanup_temp_files()
            logger.info("Cleanup completed")
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")
    
    def run_interactive_setup(self) -> bool:
        """Run interactive setup wizard"""
        print("=== WARP + NextDNS Setup Wizard ===")
        print()
        
        # Check elevation
        if not self.ensure_elevation():
            print("❌ Elevated privileges required. Please run with sudo/admin rights.")
            return False
        
        print("✅ Elevated privileges confirmed")
        print()
        
        # Install dependencies
        print("📦 Installing system dependencies...")
        deps = self.install_dependencies()
        
        if not all(deps.values()):
            print("❌ Some dependencies failed to install:")
            for dep, success in deps.items():
                print(f"   {dep}: {'✅' if success else '❌'}")
            return False
        
        print("✅ All dependencies installed successfully")
        print()
        
        # Setup WGCF
        print("🔧 Setting up WGCF...")
        wgcf_result = self.setup_wgcf()
        
        if not wgcf_result['success']:
            print(f"❌ WGCF setup failed: {wgcf_result['error']}")
            return False
        
        print("✅ WGCF setup completed")
        print()
        
        # Setup NextDNS
        profile_id = input("Enter your NextDNS profile ID: ").strip()
        if not profile_id:
            print("❌ NextDNS profile ID is required")
            return False
        
        print("🔧 Setting up NextDNS...")
        nextdns_result = self.setup_nextdns_config(profile_id)
        
        if not nextdns_result['success']:
            print(f"❌ NextDNS setup failed: {nextdns_result['error']}")
            return False
        
        print("✅ NextDNS setup completed")
        print()
        
        # Create systemd services (Linux only)
        if self.platform.is_linux:
            print("🔧 Creating system services...")
            if self.create_systemd_services():
                print("✅ System services created")
            else:
                print("⚠️  Failed to create system services")
            print()
        
        # Start services
        print("🚀 Starting services...")
        start_results = self.start_services()
        
        if all(start_results.values()):
            print("✅ All services started successfully")
        else:
            print("⚠️  Some services failed to start")
        print()
        
        # Test connection
        print("🔍 Testing connectivity...")
        test_results = self.test_connection()
        
        print("Connection test results:")
        print(f"   Internet: {'✅' if test_results['internet'] else '❌'}")
        print(f"   WARP: {'✅' if test_results['warp'] else '❌'}")
        print(f"   NextDNS: {'✅' if test_results['nextdns'] else '❌'}")
        print()
        
        # Setup auto-start
        print("🔧 Setting up auto-start...")
        if self.setup_auto_start():
            print("✅ Auto-start configured")
        else:
            print("⚠️  Auto-start configuration failed")
        print()
        
        print("🎉 Setup completed successfully!")
        print("Your WARP + NextDNS configuration is now active.")
        
        return True

def main():
    """Main entry point"""
    manager = EnhancedWARPManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "setup":
            success = manager.run_interactive_setup()
            sys.exit(0 if success else 1)
            
        elif command == "start":
            if not manager.ensure_elevation():
                sys.exit(1)
            results = manager.start_services()
            print(json.dumps(results, indent=2))
            
        elif command == "stop":
            if not manager.ensure_elevation():
                sys.exit(1)
            results = manager.stop_services()
            print(json.dumps(results, indent=2))
            
        elif command == "status":
            status = manager.get_status()
            print(json.dumps(status, indent=2))
            
        elif command == "test":
            results = manager.test_connection()
            print(json.dumps(results, indent=2))
            
        else:
            print(f"Unknown command: {command}")
            print("Available commands: setup, start, stop, status, test")
            sys.exit(1)
    else:
        # Run interactive setup by default
        success = manager.run_interactive_setup()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 