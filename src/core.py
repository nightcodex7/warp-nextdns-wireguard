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
from typing import Dict, List, Optional, Tuple, Any
import requests
from rich.console import Console
from rich.panel import Panel

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from utils.platform_utils import PlatformUtils
from utils.installer_manager import InstallerManager
from utils.wgcf_manager import WGCFManager
from utils.nextdns_manager import NextDNSManager
from utils.error_handler import ErrorHandler

# Configure logging
def setup_logging():
    """Setup logging configuration with cross-platform support"""
    if sys.platform == "win32":
        log_dir = Path.home() / ".warp" / "logs"
    else:
        log_dir = Path("/var/log/warp-nextdns")
    
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "warp-nextdns.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

class WarpNextDNSManager:
    """Enhanced WARP + NextDNS Manager with automatic elevation"""
    
    def __init__(self, auto_mode: bool = False):
        self.auto_mode = auto_mode
        self.platform = PlatformUtils()
        
        # Check for macOS and warn user
        if self.platform.is_macos:
            print("⚠️  WARNING: macOS is not supported by this project!")
            print("   This software is designed for Linux and Windows only.")
            print("   Attempting to continue may cause system issues.")
            print("   Please use a supported platform.\n")
        
        self.installer = InstallerManager()
        self.wgcf_manager = WGCFManager()
        self.nextdns_manager = NextDNSManager()
        self.error_handler = ErrorHandler()
        self.console = Console()
        
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
                    
        logger.error(f"Failed to download {url} after {max_retries} attempts")
        return False
    
    def install_dependencies(self) -> Dict[str, bool]:
        """Install required system dependencies"""
        logger.info("Installing system dependencies...")
        
        results = {}
        
        # Install wgcf
        try:
            results['wgcf'] = self.wgcf_manager.install()
        except Exception as e:
            logger.error(f"Failed to install wgcf: {e}")
            results['wgcf'] = False
            
        # Install NextDNS CLI
        try:
            results['nextdns'] = self.nextdns_manager.install()
        except Exception as e:
            logger.error(f"Failed to install NextDNS CLI: {e}")
            results['nextdns'] = False
            
        return results
    
    def setup_wgcf(self) -> Dict[str, Any]:
        """Setup WGCF and generate WireGuard configuration"""
        logger.info("Setting up WGCF...")
        
        try:
            # Check if wgcf is installed
            if not self.wgcf_manager.is_installed():
                logger.error("WGCF is not installed")
                return {'success': False, 'error': 'WGCF not installed'}
            
            # Register with WARP
            registration = self.wgcf_manager.register()
            if not registration['success']:
                return registration
            
            # Generate WireGuard configuration
            config = self.wgcf_manager.generate_config()
            if not config['success']:
                return config
            
            logger.info("WGCF setup completed successfully")
            return {'success': True, 'config': config['config']}
            
        except Exception as e:
            error_msg = f"WGCF setup failed: {e}"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}
    
    def setup_nextdns_config(self, profile_id: str) -> Dict[str, Any]:
        """Setup NextDNS configuration"""
        logger.info(f"Setting up NextDNS configuration for profile: {profile_id}")
        
        try:
            # Check if NextDNS CLI is installed
            if not self.nextdns_manager.is_installed():
                logger.error("NextDNS CLI is not installed")
                return {'success': False, 'error': 'NextDNS CLI not installed'}
            
            # Configure NextDNS
            config = self.nextdns_manager.configure(profile_id)
            if not config['success']:
                return config
            
            logger.info("NextDNS configuration completed successfully")
            return {'success': True, 'config': config['config']}
            
        except Exception as e:
            error_msg = f"NextDNS configuration failed: {e}"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}
    
    def create_systemd_services(self) -> bool:
        """Create systemd services for WARP and NextDNS"""
        logger.info("Creating systemd services...")
        
        try:
            # Create WARP service
            warp_service = self.wgcf_manager.create_service()
            if not warp_service:
                logger.error("Failed to create WARP service")
                return False
            
            # Create NextDNS service
            nextdns_service = self.nextdns_manager.create_service()
            if not nextdns_service:
                logger.error("Failed to create NextDNS service")
                return False
            
            logger.info("Systemd services created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create systemd services: {e}")
            return False
    
    def start_services(self) -> bool:
        """Start WARP and NextDNS services"""
        logger.info("Starting services...")
        
        try:
            # Start WARP service
            warp_started = self.wgcf_manager.start_service()
            if not warp_started:
                logger.error("Failed to start WARP service")
                return False
            
            # Start NextDNS service
            nextdns_started = self.nextdns_manager.start_service()
            if not nextdns_started:
                logger.error("Failed to start NextDNS service")
                return False
            
            logger.info("Services started successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start services: {e}")
            return False
    
    def stop_services(self) -> bool:
        """Stop WARP and NextDNS services"""
        logger.info("Stopping services...")
        
        try:
            # Stop WARP service
            warp_stopped = self.wgcf_manager.stop_service()
            if not warp_stopped:
                logger.warning("Failed to stop WARP service")
            
            # Stop NextDNS service
            nextdns_stopped = self.nextdns_manager.stop_service()
            if not nextdns_stopped:
                logger.warning("Failed to stop NextDNS service")
            
            logger.info("Services stopped")
            return True
            
        except Exception as e:
            logger.error(f"Failed to stop services: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get current system status with modern UI format"""
        logger.info("Getting system status...")
        
        try:
            # Get service statuses
            warp_status = self.wgcf_manager.get_service_status()
            nextdns_status = self.nextdns_manager.get_service_status()
            
            # Get tool availability
            wgcf_installed = self.wgcf_manager.is_installed()
            nextdns_installed = self.nextdns_manager.is_installed()
            
            # Get network status
            internet_connected = self.check_internet_connection()
            warp_ip = self.get_warp_ip()
            dns_servers = self.get_dns_servers()
            
            # Format for modern UI
            status = {
                'System': {
                    'status': 'Active',
                    'details': f"{platform.system()} {platform.machine()} - Python {platform.python_version()}"
                },
                'WARP Service': {
                    'status': 'Running' if warp_status.get('running', False) else 'Stopped',
                    'details': warp_status.get('details', 'Service status unknown')
                },
                'NextDNS Service': {
                    'status': 'Running' if nextdns_status.get('running', False) else 'Stopped',
                    'details': nextdns_status.get('details', 'Service status unknown')
                },
                'WGCF Tool': {
                    'status': 'Installed' if wgcf_installed else 'Not Installed',
                    'details': 'WireGuard configuration tool'
                },
                'NextDNS Tool': {
                    'status': 'Installed' if nextdns_installed else 'Not Installed',
                    'details': 'DNS filtering tool'
                },
                'Internet Connection': {
                    'status': 'Connected' if internet_connected else 'Disconnected',
                    'details': 'Network connectivity check'
                },
                'WARP IP': {
                    'status': 'Active' if warp_ip else 'Inactive',
                    'details': warp_ip or 'No WARP IP detected'
                },
                'DNS Servers': {
                    'status': 'Configured' if dns_servers else 'Not Configured',
                    'details': ', '.join(dns_servers) if dns_servers else 'No DNS servers found'
                }
            }
            
            # Add timestamp
            status['Last Updated'] = {
                'status': datetime.now().strftime('%H:%M:%S'),
                'details': 'Real-time status'
            }
            
            return status
            
        except Exception as e:
            logger.error(f"Failed to get status: {e}")
            return {
                'Error': {
                    'status': 'Failed',
                    'details': f"Status check failed: {str(e)}"
                }
            }
    
    def check_internet_connection(self) -> bool:
        """Check internet connectivity"""
        try:
            response = requests.get("https://www.google.com", timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    def get_warp_ip(self) -> Optional[str]:
        """Get WARP IP address"""
        try:
            response = requests.get("https://ipinfo.io/ip", timeout=5)
            return response.text.strip()
        except Exception:
            return None
    
    def get_dns_servers(self) -> List[str]:
        """Get current DNS servers"""
        try:
            if sys.platform == "win32":
                result = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True)
                # Parse DNS servers from ipconfig output
                dns_servers = []
                for line in result.stdout.split('\n'):
                    if 'DNS Servers' in line:
                        dns = line.split(':')[-1].strip()
                        if dns:
                            dns_servers.append(dns)
                return dns_servers
            else:
                result = subprocess.run(['cat', '/etc/resolv.conf'], capture_output=True, text=True)
                dns_servers = []
                for line in result.stdout.split('\n'):
                    if line.startswith('nameserver'):
                        dns = line.split()[1]
                        dns_servers.append(dns)
                return dns_servers
        except Exception:
            return []
    
    def verify_connection(self) -> bool:
        """Verify WARP and NextDNS connection"""
        logger.info("Verifying connection...")
        
        try:
            # Check WARP connection
            warp_status = self.wgcf_manager.get_service_status()
            if not warp_status['running']:
                logger.error("WARP service is not running")
                return False
            
            # Check NextDNS connection
            nextdns_status = self.nextdns_manager.get_service_status()
            if not nextdns_status['running']:
                logger.error("NextDNS service is not running")
                return False
            
            # Check internet connectivity
            if not self.check_internet_connection():
                logger.error("No internet connection")
                return False
            
            logger.info("Connection verification successful")
            return True
            
        except Exception as e:
            logger.error(f"Connection verification failed: {e}")
            return False
    
    def quick_setup(self) -> bool:
        """Perform complete setup process"""
        logger.info("Starting quick setup...")
        
        try:
            # Ensure elevation
            if not self.ensure_elevation():
                return False
            
            # Install dependencies
            deps = self.install_dependencies()
            if not all(deps.values()):
                logger.error("Failed to install all dependencies")
                return False
            
            # Setup WGCF
            wgcf_setup = self.setup_wgcf()
            if not wgcf_setup['success']:
                logger.error(f"WGCF setup failed: {wgcf_setup['error']}")
                return False
            
            # Setup NextDNS (using default profile if auto mode)
            profile_id = "default" if self.auto_mode else None
            if profile_id:
                nextdns_setup = self.setup_nextdns_config(profile_id)
                if not nextdns_setup['success']:
                    logger.error(f"NextDNS setup failed: {nextdns_setup['error']}")
                    return False
            
            # Create services
            if not self.create_systemd_services():
                logger.error("Failed to create systemd services")
                return False
            
            # Start services
            if not self.start_services():
                logger.error("Failed to start services")
                return False
            
            logger.info("Quick setup completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Quick setup failed: {e}")
            return False
    
    def cleanup(self):
        """Cleanup resources"""
        logger.info("Cleaning up...")
        try:
            # Stop services
            self.stop_services()
        except Exception as e:
            logger.error(f"Cleanup error: {e}")

# Backward compatibility
WarpNextDNSManager = WarpNextDNSManager 
