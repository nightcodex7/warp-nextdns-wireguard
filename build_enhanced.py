#!/usr/bin/env python3
"""
Enhanced Build Script for WARP + NextDNS Manager
Handles cross-platform builds, elevated permissions, and release management
"""

import os
import sys
import platform
import subprocess
import shutil
import json
import zipfile
from pathlib import Path
from datetime import datetime
import argparse

def is_admin():
    """Check if running with elevated permissions"""
    try:
        if platform.system().lower() == "windows":
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            return os.geteuid() == 0
    except:
        return False

def request_elevation():
    """Request elevated permissions"""
    if is_admin():
        return True
    
    print("Elevated permissions required for installation.")
    if platform.system().lower() == "windows":
        print("Please run as Administrator")
    else:
        print("Please run with sudo")
    return False

def get_version():
    """Get version from version_info.txt"""
    try:
        with open('version_info.txt', 'r') as f:
            return f.read().strip()
    except:
        return "2.0.0"

def clean_build():
    """Clean build artifacts"""
    print("Cleaning build artifacts...")
    
    # Remove build directories
    dirs_to_clean = ['build', 'dist', '__pycache__', '.pytest_cache']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  Removed {dir_name}")
    
    # Remove spec files
    spec_files = [f for f in os.listdir('.') if f.endswith('.spec')]
    for spec_file in spec_files:
        os.remove(spec_file)
        print(f"  Removed {spec_file}")

def install_dependencies():
    """Install build dependencies"""
    print("Installing build dependencies...")
    
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], check=True)
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
        print("  Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  Error installing dependencies: {e}")
        return False

def build_executable():
    """Build executable for current platform"""
    system = platform.system().lower()
    arch = platform.machine().lower()
    version = get_version()
    
    print(f"Building executable for {system} {arch}...")
    
    # PyInstaller options
    options = [
        '--onefile',
        '--clean',
        '--noconfirm'
    ]
    
    if system == "windows":
        options.extend([
            '--name', f'WARP_NextDNS_Manager_v{version}',
            '--icon', 'static/icon.ico'
        ])
    else:
        options.extend([
            '--name', f'warp-nextdns-manager-v{version}'
        ])
    
    # Add data files
    if os.path.exists('static'):
        options.extend(['--add-data', 'static:static'])
    if os.path.exists('templates'):
        options.extend(['--add-data', 'templates:templates'])
    
    # Build command
    cmd = [sys.executable, '-m', 'PyInstaller'] + options + ['cli.py']
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("  Build completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  Build failed: {e}")
        print(f"  Error output: {e.stderr}")
        return False

