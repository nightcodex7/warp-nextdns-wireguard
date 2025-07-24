#!/usr/bin/env python3
"""
WARP + NextDNS Manager - Main Entry Point
"""

import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from src.cli import cli

if __name__ == "__main__":
    sys.exit(cli())
