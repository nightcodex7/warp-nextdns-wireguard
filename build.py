#!/usr/bin/env python3
"""
Build script for WARP + NextDNS Manager
Creates executable files and handles releases
"""

import os
import sys
import subprocess
import platform
import shutil
import zipfile
import tarfile
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

class Builder:
    """Build system for WARP + NextDNS Manager"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.version = self.get_version()
        self.system = platform.system().lower()
        self.arch = platform.machine().lower()
        self.build_dir = self.project_root / "build"
        self.dist_dir = self.project_root / "dist"
        self.release_dir = self.project_root / "release"
        
    def get_version(self) -> str:
        """Get version from VERSION file"""
        version_file = self.project_root / "VERSION"
        if version_file.exists():
            return version_file.read_text().strip()
        return "1.0.0"
    
    def get_architecture(self) -> str:
        """Get system architecture"""
        arch_map = {
            'x86_64': 'amd64',
            'AMD64': 'amd64',
            'aarch64': 'arm64',
            'arm64': 'arm64',
            'i386': 'i386',
            'i686': 'i386'
        }
        return arch_map.get(self.arch, self.arch)
    
    def clean(self):
        """Clean build artifacts"""
        print("🧹 Cleaning build artifacts...")
        
        dirs_to_clean = [
            self.build_dir,
            self.dist_dir,
            self.project_root / "__pycache__",
            self.project_root / "*.egg-info"
        ]
        
        for path in dirs_to_clean:
            if path.exists():
                if path.is_dir():
                    shutil.rmtree(path, ignore_errors=True)
                else:
                    path.unlink(missing_ok=True)
        
        # Clean glob patterns
        for pattern in ["*.egg-info", "*.spec"]:
            for path in self.project_root.glob(pattern):
                if path.is_dir():
                    shutil.rmtree(path, ignore_errors=True)
                else:
                    path.unlink(missing_ok=True)
    
    def install_dependencies(self):
        """Install build dependencies"""
        print("📦 Installing build dependencies...")
        
        # Install PyInstaller if not present
        try:
            import PyInstaller
        except ImportError:
            self.run_command("pip install pyinstaller")
        
        # Install other build tools
        self.run_command("pip install -r requirements.txt")
    
    def run_command(self, cmd: str, check: bool = True) -> Optional[str]:
        """Run a command and handle errors"""
        try:
            print(f"Running: {cmd}")
            result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {cmd}")
            print(f"Error: {e.stderr}")
            if check:
                sys.exit(1)
            return None
    
    def build_executable(self):
        """Build executable using PyInstaller"""
        print("🔨 Building executable...")
        
        # Create build directories
        self.build_dir.mkdir(exist_ok=True)
        self.dist_dir.mkdir(exist_ok=True)
        
        # PyInstaller command
        cmd_parts = [
            "pyinstaller",
            "--onefile",
            "--name=warp-nextdns-manager",
            f"--version-file=VERSION",
            "--add-data=utils:utils",
            "--hidden-import=click",
            "--hidden-import=rich",
            "--hidden-import=requests",
            "--hidden-import=yaml",
            "--hidden-import=psutil",
            "--hidden-import=utils.platform_utils",
            "--hidden-import=utils.installer_manager",
            "--hidden-import=utils.wgcf_manager",
            "--hidden-import=utils.nextdns_manager",
            "--hidden-import=utils.error_handler",
            "--hidden-import=utils.navigation_manager",
            "--hidden-import=utils.backup_manager",
            "--hidden-import=utils.network_monitor",
            "--hidden-import=utils.security_manager",
            "--hidden-import=utils.auto_responder",
            "cli.py"
        ]
        
        if self.system == "windows":
            cmd_parts.extend(["--windowed"])
        
        cmd = " ".join(cmd_parts)
        self.run_command(cmd)
        
        # Move executable to release directory
        self.release_dir.mkdir(exist_ok=True)
        platform_dir = self.release_dir / self.system
        platform_dir.mkdir(exist_ok=True)
        
        executable_name = "warp-nextdns-manager"
        if self.system == "windows":
            executable_name += ".exe"
        
        source = self.dist_dir / executable_name
        if source.exists():
            dest = platform_dir / executable_name
            shutil.move(str(source), str(dest))
            print(f"✅ Executable created: {dest}")
        else:
            print(f"❌ Executable not found: {source}")
    
    def create_install_scripts(self):
        """Create platform-specific install scripts"""
        print("📝 Creating install scripts...")
        
        # Windows install script
        if self.system == "windows":
            install_script = self.release_dir / "windows" / "install.bat"
            install_content = f"""@echo off
