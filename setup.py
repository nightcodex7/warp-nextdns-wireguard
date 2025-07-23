#!/usr/bin/env python3
"""
Setup script for WARP + NextDNS Manager
Cross-platform CLI application for Windows and Linux
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read version from VERSION file
version_file = this_directory / "VERSION"
version = version_file.read_text().strip() if version_file.exists() else "1.0.0"

# Read requirements
requirements_file = this_directory / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = [
        line.strip()
        for line in requirements_file.read_text().splitlines()
        if line.strip() and not line.startswith("#")
    ]


setup(
    name="warp-nextdns-manager",
    version=version,
    author="nightcodex7",
    author_email="security@nightcode.dev",
    description="Cross-platform CLI manager for Cloudflare WARP and NextDNS",
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
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "warp-nextdns=cli:cli",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["VERSION", "README.md", "CHANGELOG.md"],
    },
)
