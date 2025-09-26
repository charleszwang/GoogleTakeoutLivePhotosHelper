"""
Google Takeout Live Photos Helper

A tool to organize Google Takeout exports by matching Live Photos pairs
and separating standalone media files into organized directories.
"""

from ._version import __version__, __version_info__, DISPLAY_VERSION

__author__ = "Charles Wang"
__email__ = "charleswangmain@gmail.com"
__description__ = "Transform messy Google Takeout exports into organized Live Photos and sorted media files"

from .processor import GoogleTakeoutProcessor

__all__ = ["GoogleTakeoutProcessor", "__version__", "__version_info__", "DISPLAY_VERSION"]
