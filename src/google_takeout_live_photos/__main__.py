#!/usr/bin/env python3
"""
Entry point for running the package as a module.

This allows running the package with: python -m google_takeout_live_photos
"""

from .cli import main

if __name__ == "__main__":
    main()
