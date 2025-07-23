#!/usr/bin/env python3
"""
Unified Cross-Platform Launcher for WARP + NextDNS Manager
Automatically detects operating system and launches the appropriate interface
"""

import os
import sys
import platform
import subprocess
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

def get_executable_path():
    """Get the path to the appropriate executable"""
    platform_name = detect_platform()
    script_dir = Path(__file__).parent
    
    if platform_name == "windows":
        # Check for Windows executable
        exe_path = script_dir / "release" / "windows" / "warp-nextdns-manager.exe"
        if exe_path.exists():
            return str(exe_path)
        
        # Fallback to Python script
        return str(script_dir / "main.py")
    
    elif platform_name == "linux":
        # Check for Linux executable
        exe_path = script_dir / "release" / "linux" / "warp-nextdns-manager"
        if exe_path.exists():
            return str(exe_path)
        
        # Fallback to Python script
        return str(script_dir / "main.py")
    
    elif platform_name == "macos":
        # macOS not supported, but provide helpful message
        print("❌ macOS is not supported by this application.")
        print("This tool is designed for Windows and Linux only.")
        return None
    
    else:
        print(f"❌ Unsupported platform: {platform_name}")
        return None

def check_dependencies():
    """Check if required dependencies are available"""
    try:
        import rich
        import requests
        import cryptography
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install required dependencies:")
        print("pip install -r requirements.txt")
        return False

def main():
    """Main launcher function"""
    print("🚀 WARP + NextDNS Manager - Cross-Platform Launcher")
    print("=" * 50)
    
    # Detect platform
    platform_name = detect_platform()
    print(f"📋 Detected platform: {platform_name}")
    
    # Check if macOS (not supported)
    if platform_name == "macos":
        print("\n❌ macOS is not supported by this application.")
        print("This tool is designed for Windows and Linux only.")
        print("Please use a supported platform.")
        sys.exit(1)
    
    # Get executable path
    executable_path = get_executable_path()
    if not executable_path:
        print("❌ Could not find appropriate executable")
        sys.exit(1)
    
    print(f"🎯 Using: {executable_path}")
    
    # Check dependencies if using Python script
    if executable_path.endswith("main.py"):
        if not check_dependencies():
            sys.exit(1)
    
    # Prepare command
    if len(sys.argv) > 1:
        # Pass through all arguments
        cmd = [executable_path] + sys.argv[1:]
    else:
        # Default to interactive mode
        cmd = [executable_path, "interactive"]
    
    print(f"🚀 Launching: {' '.join(cmd)}")
    print()
    
    try:
        # Launch the application
        result = subprocess.run(cmd)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\n👋 Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Failed to launch application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 