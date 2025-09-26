# Google Takeout Live Photos Helper v1.0.0

**Transform your messy Google Takeout exports into organized Live Photos!**

## 🎉 **Initial Release**

This is the first public release of Google Takeout Live Photos Helper - a tool that solves the frustrating problem of split Live Photos in Google Takeout exports.

### **🎯 What This Release Includes**

#### **🖥️ Beautiful Desktop Application**
- **Standalone executables** for Windows, macOS, and Linux (no Python installation required)
- **Intuitive GUI** with light and dark themes
- **Smart directory selection** with automatic subdirectory creation
- **Real-time progress tracking** and detailed logging

#### **⌨️ Powerful Command Line Interface**
- **Simple mode**: `--output-dir` creates organized subdirectories automatically
- **Traditional mode**: Specify separate directories for pairs and leftovers
- **Comprehensive options**: Dry run, verbose logging, duplicate removal
- **Professional help system** with examples

#### **🔧 Core Features**
- **Two-pass matching algorithm**: Finds Live Photos in same or different folders
- **Duplicate detection**: Prevents same files in multiple output folders
- **Issue validation**: Warns about potential problems before processing
- **Manifest files**: Detailed logs of all operations
- **Cross-platform**: Works on Windows, macOS, and Linux

### **🔒 Privacy & Security**
- **100% local processing** - your photos never leave your computer
- **No internet required** - works completely offline
- **Open source** - you can verify exactly what it does
- **No tracking or analytics** - completely private

### **📥 Downloads**

#### **For Most Users (No Installation Required)**
- **Windows**: Download `GoogleTakeoutHelper.exe` below
- **macOS**: Download `GoogleTakeoutHelper.app` below  
- **Linux**: Download `GoogleTakeoutHelper` below

#### **For Developers**
- **Source code**: Available in this repository
- **Python package**: `pip install git+https://github.com/YOUR_USERNAME/google-takeout-live-photos-helper.git`

### **🚀 Quick Start**

#### **Using the Desktop App**
1. Download the appropriate file for your operating system
2. Double-click to run (no installation needed)
3. Select your Google Takeout folder
4. Choose where to save organized photos
5. Click "Process Photos" and you're done!

#### **Using Command Line**
```bash
# Simple mode (recommended)
python google_takeout_live_photos_helper.py \
  --root ~/Downloads/Takeout \
  --output-dir ~/Desktop/OrganizedPhotos \
  --dry-run

# Run for real after reviewing dry run results
python google_takeout_live_photos_helper.py \
  --root ~/Downloads/Takeout \
  --output-dir ~/Desktop/OrganizedPhotos
```

### **📊 What You Get**

**Organized Output:**
- **LivePhotos/** folder with all your Live Photos properly paired
- **OtherMedia/** folder with all other photos and videos
- **Manifest files** with detailed operation logs

**Typical Results:**
- Organizes thousands of files in minutes
- Pairs hundreds of Live Photos automatically
- Removes duplicates and prevents conflicts
- Creates clean, importable photo library

### **🐛 Known Issues**
- GUI tests have low coverage (GUI testing is inherently complex)
- Some edge cases in cross-directory pairing may need manual review
- FFmpeg/ffprobe required for video duration analysis (optional feature)

### **🔗 Related Tools**
- **[GooglePhotosTakeoutHelper](https://github.com/TheLastGimbus/GooglePhotosTakeoutHelper)** - Alternative approach
- **[rclone](https://rclone.org/)** - Sync organized photos to cloud storage
- **[PhotoPrism](https://photoprism.app/)** - Self-hosted photo management

### **💖 Support This Project**

If this tool helped you organize your photos, please consider:
- ⭐ **Starring this repository**
- 💰 **[Making a donation](https://www.paypal.com/donate/?hosted_button_id=FPEZJUYKMH7M6)**
- 📢 **Sharing with others** who need it
- 🐛 **Reporting bugs** or suggesting features

### **🤝 Contributing**

This project welcomes contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### **📝 License**

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

**Developed with AI assistance to create a professional, user-friendly tool for the community.**

**Your Google Photos are finally organized! 📸✨**
