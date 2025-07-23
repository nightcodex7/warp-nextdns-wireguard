#!/usr/bin/env python3
<<<<<<< HEAD
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
=======
"""Build script for creating WARP NextDNS Manager executables."""
import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path
import zipfile
import tarfile


class Builder:
    """Build manager for creating releases."""
    
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.dist_dir = self.root_dir / "dist"
        self.build_dir = self.root_dir / "build"
        self.version = self.get_version()
        self.platform = platform.system().lower()
        self.arch = self.get_architecture()
        
    def get_version(self) -> str:
        """Get version from VERSION file."""
        version_file = self.root_dir / "VERSION"
        if version_file.exists():
            return version_file.read_text().strip()
        return "1.0.0"
    
    def get_architecture(self) -> str:
        """Get system architecture."""
        machine = platform.machine().lower()
        arch_map = {
            'x86_64': 'amd64',
            'amd64': 'amd64',
            'i386': '386',
            'i686': '386',
            'aarch64': 'arm64',
            'arm64': 'arm64',
        }
        return arch_map.get(machine, 'amd64')
    
    def clean(self):
        """Clean build artifacts."""
        print("🧹 Cleaning build artifacts...")
        for path in [self.dist_dir, self.build_dir]:
            if path.exists():
                shutil.rmtree(path)
        
        # Clean Python cache
        for cache_dir in self.root_dir.rglob("__pycache__"):
            shutil.rmtree(cache_dir)
    
    def install_dependencies(self):
        """Install build dependencies."""
        print("📦 Installing dependencies...")
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "-r", "requirements.txt", 
            "pyinstaller>=5.0"
        ], check=True)
    
    def build_executable(self):
        """Build executable using PyInstaller."""
        print(f"🔨 Building executable for {self.platform} ({self.arch})...")
        
        # Create dist directory
        self.dist_dir.mkdir(exist_ok=True)
        
        # PyInstaller options
        pyinstaller_args = [
            "pyinstaller",
            "--onefile",
            "--name", f"warp-nextdns-{self.platform}-{self.arch}",
            "--distpath", str(self.dist_dir),
            "--workpath", str(self.build_dir),
            "--clean",
            "--noconfirm",
            "--add-data", f"VERSION{os.pathsep}.",
            "--add-data", f"README.md{os.pathsep}.",
            "--hidden-import", "click",
            "--hidden-import", "rich",
            "--hidden-import", "requests",
            "--hidden-import", "psutil",
        ]
        
        # Platform-specific options
        if self.platform == "windows":
            pyinstaller_args.extend([
                "--icon", "NONE",  # Add icon if available
                "--uac-admin",  # Request admin privileges
            ])
        elif self.platform in ["linux", "darwin"]:
            pyinstaller_args.extend([
                "--strip",  # Strip symbols
            ])
        
        # Add main script
        pyinstaller_args.append("main.py")
        
        # Run PyInstaller
        subprocess.run(pyinstaller_args, check=True)
        
        # Clean up spec file
        spec_file = self.root_dir / f"warp-nextdns-{self.platform}-{self.arch}.spec"
        if spec_file.exists():
            spec_file.unlink()
    
    def create_archive(self):
        """Create release archive with executable and changelog."""
        print("📦 Creating release archive...")
        
        exe_name = f"warp-nextdns-{self.platform}-{self.arch}"
        if self.platform == "windows":
            exe_name += ".exe"
        
        exe_path = self.dist_dir / exe_name
        if not exe_path.exists():
            raise FileNotFoundError(f"Executable not found: {exe_path}")
        
        # Prepare files for archive
        archive_name = f"warp-nextdns-v{self.version}-{self.platform}-{self.arch}"
        archive_dir = self.dist_dir / archive_name
        archive_dir.mkdir(exist_ok=True)
        
        # Copy files to archive directory
        shutil.copy2(exe_path, archive_dir / exe_name)
        
        # Create or copy CHANGELOG.md
        changelog = self.root_dir / "CHANGELOG.md"
        if changelog.exists():
            shutil.copy2(changelog, archive_dir / "CHANGELOG.md")
        else:
            # Create a simple changelog
            with open(archive_dir / "CHANGELOG.md", "w") as f:
                f.write(f"# Changelog\n\n## v{self.version}\n\n- Initial release\n")
        
        # Create README for the archive
        with open(archive_dir / "README.txt", "w") as f:
            f.write(f"""WARP NextDNS Manager v{self.version}
================================

Platform: {self.platform} ({self.arch})

Usage:
------
Run the executable with --help to see all available commands:
    ./{exe_name} --help

Quick setup:
    sudo ./{exe_name} setup --auto

For more information, visit:
https://github.com/nightcodex7/warp-nextdns-wireguard
""")
        
        # Create archive
        if self.platform == "windows":
            # Create ZIP for Windows
            zip_path = self.dist_dir / f"{archive_name}.zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                for file in archive_dir.rglob("*"):
                    if file.is_file():
                        arcname = file.relative_to(archive_dir.parent)
                        zf.write(file, arcname)
            print(f"✅ Created: {zip_path}")
        else:
            # Create tar.gz for Linux/macOS
            tar_path = self.dist_dir / f"{archive_name}.tar.gz"
            with tarfile.open(tar_path, "w:gz") as tar:
                tar.add(archive_dir, arcname=archive_name)
            print(f"✅ Created: {tar_path}")
        
        # Clean up temporary directory
        shutil.rmtree(archive_dir)
    
    def build(self):
        """Run the complete build process."""
        print(f"🚀 Building WARP NextDNS Manager v{self.version}")
        print(f"📍 Platform: {self.platform} ({self.arch})")
        print()
        
        try:
            self.clean()
            self.install_dependencies()
            self.build_executable()
            self.create_archive()
            
            print("\n✨ Build completed successfully!")
            print(f"📁 Output directory: {self.dist_dir}")
            
        except Exception as e:
            print(f"\n❌ Build failed: {e}")
            sys.exit(1)


if __name__ == "__main__":
    builder = Builder()
    builder.build()
>>>>>>> 6f8763ed9c292fb062677073732ac3e864bb795d
