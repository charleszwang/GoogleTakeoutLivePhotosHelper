# Creating Standalone Executables

This guide explains how to create standalone executables that users can run without installing Python or any dependencies.

## 🎯 Why Create Executables?

**Benefits for users:**
- **No Python installation required** 
- **Double-click to run** - just like any other app
- **No command-line knowledge needed**
- **Works on computers without development tools**

**Perfect for:**
- Non-technical users
- Sharing with family/friends
- Corporate environments with restricted software installation
- Users who just want a simple desktop app

## 🛠️ Building Executables

### Quick Build (Recommended)

**macOS/Linux:**
```bash
# Method 1: Use the build script
./scripts/build_gui_executable.sh

# Method 2: Use Make
make build-exe
```

**Windows:**
```cmd
# Method 1: Use the batch file
scripts\build_gui_executable.bat

# Method 2: Use Make (if available)
make build-exe
```

### Manual Build

If you prefer to build manually:

```bash
# Install PyInstaller
pip install pyinstaller>=6.0

# Build GUI-only executable
pyinstaller \
    --onefile \
    --windowed \
    --name "GoogleTakeoutHelper" \
    --add-data "src/google_takeout_live_photos:google_takeout_live_photos" \
    --hidden-import tkinter \
    --clean \
    src/google_takeout_live_photos/gui_app.py
```

## 📦 Output Files

After building, you'll find:

```
dist/
├── GoogleTakeoutHelper          # macOS/Linux executable
├── GoogleTakeoutHelper.exe      # Windows executable  
└── GoogleTakeoutHelper.app/     # macOS app bundle (if using --windowed)
```

**File sizes:** Typically 15-25 MB (includes Python interpreter and all dependencies)

## 🚀 Distribution

### For End Users

**macOS:**
1. Share the `GoogleTakeoutHelper` file or `GoogleTakeoutHelper.app` bundle
2. Users might need to allow the app in System Preferences > Security & Privacy
3. Right-click → Open (first time only) to bypass Gatekeeper

**Windows:**
1. Share the `GoogleTakeoutHelper.exe` file
2. Windows Defender might show a warning (normal for unsigned executables)
3. Users can click "More info" → "Run anyway"

**Linux:**
1. Share the `GoogleTakeoutHelper` file
2. Users might need to make it executable: `chmod +x GoogleTakeoutHelper`

### Creating Installers (Advanced)

For even better user experience, you can create installers:

**Windows (using NSIS):**
```bash
# Install NSIS, then create installer script
makensis installer.nsi
```

**macOS (using create-dmg):**
```bash
# Create a DMG file for distribution
create-dmg --app-drop-link 600 185 GoogleTakeoutHelper.dmg dist/GoogleTakeoutHelper.app
```

## 🧪 Testing Executables

### Basic Testing
```bash
# Test that it launches
./dist/GoogleTakeoutHelper

# Test with sample data
# (Use the GUI to process test_takeout folder)
```

### Platform Testing
- **Test on clean machines** without Python installed
- **Test different OS versions** (macOS 10.15+, Windows 10+, Ubuntu 20.04+)
- **Test with real Google Takeout data**

## 🔧 Troubleshooting

### Common Issues

**"Module not found" errors:**
- Add missing modules to `--hidden-import` list
- Check that all dependencies are included

**Large executable size:**
- Normal - includes Python interpreter (~15-25 MB)
- Use `--exclude-module` to remove unused modules

**Slow startup:**
- Normal for PyInstaller executables
- First launch extracts files to temp directory

**macOS "App can't be opened":**
- Use: `xattr -cr GoogleTakeoutHelper.app`
- Or: System Preferences > Security & Privacy > Allow

**Windows "Windows protected your PC":**
- Click "More info" → "Run anyway"
- Consider code signing for professional distribution

### Build Issues

**PyInstaller not found:**
```bash
pip install pyinstaller>=6.0
```

**Import errors during build:**
```bash
# Add missing imports to the build command
--hidden-import module_name
```

**Data files not included:**
```bash
# Ensure data files are added correctly
--add-data "source_path:destination_path"
```

## 📋 Development Workflow

### For Developers

1. **Develop and test** using normal Python execution
2. **Build executable** when ready for distribution
3. **Test executable** on target platforms
4. **Distribute** to users

### For Users

1. **Download executable** from releases
2. **Double-click to run** - no installation needed
3. **Use GUI** to process Google Takeout data
4. **Enjoy organized photos!**

## 🎉 Benefits Summary

**For Developers:**
- Easy to create with provided scripts
- Cross-platform distribution
- No user support for Python installation issues

**For Users:**
- **Zero technical knowledge required**
- **No command line** - pure GUI experience
- **No Python installation** needed
- **Works like any desktop app**

The executable approach makes your tool accessible to **everyone**, not just developers! 🚀
