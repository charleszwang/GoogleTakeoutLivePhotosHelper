#!/usr/bin/env python3
"""
Simple launcher script for the GUI version of Google Takeout Live Photos Helper.

This script provides an easy way to launch the GUI without command line arguments.
"""

import sys
from pathlib import Path

# Add src directory to path to import modules
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

try:
    from google_takeout_live_photos.gui import main as gui_main
    
    if __name__ == "__main__":
        print("🚀 Launching Google Takeout Live Photos Helper GUI...")
        gui_main()
        
except ImportError as e:
    print(f"❌ Error: Could not import GUI module: {e}")
    print("Make sure all required files are in the same directory.")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error launching GUI: {e}")
    sys.exit(1)
