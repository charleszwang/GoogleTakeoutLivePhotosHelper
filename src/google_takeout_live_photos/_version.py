"""
Version information for Google Takeout Live Photos Helper.

This module provides version information that can be imported by other modules
and used for display in the GUI, CLI, and package metadata.
"""

__version__ = "1.0.0"
__version_info__ = (1, 0, 0)

# Version components for easy access
MAJOR = 1
MINOR = 0
PATCH = 0

# Build metadata (optional)
BUILD_DATE = "2024-09-26"
BUILD_TYPE = "release"  # "release", "beta", "alpha", "dev"

# Full version string with metadata
def get_version_string(include_build_info: bool = False) -> str:
    """Get formatted version string."""
    version = f"{MAJOR}.{MINOR}.{PATCH}"
    
    if include_build_info:
        version += f" ({BUILD_TYPE}, {BUILD_DATE})"
    
    return version

# Version for display in GUI/CLI
DISPLAY_VERSION = get_version_string(include_build_info=True)
