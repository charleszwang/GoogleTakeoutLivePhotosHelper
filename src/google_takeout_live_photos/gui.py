#!/usr/bin/env python3
"""
GUI interface for Google Takeout Live Photos Helper.

A beautiful, user-friendly graphical interface that makes it easy to organize
Google Takeout Live Photos without using the command line.

Features:
- Light blue sky theme for a pleasant experience
- Simplified directory selection with smart defaults
- Real-time processing feedback with progress tracking
- Comprehensive validation and issue reporting
- Integrated donation support for project sustainability
"""

import os
import sys
import threading
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext, ttk
from typing import Optional

from .processor import GoogleTakeoutProcessor
from ._version import __version__, DISPLAY_VERSION

# UI Theme Colors
LIGHT_THEME = {
    'bg_primary': '#FFFFFF',      # White background
    'bg_secondary': '#E6F3FF',    # Light blue for frames
    'bg_accent': '#CCE7FF',       # Accent blue for highlights
    'text_primary': '#1A365D',    # Dark blue for main text
    'text_secondary': '#2D5A87',  # Medium blue for secondary text
    'success': '#22C55E',         # Green for success messages
    'warning': '#F59E0B',         # Orange for warnings
    'error': '#EF4444',           # Red for errors
    'donate': '#3B82F6',          # Blue for donation elements
}

DARK_THEME = {
    'bg_primary': '#2D2D2D',      # Dark grey background
    'bg_secondary': '#404040',    # Medium grey for frames
    'bg_accent': '#505050',       # Lighter grey for highlights
    'text_primary': '#FFFFFF',    # White text
    'text_secondary': '#CCCCCC',  # Light grey text
    'success': '#68D391',         # Light green for success
    'warning': '#F6AD55',         # Light orange for warnings
    'error': '#FC8181',           # Light red for errors
    'donate': '#4A90E2',          # Muted blue for donation elements
}


