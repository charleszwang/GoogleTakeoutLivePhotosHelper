"""
Google Takeout Live Photos Helper

A tool to organize Google Takeout exports by matching Live Photos pairs
and separating standalone media files into organized directories.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"
__description__ = "Organize Google Takeout Live Photos pairs and standalone media files"

from .processor import GoogleTakeoutProcessor

__all__ = ["GoogleTakeoutProcessor"]
