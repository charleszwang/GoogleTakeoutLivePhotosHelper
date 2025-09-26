#!/usr/bin/env python3
"""
Version bumping script for Google Takeout Live Photos Helper.

This script helps manage semantic versioning by updating version numbers
across all relevant files in the project.
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path


def get_current_version():
    """Get the current version from _version.py."""
    version_file = Path(__file__).parent.parent / "src" / "google_takeout_live_photos" / "_version.py"
    
    with open(version_file, 'r') as f:
        content = f.read()
    
    # Extract version numbers
    major_match = re.search(r'MAJOR = (\d+)', content)
    minor_match = re.search(r'MINOR = (\d+)', content)
    patch_match = re.search(r'PATCH = (\d+)', content)
    
    if major_match and minor_match and patch_match:
        return (int(major_match.group(1)), int(minor_match.group(1)), int(patch_match.group(1)))
    
    raise ValueError("Could not parse current version")


def update_version_file(major, minor, patch):
    """Update the _version.py file with new version numbers."""
    version_file = Path(__file__).parent.parent / "src" / "google_takeout_live_photos" / "_version.py"
    
    with open(version_file, 'r') as f:
        content = f.read()
    
    # Update version components
    content = re.sub(r'__version__ = "[^"]*"', f'__version__ = "{major}.{minor}.{patch}"', content)
    content = re.sub(r'__version_info__ = \([^)]*\)', f'__version_info__ = ({major}, {minor}, {patch})', content)
    content = re.sub(r'MAJOR = \d+', f'MAJOR = {major}', content)
    content = re.sub(r'MINOR = \d+', f'MINOR = {minor}', content)
    content = re.sub(r'PATCH = \d+', f'PATCH = {patch}', content)
    
    # Update build date
    today = datetime.now().strftime("%Y-%m-%d")
    content = re.sub(r'BUILD_DATE = "[^"]*"', f'BUILD_DATE = "{today}"', content)
    
    with open(version_file, 'w') as f:
        f.write(content)
    
    print(f"✅ Updated version to {major}.{minor}.{patch}")


def update_changelog(major, minor, patch):
    """Add new version entry to changelog."""
    changelog_file = Path(__file__).parent.parent / "docs" / "CHANGELOG.md"
    
    with open(changelog_file, 'r') as f:
        content = f.read()
    
    # Find the insertion point (after the header)
    lines = content.split('\n')
    insert_index = None
    
    for i, line in enumerate(lines):
        if line.startswith('## [') and 'Unreleased' not in line:
            insert_index = i
            break
    
    if insert_index is None:
        # Find after the header
        for i, line in enumerate(lines):
            if line.strip() == '':
                continue
            if line.startswith('#'):
                continue
            insert_index = i
            break
    
    # Create new version entry
    today = datetime.now().strftime("%Y-%m-%d")
    new_entry = [
        f"## [{major}.{minor}.{patch}] - {today}",
        "",
        "### Added",
        "- (Add your changes here)",
        "",
        "### Changed", 
        "- (Add your changes here)",
        "",
        "### Fixed",
        "- (Add your changes here)",
        "",
    ]
    
    # Insert new entry
    lines[insert_index:insert_index] = new_entry
    
    with open(changelog_file, 'w') as f:
        f.write('\n'.join(lines))
    
    print(f"✅ Added v{major}.{minor}.{patch} entry to CHANGELOG.md")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Bump version numbers")
    parser.add_argument("bump_type", choices=["major", "minor", "patch"], 
                       help="Type of version bump")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Show what would be changed without making changes")
    
    args = parser.parse_args()
    
    # Get current version
    try:
        current_major, current_minor, current_patch = get_current_version()
        print(f"📋 Current version: {current_major}.{current_minor}.{current_patch}")
    except Exception as e:
        print(f"❌ Error getting current version: {e}")
        sys.exit(1)
    
    # Calculate new version
    if args.bump_type == "major":
        new_major, new_minor, new_patch = current_major + 1, 0, 0
    elif args.bump_type == "minor":
        new_major, new_minor, new_patch = current_major, current_minor + 1, 0
    else:  # patch
        new_major, new_minor, new_patch = current_major, current_minor, current_patch + 1
    
    print(f"🚀 New version: {new_major}.{new_minor}.{new_patch}")
    
    if args.dry_run:
        print("🧪 Dry run mode - no changes made")
        return
    
    # Update files
    try:
        update_version_file(new_major, new_minor, new_patch)
        update_changelog(new_major, new_minor, new_patch)
        
        print(f"\n🎉 Version bumped to {new_major}.{new_minor}.{new_patch}")
        print("📝 Next steps:")
        print("1. Update CHANGELOG.md with your changes")
        print("2. Test the new version")
        print("3. Commit and tag: git tag v{new_major}.{new_minor}.{new_patch}")
        print("4. Push: git push --tags")
        
    except Exception as e:
        print(f"❌ Error updating version: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
