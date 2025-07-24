#!/usr/bin/env python3
"""
Setup script for WARP + NextDNS Manager
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("VERSION", "r") as f:
    version = f.read().strip()

setup(
    name="warp-nextdns-manager",
    version=version,
    author="NightCodex7",
    description="Cross-platform CLI tool for Cloudflare WARP with NextDNS integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nightcodex7/warp-nextdns-wireguard",
    packages=find_packages(),
    package_dir={'': '.'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Networking",
        "Topic :: Security",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "colorama>=0.4.4",
        "psutil>=5.8.0",
        "cryptography>=3.4.0",
        "pyyaml>=5.4.0",
        "rich>=10.0.0",
        "click>=8.0.0",
        "tabulate>=0.8.9",
        "python-dotenv>=0.19.0",
        "validators>=0.18.0",
    ],
    entry_points={
        "console_scripts": [
            "warp-manager=src.cli:cli",
            "warp-nextdns=src.cli:cli",
        ],
    },
)
