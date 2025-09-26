# User Guide - Google Takeout Live Photos Helper

**Simple, no-technical-knowledge-required guide for organizing your Google Photos exports.**

## 💡 **Do You Still Have Google Photos Access?**

**If you can still access Google Photos and just want to migrate to iCloud:**
1. Open Google Photos app on your phone
2. Select a whole month of photos 
3. Share → Save to Device
4. Repeat for all your photos

**This tool is for people who've lost access to their Google Photos account or have massive exports that are too big to download via the app.**

## 🔒 **Privacy & Security**

**Your photos are completely private and secure:**

- **🏠 Everything happens on your computer** - no cloud processing
- **🚫 No data sent anywhere** - your photos never leave your device
- **🔒 Works offline** - no internet connection needed
- **👀 No tracking** - the tool doesn't collect any information about you
- **🔐 Open source** - you can see exactly what the code does

**Perfect for sensitive photos - everything stays private on your device.**

## 🎯 What This Tool Does

When you export photos from Google Photos, Live Photos get split into separate image and video files. This tool puts them back together and organizes everything neatly.

**Before:** Messy folders with thousands of scattered files  
**After:** Clean folders with Live Photos paired up and other media organized

## 📥 Download & Run

### Step 1: Download the App
- **Mac users**: Download `GoogleTakeoutHelper.app`
- **Windows users**: Download `GoogleTakeoutHelper.exe`  
- **Linux users**: Download `GoogleTakeoutHelper`

### Step 2: Run the App
- **Mac**: Double-click the app (might need to allow in Security preferences)
- **Windows**: Double-click the .exe file (might show security warning - click "Run anyway")
- **Linux**: Right-click → Properties → Make executable, then double-click

**No installation required!** The app runs immediately.

## 📋 Preparing Your Google Takeout Data

### Before Using the Tool

1. **Download Google Takeout**
   - Go to [Google Takeout](https://takeout.google.com)
   - Select Google Photos
   - Download (you'll get multiple ZIP files)

2. **Unzip Everything**
   - Unzip ALL the ZIP files you downloaded
   - You'll get multiple "Takeout" folders

3. **Merge the Folders**
   - Create one main "Takeout" folder
   - Move all the unzipped "Takeout" contents into this main folder

**Expected result:**
```
Takeout/                    ← Your main folder
├── Google Photos/
│   ├── Photos from 2023/
│   ├── Photos from 2022/
│   └── ...
```

## 🖥️ Using the App

### Step 1: Select Your Google Takeout Folder
1. Click "Browse..." next to "Google Takeout Directory"
2. Find and select your main "Takeout" folder
3. The app will automatically suggest an output location

### Step 2: Choose Output Location
1. Click "Browse..." next to "Output Directory"
2. Choose where you want your organized photos
3. The app will create two subfolders automatically:
   - `LivePhotos/` - Your Live Photos (photo + video pairs)
   - `OtherMedia/` - All other photos and videos

### Step 3: Choose Options

**Recommended settings for most users:**
- ✅ **Dry run** (preview first - always recommended!)
- ✅ **Remove duplicate files** (cleaner results)
- ❌ **Copy files** (leave unchecked to save storage space)

**Understanding the options:**

**"Dry run"** - Shows what will happen without actually moving files
- ✅ **Always use this first** to preview results
- Uncheck only when you're happy with the preview

**"Copy files instead of symbolic links"**  
- ❌ **Leave unchecked** (recommended) - saves storage space
- ✅ **Check only if** you need actual file copies
- ⚠️ **Warning**: Checking this will double your storage usage!

**"Remove duplicate files from leftovers"**
- ✅ **Recommended** - prevents the same photo appearing in both folders
- Ensures clean organization

### Step 4: Process Your Photos
1. Click "🚀 Process Photos"
2. Watch the progress bar and log messages
3. Review the results summary when complete

## 📊 Understanding Results

### What You'll See

**Processing Summary:**
```
📊 PROCESSING SUMMARY
📁 Files scanned: 1,234
📸 Live Photos found:
   Same folder pairs: 45
   Cross folder pairs: 12
   Total pairs: 57
📄 Other media files: 1,120
```

**Output Folders:**
- **LivePhotos/**: Contains numbered Live Photo pairs
  - `00001_IMG_1234__STILL.HEIC` + `00001_IMG_1234__VIDEO.MOV`
- **OtherMedia/**: Contains all other photos and videos
  - `L000001__IMG_5678.JPG`

### Warnings You Might See

**"Duplicate file names found"**
- Google Takeout sometimes exports the same file multiple times
- The tool will warn you about this
- Usually not a problem - tool handles it automatically

**"Orphaned videos found"**
- Short videos without matching photos
- Might be Live Photos missing their photo partner
- Review these manually if needed

## 🎉 What You Get

### Organized Folders
- **LivePhotos/**: All your Live Photos properly paired
- **OtherMedia/**: All other photos and videos
- **Manifest files**: Detailed logs of what was processed

### No More Mess
- No more hunting through thousands of files
- Live Photos are back together
- Easy to import into other photo apps
- Clear organization you can understand

## 🆘 Need Help?

### Common Issues

**"No Google Takeout folders found"**
- Make sure you unzipped ALL the download files
- Check that you have folders named "Google Photos" or "Photos from YYYY"

**"App won't open" (Mac)**
- Right-click the app → Open
- Or: System Preferences → Security & Privacy → Allow

**"Windows protected your PC" (Windows)**
- Click "More info" → "Run anyway"
- This is normal for apps that aren't signed

**"No Live Photos found"**
- Your export might not contain Live Photos
- Check the "Other Media" folder for all your files
- Use "Show detailed issue report" to see what was found

### Getting More Help
- Enable "Show detailed issue report" for more information
- Use "Dry run" mode to preview without making changes
- Check the project's GitHub page for more help

## 🎊 Success!

You now have your Google Photos organized and ready to use! Your Live Photos are back together, and everything else is neatly sorted. No more digging through endless folders! 📸✨
