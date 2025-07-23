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
from pathlib import Path
from datetime import datetime

def run_command(cmd, check=True):
    """Run a command and handle errors"""
    try:
        result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {cmd}")
        print(f"Error: {e.stderr}")
        if check:
            sys.exit(1)
        return None

def get_version():
    """Get version from VERSION file"""
    with open("VERSION", "r") as f:
        return f.read().strip()

def clean_build():
    """Clean build artifacts"""
    print("🧹 Cleaning build artifacts...")
    
    # Remove build directories
    dirs_to_clean = ["build", "dist", "__pycache__", "*.egg-info"]
    for pattern in dirs_to_clean:
        if "*" in pattern:
            for path in Path(".").glob(pattern):
                if path.is_dir():
                    shutil.rmtree(path, ignore_errors=True)
                else:
                    path.unlink(missing_ok=True)
        else:
            path = Path(pattern)
            if path.exists():
                shutil.rmtree(path, ignore_errors=True)

def install_dependencies():
    """Install build dependencies"""
    print("Installing build dependencies...")
    
    # Install PyInstaller if not present
    try:
        import PyInstaller
    except ImportError:
        run_command("pip install pyinstaller")
    
    # Install other build tools
    run_command("pip install -r requirements.txt")

def build_executable():
    """Build executable using PyInstaller"""
    print("Building executable...")
    
    version = get_version()
    system = platform.system().lower()
    arch = platform.machine().lower()
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name=warp-nextdns",
        f"--version-file=VERSION",
        "--add-data=utils:utils",
        "--hidden-import=click",
        "--hidden-import=rich",
        "--hidden-import=requests",
        "--hidden-import=yaml",
        "--hidden-import=psutil",
        "cli.py"
    ]
    
    if system == "windows":
        cmd.extend(["--windowed"])
    
    run_command(" ".join(cmd))
    
    # Move executable to dist directory
    dist_dir = Path("dist")
    dist_dir.mkdir(exist_ok=True)
    
    executable_name = "warp-nextdns"
    if system == "windows":
        executable_name += ".exe"
    
    source = Path("dist") / executable_name
    if source.exists():
        print(f"✅ Executable built: {source}")
        return source
    else:
        print("❌ Executable build failed")
        return None

def create_changelog():
    """Create changelog from git commits"""
    print("Creating changelog...")
    
    version = get_version()
    
    # Get commits since last tag
    try:
        commits = run_command(f"git log --oneline --since='$(git describe --tags --abbrev=0 2>/dev/null || echo HEAD~10)'")
    except:
        commits = run_command("git log --oneline -10")
    
    changelog_content = f"""# Changelog for v{version}

## Release Date: {datetime.now().strftime('%Y-%m-%d')}

### Changes:
"""
    
    if commits:
        for commit in commits.split('\n'):
            if commit.strip():
                changelog_content += f"- {commit.strip()}\n"
    
    changelog_content += f"""
### System Requirements:
- Python 3.7+
- Linux, Windows, or macOS
- Elevated privileges for installation

### Installation:
1. Download the appropriate executable for your system
2. Run with elevated privileges (sudo/admin)
3. Follow the setup wizard

### Features:
- Automatic WGCF installation and configuration
- NextDNS integration
- Cross-platform support
- Auto-start configuration
- Service management
"""
    
    with open("CHANGELOG.md", "w") as f:
        f.write(changelog_content)
    
    print("✅ Changelog created: CHANGELOG.md")
    return "CHANGELOG.md"

def create_release_assets():
    """Create release assets"""
    print("Creating release assets...")
    
    version = get_version()
    system = platform.system().lower()
    arch = platform.machine().lower()
    
    # Create release directory
    release_dir = Path(f"release-v{version}")
    release_dir.mkdir(exist_ok=True)
    
    # Copy executable
    executable = build_executable()
    if executable:
        shutil.copy2(executable, release_dir / executable.name)
    
    # Copy changelog
    changelog = create_changelog()
    if changelog:
        shutil.copy2(changelog, release_dir / "CHANGELOG.md")
    
    # Copy README
    shutil.copy2("README.md", release_dir / "README.md")
    
    # Create install script
    install_script = f"""#!/bin/bash
# WARP + NextDNS Manager Installer v{version}

echo "Installing WARP + NextDNS Manager v{version}..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (sudo)"
    exit 1
fi

# Copy executable to /usr/local/bin
cp warp-nextdns /usr/local/bin/
chmod +x /usr/local/bin/warp-nextdns

echo "Installation complete!"
echo "Run 'warp-nextdns setup' to configure"
"""
    
    with open(release_dir / "install.sh", "w") as f:
        f.write(install_script)
    
    os.chmod(release_dir / "install.sh", 0o755)
    
    print(f"✅ Release assets created in: {release_dir}")
    return release_dir

def create_github_release():
    """Create GitHub release"""
    print("Creating GitHub release...")
    
    version = get_version()
    
    # Create git tag
    run_command(f"git tag v{version}")
    run_command(f"git push origin v{version}")
    
    # Create release assets
    release_dir = create_release_assets()
    
    # Create release using GitHub CLI (if available)
    if shutil.which("gh"):
        title = f"WARP + NextDNS Manager v{version}"
        body = f"""## What's New in v{version}

This release includes:
- Enhanced installation process
- Automatic privilege elevation
- Improved cross-platform support
- Better error handling and logging

## Installation

1. Download the appropriate executable for your system
2. Run with elevated privileges
3. Follow the setup wizard

See CHANGELOG.md for detailed changes.
"""
        
        cmd = f'gh release create v{version} --title "{title}" --notes "{body}" --draft'
        run_command(cmd)
        
        # Upload assets
        for asset in release_dir.glob("*"):
            if asset.is_file():
                run_command(f'gh release upload v{version} "{asset}"')
    
    print("✅ GitHub release created")

def main():
    """Main build function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Build WARP + NextDNS Manager")
    parser.add_argument("--clean", action="store_true", help="Clean build artifacts")
    parser.add_argument("--build", action="store_true", help="Build executable")
    parser.add_argument("--release", action="store_true", help="Create release assets")
    parser.add_argument("--github", action="store_true", help="Create GitHub release")
    parser.add_argument("--all", action="store_true", help="Run all build steps")
    
    args = parser.parse_args()
    
    if args.all or not any([args.clean, args.build, args.release, args.github]):
        args.clean = True
        args.build = True
        args.release = True
    
    if args.clean:
        clean_build()
    
    if args.build:
        install_dependencies()
        build_executable()
    
    if args.release:
        create_release_assets()
    
    if args.github:
        create_github_release()
    
    print("🎉 Build completed successfully!")

if __name__ == "__main__":
    main() 