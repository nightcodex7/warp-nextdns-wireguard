# API Reference

> **Developer documentation for WARP + NextDNS Manager**

Complete API reference for developers and advanced users.

## 📚 Overview

The WARP + NextDNS Manager provides both a command-line interface and a programmatic API for integration with other applications.

## 🔧 Core Classes

### EnhancedWARPManager

The main manager class that handles all WARP and NextDNS operations.

```python
from core import EnhancedWARPManager

# Initialize the manager
manager = EnhancedWARPManager()
```

#### Methods

##### `auto_elevate_if_needed() -> bool`
Automatically elevate privileges if needed.

```python
# Auto-elevate privileges
if manager.auto_elevate_if_needed():
    print("Elevated successfully")
else:
    print("Elevation failed")
```

##### `ensure_elevation() -> bool`
Ensure elevated privileges are available.

```python
# Ensure elevation
if not manager.ensure_elevation():
    print("Elevated privileges required")
    sys.exit(1)
```

##### `install_dependencies() -> Dict[str, bool]`
Install all required system dependencies.

```python
# Install dependencies
results = manager.install_dependencies()
for dep, success in results.items():
    print(f"{dep}: {'✅' if success else '❌'}")
```

##### `setup_wgcf() -> Dict[str, any]`
Setup WGCF with automatic handling.

```python
# Setup WGCF
result = manager.setup_wgcf()
if result['success']:
    print("WGCF setup completed")
else:
    print(f"WGCF setup failed: {result['error']}")
```

##### `setup_nextdns_config(profile_id: str) -> Dict[str, any]`
Setup NextDNS configuration.

```python
# Setup NextDNS
result = manager.setup_nextdns_config("your-profile-id")
if result['success']:
    print("NextDNS setup completed")
else:
    print(f"NextDNS setup failed: {result['error']}")
```

##### `start_services() -> Dict[str, bool]`
Start all services.

```python
# Start services
results = manager.start_services()
for service, success in results.items():
    print(f"{service}: {'✅' if success else '❌'}")
```

##### `stop_services() -> Dict[str, bool]`
Stop all services.

```python
# Stop services
results = manager.stop_services()
for service, success in results.items():
    print(f"{service}: {'✅' if success else '❌'}")
```

##### `get_status() -> Dict[str, any]`
Get comprehensive status of all services.

```python
# Get status
status = manager.get_status()
print(f"WGCF running: {status['wgcf']['running']}")
print(f"NextDNS running: {status['nextdns']['running']}")
```

##### `test_connection() -> Dict[str, any]`
Test WARP and NextDNS connectivity.

```python
# Test connectivity
results = manager.test_connection()
print(f"Internet: {results['internet']}")
print(f"WARP: {results['warp']}")
print(f"NextDNS: {results['nextdns']}")
```

## 🛠️ Utility Classes

### PlatformUtils

Handles platform-specific operations and system detection.

```python
from utils.platform_utils import PlatformUtils

platform = PlatformUtils()
```

#### Methods

##### `check_root_access() -> bool`
Check if running with root/admin privileges.

```python
if platform.check_root_access():
    print("Running with elevated privileges")
else:
    print("Need elevated privileges")
```

##### `get_package_manager() -> Optional[str]`
Detect the system package manager.

```python
pm = platform.get_package_manager()
if pm:
    print(f"Package manager: {pm}")
else:
    print("No package manager detected")
```

##### `command_exists(command: str) -> bool`
Check if a command exists in PATH.

```python
if platform.command_exists("wg"):
    print("WireGuard tools available")
else:
    print("WireGuard tools not found")
```

##### `run_command(command: list, capture_output: bool = True, check: bool = True) -> subprocess.CompletedProcess`
Run a system command with proper error handling.

```python
try:
    result = platform.run_command(["wg", "show"])
    print(f"WireGuard status: {result.stdout}")
except RuntimeError as e:
    print(f"Command failed: {e}")
```

##### `get_system_info() -> Dict[str, str]`
Get system information.

```python
info = platform.get_system_info()
print(f"OS: {info['os']}")
print(f"Platform: {info['platform']}")
print(f"Architecture: {info['machine']}")
```

### InstallerManager

Manages installation with automatic elevation and OS-specific handling.

```python
from utils.installer_manager import InstallerManager

installer = InstallerManager()
```

#### Methods

##### `auto_elevate() -> bool`
Automatically elevate privileges if not running as root/admin.

```python
if installer.auto_elevate():
    print("Elevated successfully")
else:
    print("Elevation failed")
```

##### `detect_architecture() -> str`
Detect system architecture for downloads.

```python
arch = installer.detect_architecture()
print(f"Architecture: {arch}")
```

##### `download_with_progress(url: str, dest: Path) -> bool`
Download file with progress indication.

```python
if installer.download_with_progress("https://example.com/file", Path("file")):
    print("Download completed")
else:
    print("Download failed")
```

##### `extract_if_compressed(file_path: Path) -> Optional[Path]`
Extract compressed files and return the extracted binary path.

