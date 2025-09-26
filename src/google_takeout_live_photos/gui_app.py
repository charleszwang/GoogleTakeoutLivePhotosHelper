#!/usr/bin/env python3
"""
Standalone GUI application entry point for Google Takeout Live Photos Helper.

This module is designed specifically for creating standalone executables
that launch directly into the GUI without command-line interface.
"""

import sys
import tkinter as tk
from pathlib import Path

# Ensure the package can be imported
try:
    from .gui import GoogleTakeoutGUI
except ImportError:
    # Fallback for standalone executable
    sys.path.insert(0, str(Path(__file__).parent))
    from gui import GoogleTakeoutGUI


def main():
    """Main entry point for standalone GUI application."""
    # Create the main window
    root = tk.Tk()
    
    # Set application icon and properties
    root.title("Google Takeout Live Photos Helper")
    
    # Try to set a nice window icon (optional)
    try:
        # You can add an icon file later
        # root.iconbitmap('icon.ico')  # Windows
        # root.iconphoto(True, tk.PhotoImage(file='icon.png'))  # Cross-platform
        pass
    except Exception:
        pass
    
    # Create and run the application
    try:
        app = GoogleTakeoutGUI(root)
        
        # Add menu bar with donation option
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        
        # Help menu with donation
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="💖 Support This Project", command=app.show_support_info)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=lambda: tk.messagebox.showinfo(
            "About", 
            "Google Takeout Live Photos Helper v1.0\n\n"
            "Organize your Google Photos exports by matching\n"
            "Live Photos pairs and organizing media files.\n\n"
            "Free and open source software."
        ))
        
        # Handle window close event gracefully
        def on_closing():
            if app.processing:
                if tk.messagebox.askokcancel("Quit", "Processing is in progress. Do you want to quit?"):
                    app.stop_processing()
                    root.destroy()
            else:
                root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Start the GUI event loop
        root.mainloop()
        
    except KeyboardInterrupt:
        print("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        # Show error dialog if GUI fails
        try:
            tk.messagebox.showerror(
                "Application Error", 
                f"An error occurred:\n\n{str(e)}\n\nPlease check your Python installation."
            )
        except Exception:
            print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
