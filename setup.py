#!/usr/bin/env python3
"""
Setup script for WARP + NextDNS Manager
Cross-platform CLI application for Windows and Linux
"""

import os
import sys
import platform
from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
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

setup(
    name="warp-nextdns-manager",
    version=version,
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
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "warp-nextdns=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.yml", "*.yaml"],
    },
    keywords="warp, nextdns, wireguard, vpn, networking, cli",
    project_urls={
        "Bug Reports": "https://github.com/your-repo/warp-nextdns-wireguard/issues",
        "Source": "https://github.com/your-repo/warp-nextdns-wireguard",
        "Documentation": "https://github.com/your-repo/warp-nextdns-wireguard/wiki",
    },
) 