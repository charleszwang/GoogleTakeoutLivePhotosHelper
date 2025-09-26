#!/usr/bin/env python3
"""
Update coverage badge with actual coverage percentage.
"""

import re
import subprocess
import sys
from pathlib import Path


def get_coverage_percentage():
    """Get current coverage percentage."""
    try:
        # Run coverage and capture output
        result = subprocess.run([
            sys.executable, '-m', 'coverage', 'report', '--format=total'
        ], capture_output=True, text=True, cwd=Path(__file__).parent.parent)
        
        if result.returncode == 0 and result.stdout.strip():
            return float(result.stdout.strip())
    except Exception:
        pass
    
    # Fallback: parse from coverage report
    try:
        result = subprocess.run([
            sys.executable, '-m', 'coverage', 'report'
        ], capture_output=True, text=True, cwd=Path(__file__).parent.parent)
        
        # Look for TOTAL line
        for line in result.stdout.split('\n'):
            if 'TOTAL' in line:
                # Extract percentage (last column)
                parts = line.split()
                if len(parts) >= 4 and '%' in parts[-1]:
                    return float(parts[-1].replace('%', ''))
    except Exception:
        pass
    
    return None


def update_readme_coverage(coverage_pct):
    """Update README with actual coverage percentage."""
    readme_path = Path(__file__).parent.parent / 'README.md'
    
    try:
        with open(readme_path, 'r') as f:
            content = f.read()
        
        # Update coverage badge
        old_badge = r'!\[Coverage\]\(https://img\.shields\.io/codecov/c/github/charleszwang/google-takeout-live-photos-helper\)'
        new_badge = f'![Coverage](https://img.shields.io/badge/coverage-{coverage_pct:.0f}%25-brightgreen)'
        
        content = re.sub(old_badge, new_badge, content)
        
        with open(readme_path, 'w') as f:
            f.write(content)
        
        print(f"✅ Updated README coverage badge to {coverage_pct:.0f}%")
        
    except Exception as e:
        print(f"❌ Failed to update README: {e}")


def main():
    """Main function."""
    print("📊 Updating Coverage Badge")
    print("=" * 30)
    
    coverage_pct = get_coverage_percentage()
    
    if coverage_pct is not None:
        print(f"📈 Current coverage: {coverage_pct:.1f}%")
        update_readme_coverage(coverage_pct)
        
        # Provide feedback on coverage level
        if coverage_pct >= 90:
            print("🎉 Excellent coverage!")
        elif coverage_pct >= 80:
            print("👍 Good coverage!")
        elif coverage_pct >= 70:
            print("📈 Decent coverage - room for improvement")
        else:
            print("⚠️ Coverage needs improvement")
            
    else:
        print("❌ Could not determine coverage percentage")
        print("Run 'make coverage' first to generate coverage data")


if __name__ == "__main__":
    main()

