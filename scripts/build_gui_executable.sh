#!/bin/bash
# Simple script to build a standalone GUI executable

echo "🚀 Building Google Takeout Live Photos Helper Executable"
echo "======================================================="

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Run this script from the project root directory"
    exit 1
fi

# Install PyInstaller if needed
echo "📦 Installing PyInstaller..."
pip3 install pyinstaller>=6.0

# Build the executable
echo "🔨 Building executable..."
pyinstaller \
    --onefile \
    --windowed \
    --name "GoogleTakeoutHelper" \
    --add-data "src/google_takeout_live_photos:google_takeout_live_photos" \
    --hidden-import tkinter \
    --hidden-import tkinter.filedialog \
    --hidden-import tkinter.messagebox \
    --hidden-import tkinter.scrolledtext \
    --clean \
    src/google_takeout_live_photos/gui_app.py

# Check if build was successful
if [ -f "dist/GoogleTakeoutHelper" ] || [ -f "dist/GoogleTakeoutHelper.exe" ]; then
    echo "✅ Build successful!"
    echo "📦 Executable location: dist/"
    echo ""
    echo "📋 Distribution instructions:"
    echo "1. The executable in 'dist/' folder can be distributed to users"
    echo "2. Users can double-click it to run (no Python installation needed)"
    echo "3. On macOS, users might need to allow the app in Security preferences"
    echo ""
    ls -lh dist/GoogleTakeoutHelper*
else
    echo "❌ Build failed - check error messages above"
    exit 1
fi
