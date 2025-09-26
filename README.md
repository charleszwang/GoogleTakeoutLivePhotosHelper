# Google Takeout Live Photos Helper

**Transform your messy Google Takeout exports into organized Live Photos!**

When you export photos from Google Photos, Live Photos get split into separate image and video files. This tool puts them back together and organizes everything neatly.

## 💡 **Quick Migration Tip**

**If you still have access to Google Photos and just want to migrate to iCloud:**
1. Open Google Photos app on your phone
2. Select a whole month of photos 
3. Share → Save to Device
4. **This tool is for people who've lost access to their Google Photos account**

## 💖 Support This Project

If this tool helps you organize your Google Photos, please consider supporting its development:

<a href="https://www.paypal.com/donate/?hosted_button_id=FPEZJUYKMH7M6" target="_blank">
  <img src="https://img.shields.io/badge/Donate-PayPal-blue?logo=paypal&style=for-the-badge&logoColor=white" alt="Donate with PayPal">
</a>

⭐ **Also consider starring this repository** to help others discover it!

---

![Coverage](https://img.shields.io/badge/coverage-44%25-yellow)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)

*This project was developed with the assistance of AI to create a professional, user-friendly tool for the community.*

## 🔒 **Privacy & Security**

**Your photos stay 100% private:**
- **🏠 All processing happens locally** on your computer
- **🚫 Nothing sent to any servers** - completely offline
- **🔐 Open source** - you can see exactly what it does

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
2. **Toggle dark mode** if the interface is too bright (🌙 Dark Mode button)
3. **Select your Takeout folder** - click "Browse Takeout Folder"
4. **Choose output location** - click "Browse Output Folder" 
5. **Check "Dry run"** to preview first (recommended!)
6. **Click "🚀 Process Photos"**
7. **Review results** and run again without dry run if happy

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

## 🤝 Contributing

Contributions welcome! Feel free to open issues or submit pull requests.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Tools & Projects

**Complementary tools that work well with this project:**
- **[GooglePhotosTakeoutHelper](https://github.com/TheLastGimbus/GooglePhotosTakeoutHelper)** - Another approach to Google Takeout organization
- **[google-photos-exif](https://github.com/mattwilson1024/google-photos-exif)** - Fix EXIF data in Google Photos exports


**Why this tool is unique:**
- **🎯 Only tool** specifically designed for Google Takeout Live Photos pairing
- **🖥️ User-friendly GUI** unlike command-line alternatives
- **🆓 Free and open source** unlike expensive photo management software
- **🔄 Handles the exact problem** of split Live Photos in Takeout exports