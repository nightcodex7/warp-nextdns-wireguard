#!/usr/bin/env python3
"""Main entry point for WARP NextDNS WireGuard Manager."""
import sys
from cli import cli

if __name__ == "__main__":
    sys.exit(cli())