class GoogleTakeoutGUI:
    """Main GUI application class."""

    def __init__(self, root: tk.Tk):
        """Initialize the GUI application."""
        self.root = root
        self.root.title("Google Takeout Live Photos Helper")
        self.root.geometry("1100x1000")  # Much larger to show all content
        self.root.minsize(1000, 950)  # Larger minimum size
        self.root.resizable(True, True)

        # Theme management
        self.is_dark_mode = False
        self.current_theme = LIGHT_THEME
        
        # Apply theme
        self.setup_theme()
        
        # Set window background
        self.root.configure(bg=self.current_theme['bg_primary'])

        # Variables for user inputs
        self.root_dir = tk.StringVar()
        self.output_dir = tk.StringVar()  # Single output directory
        self.copy_files = tk.BooleanVar(value=False)
        self.dry_run = tk.BooleanVar(value=True)
        self.verbose = tk.BooleanVar(value=False)
        self.max_duration = tk.DoubleVar(value=6.0)
        self.dedupe_leftovers = tk.BooleanVar(value=False)
        self.show_issues = tk.BooleanVar(value=False)

        # Processing state
        self.processing = False
        self.processor: Optional[GoogleTakeoutProcessor] = None

        self.setup_ui()
        self.center_window()

    def setup_theme(self) -> None:
        """Configure the theme based on current mode."""
        style = ttk.Style()
        
        # Use a base theme that supports customization
        style.theme_use("clam")
        
        # Configure ttk widget styles with current theme
        style.configure('TFrame', background=self.current_theme['bg_primary'])
        style.configure('TLabel', background=self.current_theme['bg_primary'], 
                       foreground=self.current_theme['text_primary'])
        
        # Entry widgets
        style.configure('TEntry', fieldbackground=self.current_theme['bg_secondary'],
                       bordercolor=self.current_theme['bg_accent'], 
                       lightcolor=self.current_theme['bg_accent'])
        
        # Buttons with attractive styling
        style.configure('TButton', background=self.current_theme['bg_accent'],
                       foreground=self.current_theme['text_primary'], font=('Arial', 9))
        style.map('TButton', background=[('active', self.current_theme['bg_secondary'])])
        
        # Accent button for important actions
        style.configure('Accent.TButton', background=self.current_theme['donate'],
                       foreground='white', font=('Arial', 10, 'bold'))
        style.map('Accent.TButton', background=[('active', '#2563EB')])
        
        # Progress bar
        style.configure('TProgressbar', background=self.current_theme['donate'],
                       troughcolor=self.current_theme['bg_secondary'])
        
        # Spinbox
        style.configure('TSpinbox', fieldbackground=self.current_theme['bg_secondary'],
                       bordercolor=self.current_theme['bg_accent'])

    def toggle_dark_mode(self) -> None:
        """Toggle between light and dark mode."""
        self.is_dark_mode = not self.is_dark_mode
        self.current_theme = DARK_THEME if self.is_dark_mode else LIGHT_THEME
        
        # Reapply theme
        self.setup_theme()
        self.root.configure(bg=self.current_theme['bg_primary'])
        
        # Update all widgets - this is a simplified approach
        # In a full implementation, you'd recursively update all widgets
        self.refresh_theme()

    def setup_ui(self) -> None:
        """Set up the beautiful user interface with light blue theme."""
        # Create main container with padding and theme
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights for responsive design
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Configure specific rows for proper expansion
        # Give most weight to the log section (last row)
        main_frame.rowconfigure(8, weight=3)  # Log section gets most space
        main_frame.rowconfigure(7, weight=0)  # Progress section - fixed size
        for i in range(7):  # Other sections - minimal weight
            main_frame.rowconfigure(i, weight=0)

        current_row = 0

        # Dark mode toggle in top right corner
        self.setup_theme_toggle(main_frame, current_row)
        
        # Elegant title with version
        title_label = ttk.Label(
            main_frame,
            text=f"Google Takeout Live Photos Helper v{__version__}",
            font=("Arial", 18, "bold"),
        )
        title_label.grid(row=current_row, column=0, columnspan=2, pady=(0, 15), sticky=tk.W)
        current_row += 1

        # Descriptive subtitle
        description = (
            "Transform your messy Google Takeout exports into organized Live Photos\n"
            "and neatly sorted media files with just a few clicks."
        )
        desc_label = ttk.Label(
            main_frame, 
            text=description, 
            justify=tk.CENTER,
            font=("Arial", 11)
        )
        desc_label.grid(row=current_row, column=0, columnspan=3, pady=(0, 10))
        current_row += 1

        # Migration tip
        tip_text = (
            "💡 Still have Google Photos access? Just use the Google Photos app:\n"
            "Select photos → Share → Save to Device (this tool is for those who lost access)"
        )
        tip_label = ttk.Label(
            main_frame,
            text=tip_text,
            justify=tk.CENTER,
            font=("Arial", 9)
        )
        tip_label.grid(row=current_row, column=0, columnspan=3, pady=(0, 10))
        current_row += 1

        # Privacy notice
        privacy_text = (
            "🔒 Privacy: All processing happens locally on your computer.\n"
            "No photos are sent to any server - everything stays private on your device."
        )
        privacy_label = ttk.Label(
            main_frame,
            text=privacy_text,
            justify=tk.CENTER,
            font=("Arial", 9)
        )
        privacy_label.grid(row=current_row, column=0, columnspan=3, pady=(0, 15))
        current_row += 1

        # Prominent donation section with enhanced styling
        self.setup_donation_section(main_frame, current_row)
        current_row += 1

        # Directory selection section
        self.setup_directory_section(main_frame, current_row)
        current_row += 4  # Adjust for new layout

        # Options section
        current_row = self.setup_options_section(main_frame, current_row)

        # Action buttons
        current_row = self.setup_action_buttons(main_frame, current_row)

        # Progress section
        current_row = self.setup_progress_section(main_frame, current_row)

        # Results/log section
        self.setup_results_section(main_frame, current_row)

    def setup_theme_toggle(self, parent: ttk.Frame, start_row: int) -> None:
        """Set up the dark mode toggle."""
        # Place in top-right corner with absolute positioning
        toggle_frame = tk.Frame(parent, bg=self.current_theme['bg_primary'])
        toggle_frame.grid(row=start_row, column=2, sticky=(tk.N, tk.E), pady=(0, 0), padx=(0, 0))
        
        self.theme_button = ttk.Button(
            toggle_frame,
            text="🌙 Dark Mode",
            command=self.toggle_dark_mode,
            style="TButton"
        )
        self.theme_button.pack()

    def refresh_theme(self) -> None:
        """Refresh all widget colors after theme change."""
        # Update main window background
        self.root.configure(bg=self.current_theme['bg_primary'])
        
        # Store widget references for updating
        self.all_frames = []
        self.all_labels = []
        self.all_checkbuttons = []
        
        def collect_widgets(widget):
            if isinstance(widget, tk.Frame):
                self.all_frames.append(widget)
            elif isinstance(widget, tk.Label):
                self.all_labels.append(widget)
            elif isinstance(widget, tk.Checkbutton):
                self.all_checkbuttons.append(widget)
            
            for child in widget.winfo_children():
                collect_widgets(child)
        
        collect_widgets(self.root)
        
        # Update all frames
        for frame in self.all_frames:
            try:
                current_bg = frame.cget('bg')
                if current_bg in ['#E6F3FF', '#404040']:  # Secondary backgrounds
                    frame.configure(bg=self.current_theme['bg_secondary'])
                elif current_bg in ['#CCE7FF', '#505050']:  # Accent backgrounds  
                    frame.configure(bg=self.current_theme['bg_accent'])
                elif current_bg in ['#FFFFFF', '#2D2D2D']:  # Primary backgrounds
                    frame.configure(bg=self.current_theme['bg_primary'])
            except tk.TclError:
                pass
        
        # Update all labels
        for label in self.all_labels:
            try:
                label.configure(
                    bg=self.current_theme['bg_secondary'],
                    fg=self.current_theme['text_primary']
                )
            except tk.TclError:
                pass
        
        # Update all checkbuttons
        for check in self.all_checkbuttons:
            try:
                check.configure(
                    bg=self.current_theme['bg_secondary'],
                    fg=self.current_theme['text_primary'],
                    selectcolor=self.current_theme['bg_accent']
                )
            except tk.TclError:
                pass
        
        # Update log text area
        try:
            self.log_text.configure(
                bg=self.current_theme['bg_primary'],
                fg=self.current_theme['text_primary']
            )
        except (AttributeError, tk.TclError):
            pass
        
        # Update theme button text
        self.theme_button.configure(
            text="☀️ Light Mode" if self.is_dark_mode else "🌙 Dark Mode"
        )

    def setup_donation_section(self, parent: ttk.Frame, start_row: int) -> None:
        """Set up the prominent donation section."""
        # Create donation frame with light blue background
        donate_frame = tk.Frame(parent, bg=self.current_theme['bg_secondary'], relief=tk.RAISED, bd=2)
        donate_frame.grid(row=start_row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20), padx=5)
        
        # Add title label
        title_label = tk.Label(
            donate_frame,
            text="💖 Support Development",
            bg=self.current_theme['bg_secondary'],
            fg=self.current_theme['text_primary'],
            font=("Arial", 12, "bold")
        )
        title_label.pack(pady=(10, 5))
        
        # Donation message
        donate_text = tk.Label(
            donate_frame, 
            text="If this tool helps organize your photos, please consider supporting its development!",
            bg=self.current_theme['bg_secondary'],
            fg=self.current_theme['text_primary'],
            font=("Arial", 10),
            wraplength=400
        )
        donate_text.pack(pady=(0, 8))
        
        # Donation button with accent styling
        donate_button = ttk.Button(
            donate_frame,
            text="🎁 Donate via PayPal",
            command=self.show_support_info,
            style="Accent.TButton"
        )
        donate_button.pack(pady=(0, 10))

    def setup_directory_section(self, parent: ttk.Frame, start_row: int) -> None:
        """Set up the enhanced directory selection section."""
        # Create directory frame with light blue background
        dir_frame = tk.Frame(parent, bg=self.current_theme['bg_secondary'], relief=tk.RAISED, bd=2)
        dir_frame.grid(row=start_row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15), padx=5)
        
        # Add title label
        title_label = tk.Label(
            dir_frame,
            text="📁 Directory Selection",
            bg=self.current_theme['bg_secondary'],
            fg=self.current_theme['text_primary'],
            font=("Arial", 12, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(10, 15))
        
        # Configure grid
        dir_frame.columnconfigure(1, weight=1)

        # Google Takeout directory with light blue styling
        tk.Label(
            dir_frame, 
            text="Google Takeout Directory:",
            bg=self.current_theme['bg_secondary'],
            fg=self.current_theme['text_primary'],
            font=("Arial", 10, "bold")
        ).grid(row=1, column=0, sticky=tk.W, pady=(0, 8), padx=(15, 0))
        
        self.takeout_entry = ttk.Entry(dir_frame, textvariable=self.root_dir, width=50, font=("Arial", 10))
        self.takeout_entry.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 8), padx=(15, 8))
        
        ttk.Button(
            dir_frame, 
            text="📂 Browse Takeout Folder", 
            command=self.browse_takeout_directory,
            style="TButton"
        ).grid(row=2, column=2, padx=(0, 15), pady=(0, 8))

        # Output directory with light blue styling
        tk.Label(
            dir_frame, 
            text="Output Directory:",
            bg=self.current_theme['bg_secondary'],
            fg=self.current_theme['text_primary'],
            font=("Arial", 10, "bold")
        ).grid(row=3, column=0, sticky=tk.W, pady=(8, 8), padx=(15, 0))
        
        self.output_entry = ttk.Entry(dir_frame, textvariable=self.output_dir, width=50, font=("Arial", 10))
        self.output_entry.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 8), padx=(15, 8))
        
        ttk.Button(
            dir_frame, 
            text="📂 Browse Output Folder", 
            command=self.browse_output_directory,
            style="TButton"
        ).grid(row=4, column=2, padx=(0, 15), pady=(0, 8))

        # Enhanced info about automatic subdirectories
        info_frame = tk.Frame(dir_frame, bg=self.current_theme['bg_accent'], relief=tk.RAISED, bd=1)
        info_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 10), padx=10)
        
        info_label = tk.Label(
            info_frame,
            text="💡 The tool will automatically create 'LivePhotos' and 'OtherMedia' subdirectories",
            bg=self.current_theme['bg_accent'],
            fg=self.current_theme['text_secondary'],
            font=("Arial", 9),
            padx=10,
            pady=5
        )
        info_label.pack()

    def setup_options_section(self, parent: ttk.Frame, start_row: int) -> int:
        """Set up the enhanced options section."""
        # Options frame with light blue background
        options_frame = tk.Frame(parent, bg=self.current_theme['bg_secondary'], relief=tk.RAISED, bd=2)
        options_frame.grid(row=start_row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15), padx=5)
        
        # Add title label
        title_label = tk.Label(
            options_frame,
            text="⚙️ Processing Options",
            bg=self.current_theme['bg_secondary'],
            fg=self.current_theme['text_primary'],
            font=("Arial", 12, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(10, 15), padx=15)
        
        # Configure grid
        options_frame.columnconfigure(1, weight=1)

        # Copy files option with warning
        copy_frame = tk.Frame(options_frame, bg=self.current_theme['bg_secondary'])
        copy_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=8, padx=15)
        
        # Create custom checkbutton with light blue background
        copy_check = tk.Checkbutton(
            copy_frame,
            text="Copy files instead of creating symbolic links",
            variable=self.copy_files,
            bg=self.current_theme['bg_secondary'],
            fg=self.current_theme['text_primary'],
            selectcolor=self.current_theme['bg_accent'],
            font=("Arial", 10)
        )
        copy_check.pack(side=tk.LEFT)
        
        # Warning label for copy mode with theme colors
        copy_warning = tk.Label(
            copy_frame,
            text="⚠️ Will double storage usage",
            fg=self.current_theme['warning'],
            bg=self.current_theme['bg_secondary'],
            font=("Arial", 9, "bold")
        )
        copy_warning.pack(side=tk.LEFT, padx=(10, 0))

        # Dry run option
        dry_run_check = tk.Checkbutton(
            options_frame,
            text="Dry run (preview changes without making them)",
            variable=self.dry_run,
            bg=self.current_theme['bg_secondary'],
            fg=self.current_theme['text_primary'],
            selectcolor=self.current_theme['bg_accent'],
            font=("Arial", 10)
        )
        dry_run_check.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=8, padx=15)

        # Verbose option
        verbose_check = tk.Checkbutton(
            options_frame, 
            text="Verbose logging", 
            variable=self.verbose,
            bg=self.current_theme['bg_secondary'],
            fg=self.current_theme['text_primary'],
            selectcolor=self.current_theme['bg_accent'],
            font=("Arial", 10)
        )
        verbose_check.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=8, padx=15)

        # Deduplication option with explanation
        dedupe_frame = tk.Frame(options_frame, bg=self.current_theme['bg_secondary'])
        dedupe_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=8, padx=15)
        
        dedupe_check = tk.Checkbutton(
            dedupe_frame,
            text="Remove duplicate files from leftovers (by content hash)",
            variable=self.dedupe_leftovers,
            bg=self.current_theme['bg_secondary'],
            fg=self.current_theme['text_primary'],
            selectcolor=self.current_theme['bg_accent'],
            font=("Arial", 10)
        )
        dedupe_check.pack(side=tk.LEFT)
        
        # Info tooltip with theme colors
        dedupe_info = tk.Label(
            dedupe_frame,
            text="ℹ️ Prevents same file in both folders",
            fg=self.current_theme['text_secondary'],
            bg=self.current_theme['bg_secondary'],
            font=("Arial", 9)
        )
        dedupe_info.pack(side=tk.LEFT, padx=(10, 0))

        # Show issues option
        issues_check = tk.Checkbutton(
            options_frame,
            text="Show detailed issue report after processing",
            variable=self.show_issues,
            bg=self.current_theme['bg_secondary'],
            fg=self.current_theme['text_primary'],
            selectcolor=self.current_theme['bg_accent'],
            font=("Arial", 10)
        )
        issues_check.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=8, padx=15)

        # Max duration setting
        duration_frame = tk.Frame(options_frame, bg=self.current_theme['bg_secondary'])
        duration_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=8, padx=15)

        tk.Label(
            duration_frame, 
            text="Max video duration for Live Photos (seconds):",
            bg=self.current_theme['bg_secondary'],
            fg=self.current_theme['text_primary'],
            font=("Arial", 10)
        ).pack(side=tk.LEFT)
        
        duration_spinbox = ttk.Spinbox(
            duration_frame,
            from_=0.0,
            to=30.0,
            increment=0.5,
            textvariable=self.max_duration,
            width=10,
        )
        duration_spinbox.pack(side=tk.LEFT, padx=(10, 0))

        # Enhanced tip section
        tip_frame = tk.Frame(options_frame, bg=self.current_theme['bg_accent'], relief=tk.RAISED, bd=1)
        tip_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(15, 10), padx=15)
        
        tk.Label(
            tip_frame,
            text="💡 Tip: Always use dry run first to preview what will happen!",
            bg=self.current_theme['bg_accent'],
            fg=self.current_theme['text_secondary'],
            font=("Arial", 10, "bold"),
            padx=10,
            pady=8
        ).pack()

        return start_row + 1

    def setup_action_buttons(self, parent: ttk.Frame, start_row: int) -> int:
        """Set up the enhanced action buttons section."""
        # Action buttons frame with spacing
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=start_row, column=0, columnspan=3, pady=(20, 15))

        # Main process button - large and prominent
        self.process_button = ttk.Button(
            button_frame,
            text="🚀 Process Photos",
            command=self.start_processing,
            style="Accent.TButton",
        )
        self.process_button.pack(side=tk.LEFT, padx=(0, 10), ipadx=10, ipady=5)

        # Stop button with warning style
        self.stop_button = ttk.Button(
            button_frame, 
            text="⏹ Stop", 
            command=self.stop_processing, 
            state="disabled"
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Clear log button
        clear_button = ttk.Button(
            button_frame, 
            text="🗑 Clear Log", 
            command=self.clear_log
        )
        clear_button.pack(side=tk.LEFT, padx=5)

        return start_row + 1

    def setup_progress_section(self, parent: ttk.Frame, start_row: int) -> int:
        """Set up the enhanced progress section."""
        # Progress frame with light blue background
        progress_frame = tk.Frame(parent, bg=self.current_theme['bg_secondary'], relief=tk.RAISED, bd=2)
        progress_frame.grid(row=start_row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15), padx=5)
        
        # Add title label
        title_label = tk.Label(
            progress_frame,
            text="📊 Processing Status",
            bg=self.current_theme['bg_secondary'],
            fg=self.current_theme['text_primary'],
            font=("Arial", 12, "bold")
        )
        title_label.pack(pady=(10, 10))
        
        # Progress bar with enhanced styling
        self.progress = ttk.Progressbar(progress_frame, mode="indeterminate", length=400)
        self.progress.pack(pady=(0, 8), fill=tk.X, padx=15)

        # Status label with theme colors
        self.status_label = tk.Label(
            progress_frame, 
            text="Ready to process photos",
            bg=self.current_theme['bg_secondary'],
            fg=self.current_theme['text_primary'],
            font=("Arial", 10)
        )
        self.status_label.pack(pady=(0, 10))

        return start_row + 1

    def setup_results_section(self, parent: ttk.Frame, start_row: int) -> None:
        """Set up the enhanced results/log section."""
        # Results frame with light blue background
        results_frame = tk.Frame(parent, bg=self.current_theme['bg_secondary'], relief=tk.RAISED, bd=2)
        results_frame.grid(row=start_row, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10), padx=5)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(1, weight=1)
        
        # Add title label
        title_label = tk.Label(
            results_frame,
            text="📋 Processing Log",
            bg=self.current_theme['bg_secondary'],
            fg=self.current_theme['text_primary'],
            font=("Arial", 12, "bold")
        )
        title_label.grid(row=0, column=0, pady=(10, 10), padx=15)

        # Enhanced log text area with theme colors
        self.log_text = scrolledtext.ScrolledText(
            results_frame, 
            height=12, 
            wrap=tk.WORD, 
            font=("Consolas", 10),
            bg=self.current_theme['bg_primary'],
            fg=self.current_theme['text_primary'],
            insertbackground=self.current_theme['text_primary'],
            selectbackground=self.current_theme['bg_accent']
        )
        self.log_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=15, pady=(0, 15))

        # Configure grid weight for resizing
        parent.rowconfigure(start_row, weight=1)

    def center_window(self) -> None:
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def browse_takeout_directory(self) -> None:
        """Open directory browser for Google Takeout directory."""
        # Start in user's home directory for better UX
        initial_dir = os.path.expanduser("~")
        
        directory = filedialog.askdirectory(
            title="Select Google Takeout Directory",
            initialdir=initial_dir
        )
        if directory:
            self.root_dir.set(directory)
            
            # Auto-suggest output directory next to the Takeout folder
            if not self.output_dir.get():
                suggested_output = str(Path(directory).parent / f"{Path(directory).name}_Processed")
                self.output_dir.set(suggested_output)

    def browse_output_directory(self) -> None:
        """Open directory browser for output directory."""
        # Start in same directory as Takeout folder if available
        initial_dir = os.path.expanduser("~")
        if self.root_dir.get():
            initial_dir = str(Path(self.root_dir.get()).parent)
            
        directory = filedialog.askdirectory(
            title="Select Output Directory (subdirectories will be created automatically)",
            initialdir=initial_dir
        )
        if directory:
            self.output_dir.set(directory)

    def log_message(self, message: str, level: str = "INFO") -> None:
        """Add a color-coded message to the log."""
        # Configure text tags for different log levels
        self.log_text.tag_configure("INFO", foreground=self.current_theme['text_primary'])
        self.log_text.tag_configure("SUCCESS", foreground=self.current_theme['success'], font=("Consolas", 10, "bold"))
        self.log_text.tag_configure("WARNING", foreground=self.current_theme['warning'], font=("Consolas", 10, "bold"))
        self.log_text.tag_configure("ERROR", foreground=self.current_theme['error'], font=("Consolas", 10, "bold"))
        
        # Insert message with appropriate styling
        timestamp = ""  # Could add timestamp if desired
        formatted_message = f"[{level}] {message}\n"
        
        start_index = self.log_text.index(tk.END + "-1c")
        self.log_text.insert(tk.END, formatted_message)
        end_index = self.log_text.index(tk.END + "-1c")
        
        # Apply color tag based on level
        self.log_text.tag_add(level, start_index, end_index)
        
        # Auto-scroll to bottom
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def clear_log(self) -> None:
        """Clear the log text area."""
        self.log_text.delete(1.0, tk.END)

    def update_status(self, message: str, level: str = "INFO") -> None:
        """Update the status label with appropriate styling."""
        color_map = {
            "INFO": self.current_theme['text_primary'],
            "SUCCESS": self.current_theme['success'],
            "WARNING": self.current_theme['warning'],
            "ERROR": self.current_theme['error']
        }
        
        self.status_label.config(
            text=message,
            fg=color_map.get(level, self.current_theme['text_primary'])
        )
        self.root.update_idletasks()

    def validate_inputs(self) -> bool:
        """Validate user inputs before processing."""
        if not self.root_dir.get():
            messagebox.showerror("Error", "Please select a Google Takeout directory")
            return False

        if not os.path.isdir(self.root_dir.get()):
            messagebox.showerror("Error", "Google Takeout directory does not exist")
            return False

        if not self.output_dir.get():
            messagebox.showerror("Error", "Please select an output directory")
            return False

        # Check if output directory would conflict with input
        output_path = Path(self.output_dir.get())
        input_path = Path(self.root_dir.get())
        
        if output_path == input_path:
            messagebox.showerror(
                "Error", "Output directory cannot be the same as the Google Takeout directory"
            )
            return False

        # Check if output is inside input (could cause recursion)
        try:
            output_path.relative_to(input_path)
            messagebox.showerror(
                "Error", "Output directory cannot be inside the Google Takeout directory"
            )
            return False
        except ValueError:
            # Not a subdirectory, which is good
            pass

        return True

    def start_processing(self) -> None:
        """Start the processing in a separate thread."""
        if not self.validate_inputs():
            return

        if self.processing:
            messagebox.showwarning("Warning", "Processing is already in progress")
            return

        # Clear previous log
        self.clear_log()

        # Update UI state
        self.processing = True
        self.process_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.progress.start()

        # Start processing in separate thread
        processing_thread = threading.Thread(target=self.process_photos, daemon=True)
        processing_thread.start()

    def stop_processing(self) -> None:
        """Stop the current processing."""
        self.processing = False
        self.update_status("Stopping...")

    def process_photos(self) -> None:
        """Process photos using the GoogleTakeoutProcessor."""
        try:
            self.update_status("Initializing processor...")
            self.log_message("Starting Google Takeout Live Photos processing...")

            # Create automatic subdirectories
            output_base = Path(self.output_dir.get())
            pairs_dir = output_base / "LivePhotos"
            leftovers_dir = output_base / "OtherMedia"
            
            self.log_message(f"Output directories:")
            self.log_message(f"  Live Photos: {pairs_dir}")
            self.log_message(f"  Other Media: {leftovers_dir}")

            # Create processor
            self.processor = GoogleTakeoutProcessor(
                root_dir=self.root_dir.get(),
                pairs_dir=str(pairs_dir),
                leftovers_dir=str(leftovers_dir),
                copy_files=self.copy_files.get(),
                dry_run=self.dry_run.get(),
                verbose=self.verbose.get(),
                max_video_duration=self.max_duration.get(),
                dedupe_leftovers=self.dedupe_leftovers.get(),
            )

            # Redirect logging to GUI
            self.setup_processor_logging()

            self.update_status("Scanning files...")
            self.log_message("Scanning media files...")

            # Process the photos
            self.processor.process()

            if not self.processing:  # Check if stopped
                self.log_message("Processing stopped by user", "WARNING")
                self.update_status("Processing stopped")
            else:
                self.log_message("Processing completed successfully!", "SUCCESS")
                self.update_status("Processing completed")
                self.show_results()
                
                # Show detailed issues if requested
                if self.show_issues.get() and not self.verbose.get():
                    has_issues = (self.processor.stats['duplicate_names'] > 0 or 
                                 self.processor.stats['potential_issues'] > 0 or
                                 len(self.processor.issues.get('orphaned_videos', [])) > 0)
                    if has_issues:
                        self.show_issues_dialog()

        except Exception as e:
            self.log_message(f"Error during processing: {str(e)}", "ERROR")
            self.update_status(f"Error: {str(e)}")
            messagebox.showerror("Processing Error", f"An error occurred:\n\n{str(e)}")

        finally:
            # Reset UI state
            self.processing = False
            self.process_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.progress.stop()

    def setup_processor_logging(self) -> None:
        """Set up logging redirection from processor to GUI."""
        # This is a simplified approach - in a real implementation,
        # you might want to use a custom logging handler
        original_logger_info = self.processor.logger.info
        original_logger_warning = self.processor.logger.warning
        original_logger_error = self.processor.logger.error

        def gui_info(msg):
            self.log_message(str(msg), "INFO")
            if not self.processing:
                return  # Stop if processing was cancelled

        def gui_warning(msg):
            self.log_message(str(msg), "WARNING")

        def gui_error(msg):
            self.log_message(str(msg), "ERROR")

        self.processor.logger.info = gui_info
        self.processor.logger.warning = gui_warning
        self.processor.logger.error = gui_error

    def show_results(self) -> None:
        """Show processing results."""
        if not self.processor:
            return

        stats = self.processor.stats
        total_pairs = stats["same_dir_pairs"] + stats["cross_dir_pairs"]

        result_message = f"""
Processing Complete! 📸

📊 Summary:
• Files scanned: {stats['total_scanned']:,}
• Live Photos pairs found: {total_pairs:,}
  - Same directory: {stats['same_dir_pairs']:,}
  - Cross directory: {stats['cross_dir_pairs']:,}
• Other media files: {stats['leftovers_staged']:,}
"""

        if self.dedupe_leftovers.get() and stats['leftovers_skipped'] > 0:
            result_message += f"• Duplicates skipped: {stats['leftovers_skipped']:,}\n"

        # Add warnings if present
        has_warnings = (stats.get('duplicate_names', 0) > 0 or 
                       stats.get('potential_issues', 0) > 0 or
                       len(self.processor.issues.get('orphaned_videos', [])) > 0)
        
        if has_warnings:
            result_message += f"\n⚠️ Warnings:\n"
            if stats.get('duplicate_names', 0) > 0:
                result_message += f"• {stats['duplicate_names']} sets of duplicate file names\n"
            if stats.get('potential_issues', 0) > 0:
                result_message += f"• {stats['potential_issues']} potential matching conflicts\n"
            if len(self.processor.issues.get('orphaned_videos', [])) > 0:
                orphaned_count = len(self.processor.issues['orphaned_videos'])
                result_message += f"• {orphaned_count} orphaned videos (might be Live Photos missing partners)\n"

        # Calculate output directories
        output_base = Path(self.output_dir.get())
        pairs_dir = output_base / "LivePhotos"
        leftovers_dir = output_base / "OtherMedia"

        result_message += f"""
📁 Output locations:
• Live Photos pairs: {pairs_dir}
• Other media: {leftovers_dir}
"""

        if self.dry_run.get():
            result_message += "\n⚠️ This was a dry run - no files were actually moved or copied."
        else:
            result_message += "\n\n💖 If this tool helped you, consider supporting it!"

        # Show results with donation prompt
        result = messagebox.showinfo("Processing Complete", result_message)
        
        # After showing results, offer donation (only for successful processing)
        if not self.dry_run.get() and total_pairs > 0:
            donate_response = messagebox.askyesno(
                "💖 Support Development",
                f"Great! You successfully organized {total_pairs} Live Photos!\n\n"
                "This tool is free and open source. If it saved you time, "
                "would you like to support its development with a small donation?",
                icon='question'
            )
            if donate_response:
                self.show_support_info()

    def show_issues_dialog(self) -> None:
        """Show detailed issues in a separate dialog."""
        if not self.processor:
            return
            
        # Create issues dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("⚠️ Issues and Conflicts Report")
        dialog.geometry("700x500")
        dialog.resizable(True, True)
        
        # Create scrolled text for issues
        issues_text = scrolledtext.ScrolledText(
            dialog, wrap=tk.WORD, font=("Consolas", 10), padx=10, pady=10
        )
        issues_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Generate issues report
        issues_report = self.generate_issues_report()
        issues_text.insert(tk.END, issues_report)
        issues_text.config(state=tk.DISABLED)
        
        # Add close button
        close_button = ttk.Button(dialog, text="Close", command=dialog.destroy)
        close_button.pack(pady=10)
        
        # Center the dialog
        dialog.transient(self.root)
        dialog.grab_set()

    def generate_issues_report(self) -> str:
        """Generate a detailed issues report for display."""
        if not self.processor:
            return "No processor available"
            
        report = []
        report.append("🔍 DETAILED ISSUES REPORT")
        report.append("=" * 60)
        
        # Storage warning if copy mode is enabled
        if self.copy_files.get():
            report.append("\n⚠️ STORAGE WARNING:")
            report.append("   Copy mode is enabled - this will double your storage usage!")
            report.append("   Consider using symbolic links instead if storage is limited.")
        
        # Structure warnings
        if self.processor.issues['structure_warnings']:
            report.append("\n📋 STRUCTURE WARNINGS:")
            for warning in self.processor.issues['structure_warnings']:
                report.append(f"   ⚠️  {warning}")
        
        # Duplicate names
        if self.processor.issues['duplicate_names']:
            report.append(f"\n📋 DUPLICATE FILE NAMES ({len(self.processor.issues['duplicate_names'])} issues):")
            for i, issue in enumerate(self.processor.issues['duplicate_names'][:10], 1):
                report.append(f"\n{i}. {issue['type'].upper()}: '{issue['base_name']}' ({issue['count']} files)")
                for file_path in issue['files']:
                    report.append(f"   📄 {file_path}")
            
            if len(self.processor.issues['duplicate_names']) > 10:
                remaining = len(self.processor.issues['duplicate_names']) - 10
                report.append(f"\n   ... and {remaining} more duplicate name issues")
        
        # Matching conflicts
        if self.processor.issues['matching_conflicts']:
            report.append(f"\n⚡ MATCHING CONFLICTS ({len(self.processor.issues['matching_conflicts'])} conflicts):")
            for i, conflict in enumerate(self.processor.issues['matching_conflicts'][:5], 1):
                report.append(f"\n{i}. '{conflict['base_name']}':")
                report.append(f"   📸 {conflict['still_count']} still image(s)")
                report.append(f"   🎥 {conflict['video_count']} video(s)")
                report.append(f"   ❗ Cannot determine correct Live Photo pairing")
            
            if len(self.processor.issues['matching_conflicts']) > 5:
                remaining = len(self.processor.issues['matching_conflicts']) - 5
                report.append(f"\n   ... and {remaining} more conflicts")
        
        # Orphaned videos
        if self.processor.issues['orphaned_videos']:
            report.append(f"\n🎥 ORPHANED VIDEOS ({len(self.processor.issues['orphaned_videos'])} videos):")
            report.append("-" * 40)
            
            for i, orphan in enumerate(self.processor.issues['orphaned_videos'][:10], 1):
                report.append(f"\n{i}. '{orphan['base_name']}' ({orphan['duration']:.1f}s)")
                report.append(f"   📄 {orphan['video_path']}")
                report.append(f"   💡 Short video without matching photo - might be orphaned Live Photo")
            
            if len(self.processor.issues['orphaned_videos']) > 10:
                remaining = len(self.processor.issues['orphaned_videos']) - 10
                report.append(f"\n   ... and {remaining} more orphaned videos")
        
        # Deduplication explanation
        if self.dedupe_leftovers.get():
            report.append("\n✅ DEDUPLICATION ENABLED:")
            report.append("   Files with identical content (by hash) are skipped from leftovers")
            report.append("   This prevents the same file appearing in both pairs and leftovers folders")
        
        # Recommendations
        report.append("\n💡 RECOMMENDATIONS:")
        report.append("   1. Check for duplicate exports in your Google Takeout")
        report.append("   2. Consider manually reviewing conflicted files")
        report.append("   3. Orphaned videos might need manual pairing or could be standalone clips")
        report.append("   4. Use verbose mode for more detailed logging")
        report.append("   5. Enable deduplication to prevent files in both output folders")
        report.append("=" * 60)
        
        return "\n".join(report)

    def show_support_info(self) -> None:
        """Open PayPal donation page directly."""
        import webbrowser
        
        donation_url = "https://www.paypal.com/donate/?hosted_button_id=FPEZJUYKMH7M6"
        try:
            webbrowser.open(donation_url)
        except Exception:
            messagebox.showinfo(
                "Donation Link", 
                f"Please visit this link to donate:\n\n{donation_url}"
            )


def main():
    """Main entry point for the GUI application."""
    # Create the main window
    root = tk.Tk()

    # Set up the application
    app = GoogleTakeoutGUI(root)

    # Add some style improvements
    try:
        # Try to set a nice icon (you can add an icon file later)
        # root.iconbitmap('icon.ico')
        pass
    except Exception:
        pass

    # Start the GUI event loop
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nGUI application interrupted by user")
        sys.exit(0)


if __name__ == "__main__":
    main()
