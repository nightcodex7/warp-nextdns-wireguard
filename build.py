#!/usr/bin/env python3
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