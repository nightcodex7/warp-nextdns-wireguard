"""Setup script for WARP NextDNS WireGuard Manager."""
from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
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

setup(
    name="warp-nextdns-manager",
    version=version,
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
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
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