def create_release_package():
    """Create release package with executable and changelog"""
    system = platform.system().lower()
    version = get_version()
    
    print("Creating release package...")
    
    # Create release directory
    release_dir = f'release/WARP_NextDNS_Manager_{system.capitalize()}_v{version}'
    os.makedirs(release_dir, exist_ok=True)
    
    # Copy executable
    if system == "windows":
        exe_name = f'WARP_NextDNS_Manager_v{version}.exe'
        exe_path = f'dist/{exe_name}'
    else:
        exe_name = f'warp-nextdns-manager-v{version}'
        exe_path = f'dist/{exe_name}'
    
    if os.path.exists(exe_path):
        shutil.copy2(exe_path, release_dir)
        print(f"  Copied {exe_name}")
    else:
        print(f"  Warning: {exe_path} not found")
    
    # Create changelog
    changelog_content = f"""# WARP + NextDNS Manager v{version}

## Release Notes

### Version {version} - {datetime.now().strftime('%Y-%m-%d')}

### New Features
- Enhanced installation with elevated permissions
- Automatic tool detection and installation
- Improved navigation and user experience
- Cross-platform compatibility improvements
- Auto-responder functionality for automated operations

### Improvements
- Better error handling and recovery
- Enhanced security features
- Improved backup management
- Network diagnostics and monitoring
- Comprehensive logging system

### Bug Fixes
- Fixed navigation issues in interactive mode
- Resolved tool installation problems
- Improved platform detection
- Enhanced error reporting

### System Requirements
- Windows 11 (64-bit) or Linux
- Python 3.8 or higher
- Internet connection for tool downloads

### Installation
1. Extract the package
2. Run the executable with elevated permissions
3. Follow the interactive setup

### Usage
```bash
# Interactive mode
./warp-nextdns-manager

# Command line mode
./warp-nextdns-manager status
./warp-nextdns-manager auto-install
./warp-nextdns-manager setup
```

### Support
For issues and support, please visit the GitHub repository.
"""
    
    with open(f'{release_dir}/CHANGELOG.md', 'w', encoding='utf-8') as f:
        f.write(changelog_content)
    print("  Created CHANGELOG.md")
    
    # Create README
    readme_content = f"""# WARP + NextDNS Manager v{version}

Enhanced WARP + NextDNS Manager with automatic installation and elevated permissions.

## Quick Start

1. **Extract** this package
2. **Run** the executable with elevated permissions
3. **Follow** the interactive setup

## Features

- ✅ Automatic tool installation with elevated permissions
- ✅ Cross-platform support (Windows 11, Linux)
- ✅ Enhanced navigation and user experience
- ✅ Network diagnostics and monitoring
- ✅ Backup and restore functionality
- ✅ Security reporting and validation

## Commands

- `status` - Show system status
- `auto-install` - Automatic installation
- `setup` - Interactive setup
- `start` - Start services
- `stop` - Stop services
- `network` - Network diagnostics
- `backup` - Backup management
- `tools` - Manage tools

## System Requirements

- Windows 11 (64-bit) or Linux
- Internet connection
- Elevated permissions for installation

## Support

Visit the GitHub repository for documentation and support.
"""
    
    with open(f'{release_dir}/README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("  Created README.md")
    
    # Create launcher script
    if system == "windows":
        launcher_content = f"""@echo off
echo Starting WARP + NextDNS Manager v{version}...
echo.
echo Please run this as Administrator for full functionality.
echo.
pause
start "" "{exe_name}"
"""
        with open(f'{release_dir}/launch.bat', 'w') as f:
            f.write(launcher_content)
        print("  Created launch.bat")
    else:
        launcher_content = f"""#!/bin/bash
echo "Starting WARP + NextDNS Manager v{version}..."
echo ""
echo "Please run with sudo for full functionality."
echo ""
read -p "Press Enter to continue..."
./{exe_name}
"""
        with open(f'{release_dir}/launch.sh', 'w') as f:
            f.write(launcher_content)
        os.chmod(f'{release_dir}/launch.sh', 0o755)
        print("  Created launch.sh")
    
    return release_dir

def create_zip_package(release_dir):
    """Create ZIP package for release"""
    print("Creating ZIP package...")
    
    zip_name = f'{os.path.basename(release_dir)}.zip'
    zip_path = f'release/{zip_name}'
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(release_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, release_dir)
                zipf.write(file_path, arc_name)
    
    print(f"  Created {zip_name}")
    return zip_path

def main():
    """Main build function"""
    parser = argparse.ArgumentParser(description='Enhanced Build Script')
    parser.add_argument('--clean', action='store_true', help='Clean build artifacts')
    parser.add_argument('--install', action='store_true', help='Install dependencies')
    parser.add_argument('--build', action='store_true', help='Build executable')
    parser.add_argument('--package', action='store_true', help='Create release package')
    parser.add_argument('--all', action='store_true', help='Run all steps')
    parser.add_argument('--elevated', action='store_true', help='Request elevated permissions')
    
    args = parser.parse_args()
    
    # Check for elevated permissions if requested
    if args.elevated and not is_admin():
        if not request_elevation():
            return 1
    
    # Run requested steps
    if args.clean or args.all:
        clean_build()
    
    if args.install or args.all:
        if not install_dependencies():
            return 1
    
    if args.build or args.all:
        if not build_executable():
            return 1
    
    if args.package or args.all:
        release_dir = create_release_package()
        zip_path = create_zip_package(release_dir)
        print(f"\n✅ Build completed successfully!")
        print(f"Release package: {zip_path}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 