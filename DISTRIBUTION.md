# Distribution Guide

This guide explains how to distribute Google Takeout Live Photos Helper to end users.

## 🎯 Distribution Options

### 1. **Standalone Executables (Recommended for End Users)**
- **No Python installation required**
- **Double-click to run**
- **Works on any computer**
- **Best user experience**

### 2. **Python Package (For Developers)**
- **Requires Python installation**
- **Install via pip**
- **Access to source code**
- **Easy to modify and extend**

## 📦 Creating Executables

### Quick Build

```bash
# macOS/Linux
./scripts/build_gui_executable.sh

# Windows  
scripts\build_gui_executable.bat

# Or use Make
make build-exe
```

### Manual Build

```bash
# 1. Create virtual environment
python3 -m venv build_env
source build_env/bin/activate  # Linux/macOS
# build_env\Scripts\activate     # Windows

# 2. Install PyInstaller
pip install pyinstaller>=6.0

# 3. Build executable
pyinstaller \
    --onefile \
    --windowed \
    --name "GoogleTakeoutHelper" \
    --add-data "src/google_takeout_live_photos:google_takeout_live_photos" \
    --hidden-import tkinter \
    --clean \
    src/google_takeout_live_photos/gui_app.py
```

## 📁 Distribution Files

After building, you'll have:

```
dist/
├── GoogleTakeoutHelper          # Standalone executable (macOS/Linux)
├── GoogleTakeoutHelper.exe      # Standalone executable (Windows)
└── GoogleTakeoutHelper.app/     # macOS app bundle
```

**File sizes:** ~10-25 MB (includes Python interpreter and dependencies)

## 🚀 User Instructions

### For macOS Users

**Option 1: App Bundle (Recommended)**
1. Download `GoogleTakeoutHelper.app`
2. Drag to Applications folder (optional)
3. Double-click to run
4. If security warning appears:
   - Right-click → Open (first time only)
   - Or: System Preferences → Security & Privacy → Allow

**Option 2: Standalone Executable**
1. Download `GoogleTakeoutHelper`
2. Make executable: `chmod +x GoogleTakeoutHelper`
3. Double-click or run from terminal

### For Windows Users

1. Download `GoogleTakeoutHelper.exe`
2. Double-click to run
3. If Windows Defender warning appears:
   - Click "More info"
   - Click "Run anyway"
   - This is normal for unsigned executables

### For Linux Users

1. Download `GoogleTakeoutHelper`
2. Make executable: `chmod +x GoogleTakeoutHelper`
3. Double-click or run: `./GoogleTakeoutHelper`

## 📋 What Users Get

### No Technical Knowledge Required
- **Double-click to launch** - just like any desktop app
- **Visual interface** - no command line needed
- **Built-in help** - tooltips and guidance throughout
- **Error handling** - clear messages if something goes wrong

### Professional Experience
- **Native file dialogs** for directory selection
- **Progress tracking** with real-time updates
- **Detailed results** with statistics
- **Issue detection** and warnings

## 🔧 Advanced Distribution

### Code Signing (Recommended for Public Release)

**macOS:**
```bash
# Sign the app bundle
codesign --force --deep --sign "Developer ID Application: Your Name" dist/GoogleTakeoutHelper.app

# Notarize for Gatekeeper
xcrun notarytool submit dist/GoogleTakeoutHelper.app --keychain-profile "notary-profile" --wait
```

**Windows:**
```bash
# Sign with certificate
signtool sign /f certificate.p12 /p password /t http://timestamp.verisign.com/scripts/timstamp.dll dist/GoogleTakeoutHelper.exe
```

### Creating Installers

**Windows (NSIS):**
```nsis
; installer.nsi
Name "Google Takeout Helper"
OutFile "GoogleTakeoutHelper-Installer.exe"
InstallDir "$PROGRAMFILES\GoogleTakeoutHelper"

Section "MainSection" SEC01
    SetOutPath "$INSTDIR"
    File "dist\GoogleTakeoutHelper.exe"
    CreateShortCut "$DESKTOP\Google Takeout Helper.lnk" "$INSTDIR\GoogleTakeoutHelper.exe"
SectionEnd
```

**macOS (DMG):**
```bash
create-dmg \
    --volname "Google Takeout Helper" \
    --app-drop-link 600 185 \
    "GoogleTakeoutHelper.dmg" \
    "dist/GoogleTakeoutHelper.app"
```

## 📊 File Size Optimization

### Reducing Executable Size

```bash
# Exclude unused modules
pyinstaller \
    --onefile \
    --windowed \
    --exclude-module matplotlib \
    --exclude-module numpy \
    --exclude-module pandas \
    src/google_takeout_live_photos/gui_app.py
```

### Expected Sizes
- **Basic executable**: ~10-15 MB
- **With all dependencies**: ~15-25 MB
- **Compressed (UPX)**: ~8-12 MB

## 🎉 Benefits for Users

### Before (Python Script)
```
❌ Install Python 3.8+
❌ Install dependencies
❌ Learn command line
❌ Navigate terminal
❌ Troubleshoot import errors
```

### After (Standalone Executable)
```
✅ Download one file
✅ Double-click to run
✅ Visual interface
✅ No installation needed
✅ Works immediately
```

## 📝 Release Checklist

### Before Building
- [ ] Test on clean Python environment
- [ ] Update version numbers
- [ ] Test all GUI functionality
- [ ] Run full test suite

### Building
- [ ] Build for all target platforms
- [ ] Test executables on each platform
- [ ] Verify file sizes are reasonable
- [ ] Test on machines without Python

### Distribution
- [ ] Create GitHub release
- [ ] Upload executables as release assets
- [ ] Write clear download instructions
- [ ] Test download links

### Documentation
- [ ] Update README with download links
- [ ] Create user guide for executable
- [ ] Add screenshots of executable in action
- [ ] Document system requirements

The executable approach makes your tool **accessible to everyone** - from your grandmother to corporate users who can't install Python! 🎉
