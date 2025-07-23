#!/usr/bin/env python3
<<<<<<< HEAD
"""
WARP + NextDNS Manager - Main Entry Point
"""

import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from cli import main

if __name__ == "__main__":
    main() 
=======
"""Main entry point for WARP NextDNS WireGuard Manager."""
import sys
from cli import cli

if __name__ == "__main__":
    sys.exit(cli())
>>>>>>> 6f8763ed9c292fb062677073732ac3e864bb795d
