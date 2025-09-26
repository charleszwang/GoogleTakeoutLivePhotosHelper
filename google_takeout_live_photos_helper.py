#!/usr/bin/env python3
"""
Simple entry point for backward compatibility.

This file provides backward compatibility for users who might be used to
running the old monolithic script. It simply imports and runs the new
modular CLI.
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

try:
    from google_takeout_live_photos.cli import main
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"Error: Could not import the main application: {e}")
    print("Please ensure the project is properly installed or run from the project root.")
    sys.exit(1)