echo Installing WARP + NextDNS Manager...
echo Version: {self.version}
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running as administrator
) else (
    echo Please run as administrator
    pause
    exit /b 1
)

REM Install Python dependencies
pip install -r requirements.txt

REM Make executable
warp-nextdns-manager.exe setup --auto

echo.
echo Installation completed!
pause
"""
            install_script.write_text(install_content)
        
        # Linux install script
        else:
            install_script = self.release_dir / "linux" / "install.sh"
            install_content = f"""#!/bin/bash
echo "Installing WARP + NextDNS Manager..."
echo "Version: {self.version}"
echo

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (use sudo)"
    exit 1
fi

# Install Python dependencies
pip3 install -r requirements.txt

# Make executable
chmod +x warp-nextdns-manager
./warp-nextdns-manager setup --auto

echo
echo "Installation completed!"
"""
            install_script.write_text(install_content)
            # Make executable
            install_script.chmod(0o755)
    
    def create_archive(self):
        """Create release archive"""
        print("📦 Creating release archive...")
        
        arch_name = f"warp-nextdns-manager-{self.version}-{self.system}-{self.get_architecture()}"
        archive_path = self.release_dir / f"{arch_name}.zip"
        
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add executable
            platform_dir = self.release_dir / self.system
            for file in platform_dir.iterdir():
                if file.is_file():
                    zipf.write(file, file.name)
            
            # Add install script
            install_script = platform_dir / ("install.bat" if self.system == "windows" else "install.sh")
            if install_script.exists():
                zipf.write(install_script, install_script.name)
            
            # Add README
            readme = self.project_root / "README.md"
            if readme.exists():
                zipf.write(readme, "README.md")
            
            # Add requirements
            requirements = self.project_root / "requirements.txt"
            if requirements.exists():
                zipf.write(requirements, "requirements.txt")
        
        print(f"✅ Archive created: {archive_path}")
    
    def create_changelog(self):
        """Create changelog for release"""
        print("📋 Creating changelog...")
        
        changelog_file = self.project_root / "CHANGELOG.md"
        if changelog_file.exists():
            changelog_content = changelog_file.read_text()
            
            # Extract version section
            lines = changelog_content.split('\n')
            version_section = []
            in_version = False
            
            for line in lines:
                if line.startswith(f"## [{self.version}]"):
                    in_version = True
                    version_section.append(line)
                elif in_version and line.startswith("## ["):
                    break
                elif in_version:
                    version_section.append(line)
            
            if version_section:
                changelog = '\n'.join(version_section).strip()
                changelog_file = self.release_dir / "CHANGELOG.md"
                changelog_file.write_text(changelog)
                print(f"✅ Changelog created: {changelog_file}")
    
    def build(self):
        """Complete build process"""
        print(f"🚀 Starting build for {self.system} {self.get_architecture()}")
        print(f"Version: {self.version}")
        print()
        
        try:
            # Clean previous builds
            self.clean()
            
            # Install dependencies
            self.install_dependencies()
            
            # Build executable
            self.build_executable()
            
            # Create install scripts
            self.create_install_scripts()
            
            # Create archive
            self.create_archive()
            
            # Create changelog
            self.create_changelog()
            
            print()
            print("🎉 Build completed successfully!")
            print(f"Release files: {self.release_dir}")
            
        except Exception as e:
            print(f"❌ Build failed: {e}")
            sys.exit(1)

def main():
    """Main build function"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        builder = Builder()
        
        if command == "clean":
            builder.clean()
        elif command == "deps":
            builder.install_dependencies()
        elif command == "build":
            builder.build_executable()
        elif command == "archive":
            builder.create_archive()
        elif command == "full":
            builder.build()
        else:
            print(f"Unknown command: {command}")
            print("Available commands: clean, deps, build, archive, full")
            sys.exit(1)
    else:
        # Default: full build
        builder = Builder()
        builder.build()

if __name__ == "__main__":
    main()
