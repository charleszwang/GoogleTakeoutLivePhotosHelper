@echo off
REM Simple script to build a standalone GUI executable on Windows

echo 🚀 Building Google Takeout Live Photos Helper Executable
echo =======================================================

REM Check if we're in the right directory
if not exist "pyproject.toml" (
    echo ❌ Error: Run this script from the project root directory
    pause
    exit /b 1
)

REM Install PyInstaller if needed
echo 📦 Installing PyInstaller...
pip install pyinstaller>=6.0

REM Build the executable
echo 🔨 Building executable...
pyinstaller ^
    --onefile ^
    --windowed ^
    --name "GoogleTakeoutHelper" ^
    --add-data "src/google_takeout_live_photos;google_takeout_live_photos" ^
    --hidden-import tkinter ^
    --hidden-import tkinter.filedialog ^
    --hidden-import tkinter.messagebox ^
    --hidden-import tkinter.scrolledtext ^
    --clean ^
    src/google_takeout_live_photos/gui_app.py

REM Check if build was successful
if exist "dist\GoogleTakeoutHelper.exe" (
    echo ✅ Build successful!
    echo 📦 Executable location: dist\
    echo.
    echo 📋 Distribution instructions:
    echo 1. The executable in 'dist\' folder can be distributed to users
    echo 2. Users can double-click it to run (no Python installation needed)
    echo 3. Windows might show a security warning - users can click "More info" then "Run anyway"
    echo.
    dir dist\GoogleTakeoutHelper.exe
) else (
    echo ❌ Build failed - check error messages above
    pause
    exit /b 1
)

pause
