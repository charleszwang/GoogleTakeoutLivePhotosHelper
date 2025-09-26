#!/usr/bin/env python3
"""
Build script for creating standalone executables using PyInstaller.

This script creates platform-specific executables that users can run
without installing Python or any dependencies.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def build_executable():
    """Build the standalone executable using PyInstaller."""
    
    print("🚀 Building Google Takeout Live Photos Helper executable...")
    print(f"Platform: {platform.system()} {platform.machine()}")
    
    # Ensure we're in the right directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Define the main script to compile
    main_script = "src/google_takeout_live_photos/gui_app.py"
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single executable file
        "--windowed",                   # No console window (GUI only)
        "--name", "GoogleTakeoutHelper", # Executable name
        "--add-data", "src/google_takeout_live_photos:google_takeout_live_photos",  # Include package
        "--hidden-import", "tkinter",   # Ensure tkinter is included
        "--hidden-import", "tkinter.filedialog",
        "--hidden-import", "tkinter.messagebox",
        "--hidden-import", "tkinter.scrolledtext",
        "--clean",                      # Clean cache
        main_script
    ]
    
    # Add platform-specific options
    if platform.system() == "Darwin":  # macOS
        cmd.extend([
            "--osx-bundle-identifier", "com.example.google-takeout-helper",
            "--target-arch", "universal2"  # Universal binary for Intel and Apple Silicon
        ])
    elif platform.system() == "Windows":
        cmd.extend([
            "--version-file", "version_info.txt",  # Windows version info (if exists)
        ])
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build successful!")
        
        # Show output location
        dist_dir = script_dir / "dist"
        if platform.system() == "Windows":
            executable_name = "GoogleTakeoutHelper.exe"
        else:
            executable_name = "GoogleTakeoutHelper"
            
        executable_path = dist_dir / executable_name
        
        if executable_path.exists():
            print(f"📦 Executable created: {executable_path}")
            print(f"📏 File size: {executable_path.stat().st_size / (1024*1024):.1f} MB")
            
            # Test the executable
            print("\n🧪 Testing executable...")
            test_result = subprocess.run([str(executable_path), "--help"], 
                                       capture_output=True, text=True, timeout=10)
            if test_result.returncode == 0:
                print("✅ Executable test passed!")
            else:
                print("⚠️ Executable test failed - but file was created")
                
        else:
            print("❌ Executable not found in expected location")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    return True


def create_spec_file():
    """Create a PyInstaller spec file for advanced configuration."""
    
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/google_takeout_live_photos/gui_app.py'],
    pathex=[],
    binaries=[],
    datas=[('src/google_takeout_live_photos', 'google_takeout_live_photos')],
    hiddenimports=[
        'tkinter',
        'tkinter.filedialog',
        'tkinter.messagebox', 
        'tkinter.scrolledtext',
        'tkinter.ttk'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GoogleTakeoutHelper',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# macOS app bundle (optional)
app = BUNDLE(
    exe,
    name='GoogleTakeoutHelper.app',
    icon=None,
    bundle_identifier='com.example.google-takeout-helper',
)
'''
    
    with open("GoogleTakeoutHelper.spec", "w") as f:
        f.write(spec_content)
    
    print("📝 Created GoogleTakeoutHelper.spec file")


if __name__ == "__main__":
    print("Google Takeout Live Photos Helper - Executable Builder")
    print("=" * 50)
    
    # Check if PyInstaller is available
    try:
        subprocess.run(["pyinstaller", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller>=6.0"], check=True)
    
    # Create spec file
    create_spec_file()
    
    # Build executable
    success = build_executable()
    
    if success:
        print("\n🎉 Build complete!")
        print("\n📋 Next steps:")
        print("1. Test the executable in the 'dist' folder")
        print("2. Distribute the executable to users")
        print("3. No Python installation required for end users!")
    else:
        print("\n❌ Build failed. Check the error messages above.")
        sys.exit(1)