```python
extracted = installer.extract_if_compressed(Path("file.tar.gz"))
if extracted:
    print(f"Extracted to: {extracted}")
```

##### `install_wireguard_tools() -> bool`
Install WireGuard tools based on the OS.

```python
if installer.install_wireguard_tools():
    print("WireGuard tools installed")
else:
    print("WireGuard installation failed")
```

### WGCFManager

Manage wgcf installation and configuration.

```python
from utils.wgcf_manager import WGCFManager

wgcf = WGCFManager()
```

#### Methods

##### `download_wgcf() -> bool`
Download the latest wgcf binary.

```python
if wgcf.download_wgcf():
    print("WGCF downloaded")
else:
    print("WGCF download failed")
```

##### `register_account() -> bool`
Register a new WARP account.

```python
if wgcf.register_account():
    print("WARP account registered")
else:
    print("Registration failed")
```

##### `generate_profile() -> bool`
Generate WireGuard profile from account.

```python
if wgcf.generate_profile():
    print("Profile generated")
else:
    print("Profile generation failed")
```

##### `modify_profile_for_nextdns() -> bool`
Modify WireGuard profile to use NextDNS.

```python
if wgcf.modify_profile_for_nextdns():
    print("Profile modified for NextDNS")
else:
    print("Profile modification failed")
```

##### `install_profile() -> bool`
Install WireGuard profile to system directory.

```python
if wgcf.install_profile():
    print("Profile installed")
else:
    print("Profile installation failed")
```

##### `get_status() -> Dict[str, bool]`
Get current status of wgcf setup.

```python
status = wgcf.get_status()
print(f"Binary exists: {status['wgcf_binary']}")
print(f"Account registered: {status['account_registered']}")
print(f"Profile generated: {status['profile_generated']}")
print(f"Profile installed: {status['profile_installed']}")
```

### NextDNSManager

Manage NextDNS installation and configuration.

```python
from utils.nextdns_manager import NextDNSManager

nextdns = NextDNSManager()
```

#### Methods

##### `is_installed() -> bool`
Check if NextDNS is installed.

```python
if nextdns.is_installed():
    print("NextDNS is installed")
else:
    print("NextDNS not found")
```

##### `is_configured() -> bool`
Check if NextDNS is configured.

```python
if nextdns.is_configured():
    print("NextDNS is configured")
else:
    print("NextDNS not configured")
```

##### `get_status() -> Dict[str, any]`
Get NextDNS status.

```python
status = nextdns.get_status()
print(f"Installed: {status['installed']}")
print(f"Running: {status['running']}")
print(f"Configured: {status['configured']}")
```

##### `install() -> bool`
Install NextDNS using the official script.

```python
if nextdns.install():
    print("NextDNS installed")
else:
    print("NextDNS installation failed")
```

##### `configure(profile_id: str, arguments: Optional[str] = None) -> bool`
Configure NextDNS with profile ID.

```python
if nextdns.configure("your-profile-id"):
    print("NextDNS configured")
else:
    print("NextDNS configuration failed")
```

##### `start() -> bool`
Start NextDNS service.

```python
if nextdns.start():
    print("NextDNS started")
else:
    print("NextDNS start failed")
```

##### `stop() -> bool`
Stop NextDNS service.

```python
if nextdns.stop():
    print("NextDNS stopped")
else:
    print("NextDNS stop failed")
```

##### `restart() -> bool`
Restart NextDNS service.

```python
if nextdns.restart():
    print("NextDNS restarted")
else:
    print("NextDNS restart failed")
```

##### `get_logs(lines: int = 50) -> str`
Get NextDNS logs.

```python
logs = nextdns.get_logs(100)
print(logs)
```

##### `test_connection() -> bool`
Test if NextDNS is working properly.

```python
if nextdns.test_connection():
    print("NextDNS connection working")
else:
    print("NextDNS connection failed")
```

## 🔌 Integration Examples

### Basic Integration

```python
from core import EnhancedWARPManager

def setup_warp_nextdns(profile_id: str):
    """Setup WARP + NextDNS with error handling."""
    manager = EnhancedWARPManager()
    
    try:
        # Ensure elevation
        if not manager.ensure_elevation():
            raise RuntimeError("Elevated privileges required")
        
        # Install dependencies
        deps = manager.install_dependencies()
        if not all(deps.values()):
            raise RuntimeError("Dependency installation failed")
        
        # Setup WGCF
        wgcf_result = manager.setup_wgcf()
        if not wgcf_result['success']:
            raise RuntimeError(f"WGCF setup failed: {wgcf_result['error']}")
        
        # Setup NextDNS
        nextdns_result = manager.setup_nextdns_config(profile_id)
        if not nextdns_result['success']:
            raise RuntimeError(f"NextDNS setup failed: {nextdns_result['error']}")
        
        # Start services
        start_results = manager.start_services()
        if not all(start_results.values()):
            raise RuntimeError("Service startup failed")
        
        # Test connectivity
        test_results = manager.test_connection()
        if not all(test_results.values()):
            raise RuntimeError("Connectivity test failed")
        
        return True
        
    except Exception as e:
        print(f"Setup failed: {e}")
        return False

# Usage
if setup_warp_nextdns("your-profile-id"):
    print("Setup completed successfully")
else:
    print("Setup failed")
```

