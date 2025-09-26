# Google Takeout Live Photos Helper

**Transform your messy Google Takeout exports into organized Live Photos!**

When you export photos from Google Photos, Live Photos get split into separate image and video files. This tool puts them back together and organizes everything neatly.

## 💖 Support This Project

If this tool helps you organize your Google Photos, please consider supporting its development:

[![Donate with PayPal](https://img.shields.io/badge/Donate-PayPal-blue?logo=paypal&style=for-the-badge&logoColor=white)](https://www.paypal.com/donate/?hosted_button_id=FPEZJUYKMH7M6)

⭐ **Also consider starring this repository** to help others discover it!

---

*This project was developed with the assistance of AI to create a professional, user-friendly tool for the community.*

## 🎯 What it does

**Before:** Messy folders with thousands of scattered files  
**After:** Clean folders with Live Photos paired up and other media organized

The tool:
1. **Finds** your Live Photos (photo + video pairs)
2. **Puts them back together** in one organized folder
3. **Sorts** all other photos and videos separately
4. **Removes duplicates** (optional)
5. **Creates** a clean, organized photo library

## 🚀 **Easy Download & Run (Recommended)**

**No installation required! Just download and double-click:**

- **macOS**: Download `GoogleTakeoutHelper.app` from [Releases](https://github.com/yourusername/google-takeout-live-photos-helper/releases)
- **Windows**: Download `GoogleTakeoutHelper.exe` from [Releases](https://github.com/yourusername/google-takeout-live-photos-helper/releases)  
- **Linux**: Download `GoogleTakeoutHelper` from [Releases](https://github.com/yourusername/google-takeout-live-photos-helper/releases)

**Works immediately - no Python, no command line, no technical knowledge needed!** 🎉

## 📋 Setting Up Your Google Takeout Data

**IMPORTANT**: Before using this tool, you need to properly set up your Google Takeout data:

1. **Download Google Takeout**: Go to [Google Takeout](https://takeout.google.com) and export your Google Photos
2. **Unzip all files**: Google Takeout gives you multiple ZIP files - unzip ALL of them
3. **Create Takeout folder**: Create a folder called `Takeout`
4. **Merge all exports**: Move all the unzipped `Takeout` folders into your main `Takeout` folder

**Expected structure:**
```
Takeout/                          # ← Your main folder
├── Google Photos/
│   ├── Photos from 2023/
│   │   ├── IMG_1234.HEIC        # ← Still image
│   │   ├── IMG_1234.MOV         # ← Live Photo video
│   │   └── IMG_5678.JPG
│   └── Photos from 2022/
│       ├── IMG_9999.HEIC
│       └── Videos/
│           └── IMG_9999.MOV     # ← Cross-folder Live Photo
└── (other Google services data)
```

## 🖥️ Using the GUI (Easiest)

1. **Launch the app** (download from releases or run `python google_takeout_live_photos_helper.py --gui`)
2. **Select your Takeout folder** - click "Browse Takeout Folder"
3. **Choose output location** - click "Browse Output Folder" 
4. **Check "Dry run"** to preview first (recommended!)
5. **Click "🚀 Process Photos"**
6. **Review results** and run again without dry run if happy

## 📋 **Step-by-Step CLI Walkthrough**

If you prefer using the command line, here's a complete example:

### Step 1: Prepare Your Data
```bash
# You should have a structure like this:
# Takeout/
# ├── Google Photos/
# │   ├── Photos from 2023/
# │   └── Photos from 2022/
```

### Step 2: Run the Tool
```bash
# Simple mode (recommended) - always try dry run first!
python google_takeout_live_photos_helper.py \
  --root ~/Downloads/Takeout \
  --output-dir ~/Desktop/OrganizedPhotos \
  --dry-run

# This will show you what would be created:
# ~/Desktop/OrganizedPhotos/LivePhotos/     ← Your Live Photos
# ~/Desktop/OrganizedPhotos/OtherMedia/     ← Everything else
```

### Step 3: Review and Run for Real
```bash
# If you're happy with the dry run results, run for real:
python google_takeout_live_photos_helper.py \
  --root ~/Downloads/Takeout \
  --output-dir ~/Desktop/OrganizedPhotos \
  --dedupe-leftovers

# Add --verbose to see detailed progress
# Add --show-issues to see potential problems
```

### Step 4: Check Your Results
```bash
# You'll now have organized folders:
ls ~/Desktop/OrganizedPhotos/LivePhotos/     # Your Live Photos
ls ~/Desktop/OrganizedPhotos/OtherMedia/     # Other photos/videos
```

## ⚠️ Important Notes

### Storage Warning
- **Default (symlinks)**: No extra storage used - just creates shortcuts
- **Copy mode (`--copy`)**: Doubles your storage usage ⚠️

### Deduplication
- **Enable with `--dedupe-leftovers`** to prevent same file in both output folders
- Highly recommended for cleaner results

### Orphaned Videos
- Tool automatically detects short videos that might be missing their photo partners
- Use `--show-issues` to see detailed analysis

## 🐛 Troubleshooting

**"No Google Takeout folders found"**
- Make sure you unzipped ALL the download files
- Check that you have folders named "Google Photos" or "Photos from YYYY"

**"No Live Photos found"**
- Your export might not contain Live Photos
- Check the "Other Media" folder for all your files

**GUI won't launch**
- Download the standalone executable instead (no Python needed)
- Or install tkinter: `brew install python-tk` (macOS)

## 🔧 For Developers

Want to contribute or modify the code? See the [Developer Guide](docs/DEVELOPER_GUIDE.md) for:
- Development setup and testing
- Code quality tools and standards  
- Architecture overview and design patterns
- Building and distribution instructions

## 🤝 Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the absolute pain the ass live photos from Google Takeout is
- Uses FFmpeg for video analysis
- Developed with AI assistance to create a professional tool for the community
