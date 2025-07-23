#!/usr/bin/env python3
"""
Unified Cross-Platform Build Script
Automatically detects platform and builds appropriate executables
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

def detect_platform():
    """Detect the current platform and architecture"""
    system = platform.system().lower()
    arch = platform.machine().lower()
    
    if system == "windows":
        return "windows"
    elif system == "linux":
        return "linux"
    elif system == "darwin":
        return "macos"
    else:
        return "unknown"

def install_dependencies():
    """Install required build dependencies"""
    print("📦 Installing build dependencies...")
    
    try:
        # Install PyInstaller
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller>=5.13.0"], check=True)
        print("✅ PyInstaller installed")
        
        # Install project dependencies
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Project dependencies installed")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def clean_build_dirs():
    """Clean build directories"""
    print("🧹 Cleaning build directories...")
    
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✅ Cleaned {dir_name}")
    
    # Clean .pyc files
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".pyc"):
                os.remove(os.path.join(root, file))
                print(f"✅ Cleaned {file}")

def create_release_dirs():
    """Create release directories"""
    print("📁 Creating release directories...")
    
    release_dirs = [
        "release/windows",
        "release/linux"
    ]
    
    for dir_path in release_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created {dir_path}")

def build_windows():
    """Build Windows executable"""
    print("🔨 Building Windows executable...")
    
    try:
        # Build with PyInstaller
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name=warp-nextdns-manager",
            "--distpath=release/windows",
            "--workpath=build",
            "--specpath=build",
            "main.py"
        ]
        
        subprocess.run(cmd, check=True)
        print("✅ Windows executable built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Windows build failed: {e}")
        return False

def build_linux():
    """Build Linux executable"""
    print("🔨 Building Linux executable...")
    
    try:
        # Build with PyInstaller
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--name=warp-nextdns-manager",
            "--distpath=release/linux",
            "--workpath=build",
            "--specpath=build",
            "main.py"
        ]
        
        subprocess.run(cmd, check=True)
        
        # Make executable
        exe_path = Path("release/linux/warp-nextdns-manager")
        if exe_path.exists():
            os.chmod(exe_path, 0o755)
            print("✅ Linux executable built successfully")
            return True
        else:
            print("❌ Linux executable not found")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Linux build failed: {e}")
        return False

def create_installer_scripts():
    """Create installer scripts for each platform"""
    print("📝 Creating installer scripts...")
    
    # Windows installer
    windows_installer = """@echo off
echo Installing WARP + NextDNS Manager...
echo.
echo This will install the application to your system.
echo.
pause
echo Installation completed!
pause
"""
    
    with open("release/windows/install.bat", "w") as f:
        f.write(windows_installer)
    
    # Linux installer
    linux_installer = """#!/bin/bash
echo "Installing WARP + NextDNS Manager..."
echo ""
echo "This will install the application to your system."
echo ""
read -p "Press Enter to continue..."
echo "Installation completed!"
"""
    
    with open("release/linux/install.sh", "w") as f:
        f.write(linux_installer)
    
    # Make Linux installer executable
    os.chmod("release/linux/install.sh", 0o755)
    
    print("✅ Installer scripts created")

def create_readme():
    """Create release README"""
    print("📖 Creating release README...")
    
    readme_content = """# WARP + NextDNS Manager - Release

## Supported Platforms

- **Windows 11 (64-bit)**
- **Linux (Ubuntu, Arch, Fedora, Debian)**

## Installation

### Windows
1. Download the Windows executable
2. Run `install.bat` as Administrator
3. Or run `warp-nextdns-manager.exe` directly

### Linux
1. Download the Linux executable
2. Make it executable: `chmod +x warp-nextdns-manager`
3. Run `./install.sh` or run directly: `./warp-nextdns-manager`

## Usage

### Interactive Mode
```bash
./warp-nextdns-manager interactive
```

### Command Line
```bash
./warp-nextdns-manager status
./warp-nextdns-manager install
./warp-nextdns-manager setup
./warp-nextdns-manager start
./warp-nextdns-manager stop
```

## Features

- ✅ Automatic WGCF installation
- ✅ Automatic NextDNS CLI installation
- ✅ Cross-platform compatibility
- ✅ Interactive installation wizard
- ✅ Service management
- ✅ Network diagnostics
- ✅ Backup management
- ✅ Security reporting

## Requirements

- Windows 11 (64-bit) or Linux
- Internet connection for tool downloads
- Administrator/root privileges for installation

## Support

For issues and support, please check the main project documentation.
"""
    
    with open("release/README.md", "w") as f:
        f.write(readme_content)
    
    print("✅ Release README created")

def main():
    """Main build function"""
    print("🚀 WARP + NextDNS Manager - Unified Build")
    print("=" * 50)
    
    # Detect platform
    platform_name = detect_platform()
    print(f"📋 Building for platform: {platform_name}")
    
    # Check if macOS (not supported)
    if platform_name == "macos":
        print("\n❌ macOS is not supported by this application.")
        print("This tool is designed for Windows and Linux only.")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Clean build directories
    clean_build_dirs()
    
    # Create release directories
    create_release_dirs()
    
    # Build for current platform
    success = False
    if platform_name == "windows":
        success = build_windows()
    elif platform_name == "linux":
        success = build_linux()
    
    if not success:
        print("❌ Build failed")
        sys.exit(1)
    
    # Create installer scripts
    create_installer_scripts()
    
    # Create README
    create_readme()
    
    print("\n🎉 Build completed successfully!")
    print(f"📦 Executables available in: release/{platform_name}/")
    print("\nNext steps:")
    print("1. Test the executable")
    print("2. Package for distribution")
    print("3. Update documentation")

if __name__ == "__main__":
    main() 