### Monitoring Integration

```python
import time
from core import EnhancedWARPManager

def monitor_services():
    """Monitor WARP + NextDNS services."""
    manager = EnhancedWARPManager()
    
    while True:
        try:
            # Get status
            status = manager.get_status()
            
            # Check WGCF
            if not status['wgcf']['running']:
                print("WGCF is down, restarting...")
                manager.start_services()
            
            # Check NextDNS
            if not status['nextdns']['running']:
                print("NextDNS is down, restarting...")
                manager.start_services()
            
            # Test connectivity
            test_results = manager.test_connection()
            if not test_results['warp'] or not test_results['nextdns']:
                print("Connectivity issues detected")
                manager.restart_services()
            
            time.sleep(60)  # Check every minute
            
        except Exception as e:
            print(f"Monitoring error: {e}")
            time.sleep(30)

# Start monitoring
monitor_services()
```

### Web API Integration

```python
from flask import Flask, jsonify
from core import EnhancedWARPManager

app = Flask(__name__)
manager = EnhancedWARPManager()

@app.route('/status')
def get_status():
    """Get system status."""
    try:
        status = manager.get_status()
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test')
def test_connectivity():
    """Test connectivity."""
    try:
        results = manager.test_connection()
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/start', methods=['POST'])
def start_services():
    """Start services."""
    try:
        results = manager.start_services()
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stop', methods=['POST'])
def stop_services():
    """Stop services."""
    try:
        results = manager.stop_services()
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

### Docker Integration

```dockerfile
FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    wireguard-tools \
    curl \
    dnsutils \
    && rm -rf /var/lib/apt/lists/*

# Copy application
COPY . /app
WORKDIR /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Create non-root user
RUN useradd -m -s /bin/bash warpuser
USER warpuser

# Expose API port
EXPOSE 8080

# Start API server
CMD ["python", "api_server.py"]
```

## 📊 Error Handling

### Exception Types

```python
# RuntimeError - General runtime errors
try:
    manager.setup_wgcf()
except RuntimeError as e:
    print(f"Setup failed: {e}")

# FileNotFoundError - Missing files
try:
    manager.install_profile()
except FileNotFoundError as e:
    print(f"File not found: {e}")

# PermissionError - Permission issues
try:
    manager.start_services()
except PermissionError as e:
    print(f"Permission denied: {e}")
```

### Error Recovery

```python
def robust_setup(profile_id: str, max_retries: int = 3):
    """Robust setup with retry logic."""
    manager = EnhancedWARPManager()
    
    for attempt in range(max_retries):
        try:
            # Setup with error handling
            if manager.setup_wgcf()['success']:
                break
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)  # Wait before retry
            else:
                raise RuntimeError(f"Setup failed after {max_retries} attempts")
```

## 🔐 Security Considerations

### Privilege Management

```python
# Check privileges before operations
if not manager.platform.check_root_access():
    print("Elevated privileges required")
    sys.exit(1)

# Use minimal privileges when possible
manager.setup_auto_start()  # May require elevation
```

### Input Validation

```python
import re

def validate_profile_id(profile_id: str) -> bool:
    """Validate NextDNS profile ID."""
    pattern = r'^[a-f0-9]{6}$'
    return bool(re.match(pattern, profile_id))

# Usage
if not validate_profile_id(profile_id):
    raise ValueError("Invalid profile ID format")
```

## 📚 Best Practices

### Resource Management

```python
# Use context managers for cleanup
def setup_with_cleanup(profile_id: str):
    manager = EnhancedWARPManager()
    try:
        # Setup operations
        manager.setup_wgcf()
        manager.setup_nextdns_config(profile_id)
        return True
    except Exception as e:
        # Cleanup on failure
        manager.cleanup()
        raise e
    finally:
        # Always cleanup temporary files
        manager.installer.cleanup_temp_files()
```

### Logging

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Use in your application
logger = logging.getLogger(__name__)

def setup_with_logging(profile_id: str):
    logger.info("Starting WARP + NextDNS setup")
    try:
        # Setup operations
        logger.info("Setup completed successfully")
    except Exception as e:
        logger.error(f"Setup failed: {e}")
        raise
```

## 📖 Next Steps

After learning the API:

1. **[Usage Guide](usage.md)** - Learn how to use the tool
2. **[Configuration Guide](configuration.md)** - Advanced configuration
3. **[Troubleshooting Guide](troubleshooting.md)** - Solve common issues

---

**Need help?** Check our [troubleshooting guide](troubleshooting.md) or [create an issue](https://github.com/nightcodex7/warp-nextdns-wireguard/issues). 