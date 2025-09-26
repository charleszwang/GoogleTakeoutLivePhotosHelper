#!/usr/bin/env python3
"""
Generate code coverage report for the project.

This script runs the test suite and generates comprehensive coverage reports
including HTML and XML formats for CI/CD integration.
"""

import os
import subprocess
import sys
from pathlib import Path


def main():
    """Generate coverage reports."""
    print("📊 Generating Code Coverage Report")
    print("=" * 40)
    
    # Ensure we're in the project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Set PYTHONPATH
    env = os.environ.copy()
    env['PYTHONPATH'] = 'src'
    
    try:
        # Install coverage if not available
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'coverage', 'pytest-cov'], 
                      check=True, capture_output=True)
        
        print("🧪 Running tests with coverage...")
        
        # Run tests with coverage
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 'tests/',
            '--cov=google_takeout_live_photos',
            '--cov-report=term-missing',
            '--cov-report=html',
            '--cov-report=xml',
            '-v'
        ], env=env, capture_output=True, text=True)
        
        print("📋 Test Results:")
        print(result.stdout)
        
        if result.stderr:
            print("⚠️ Warnings/Errors:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ Coverage report generated successfully!")
            print(f"📁 HTML Report: {project_root}/htmlcov/index.html")
            print(f"📄 XML Report: {project_root}/coverage.xml")
            
            # Try to get coverage percentage
            try:
                cov_result = subprocess.run([
                    sys.executable, '-m', 'coverage', 'report', '--format=total'
                ], env=env, capture_output=True, text=True)
                
                if cov_result.stdout.strip():
                    coverage_pct = float(cov_result.stdout.strip())
                    print(f"📊 Total Coverage: {coverage_pct:.1f}%")
                    
                    if coverage_pct >= 90:
                        print("🎉 Excellent coverage!")
                    elif coverage_pct >= 80:
                        print("👍 Good coverage!")
                    else:
                        print("⚠️ Coverage could be improved")
                        
            except Exception:
                pass  # Coverage percentage extraction failed
                
        else:
            print("❌ Coverage generation failed")
            sys.exit(1)
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
