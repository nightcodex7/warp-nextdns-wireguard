<<<<<<< HEAD
#!/usr/bin/env python3
"""
Setup script for WARP + NextDNS Manager
Cross-platform CLI application for Windows and Linux
"""

import os
import sys
import platform
=======
"""Setup script for WARP NextDNS WireGuard Manager."""
>>>>>>> 6f8763ed9c292fb062677073732ac3e864bb795d
from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
<<<<<<< HEAD
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read version from VERSION file
version = (this_directory / "VERSION").read_text().strip()

# Read requirements
with open("requirements.txt") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

# Platform-specific requirements
if platform.system() == "Windows":
    requirements.extend([
        "pywin32>=306; sys_platform == 'win32'",
    ])
elif platform.system() == "Linux":
    requirements.extend([
        "psutil>=5.9.0",
    ])
=======
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read version
version_file = Path(__file__).parent / "VERSION"
version = version_file.read_text().strip() if version_file.exists() else "1.0.0"

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = [
        line.strip() 
        for line in requirements_file.read_text().splitlines() 
        if line.strip() and not line.startswith("#") and not line.startswith("-")
    ]
>>>>>>> 6f8763ed9c292fb062677073732ac3e864bb795d

setup(
    name="warp-nextdns-manager",
    version=version,
<<<<<<< HEAD
    author="WARP NextDNS Manager Team",
    author_email="support@example.com",
    description="Cross-platform CLI manager for Cloudflare WARP and NextDNS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-repo/warp-nextdns-wireguard",
    packages=find_packages(),
    py_modules=["main", "cli", "core"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
=======
    author="nightcodex7",
    author_email="",
    description="WARP + NextDNS WireGuard Manager - Secure your connection with Cloudflare WARP and NextDNS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nightcodex7/warp-nextdns-wireguard",
    project_urls={
        "Bug Tracker": "https://github.com/nightcodex7/warp-nextdns-wireguard/issues",
        "Documentation": "https://nightcodex7.github.io/warp-nextdns-wireguard/",
        "Source Code": "https://github.com/nightcodex7/warp-nextdns-wireguard",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Networking",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
>>>>>>> 6f8763ed9c292fb062677073732ac3e864bb795d
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
<<<<<<< HEAD
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
=======
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
>>>>>>> 6f8763ed9c292fb062677073732ac3e864bb795d
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
<<<<<<< HEAD
            "warp-nextdns=main:main",
=======
            "warp-nextdns=cli:cli",
>>>>>>> 6f8763ed9c292fb062677073732ac3e864bb795d
        ],
    },
    include_package_data=True,
    package_data={
<<<<<<< HEAD
        "": ["*.txt", "*.md", "*.yml", "*.yaml"],
    },
    keywords="warp, nextdns, wireguard, vpn, networking, cli",
    project_urls={
        "Bug Reports": "https://github.com/your-repo/warp-nextdns-wireguard/issues",
        "Source": "https://github.com/your-repo/warp-nextdns-wireguard",
        "Documentation": "https://github.com/your-repo/warp-nextdns-wireguard/wiki",
    },
) 
=======
        "": ["VERSION", "README.md", "CHANGELOG.md"],
    },
)
>>>>>>> 6f8763ed9c292fb062677073732ac3e864bb795d
