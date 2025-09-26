#!/usr/bin/env python3
"""
GUI interface for Google Takeout Live Photos Helper

A user-friendly graphical interface that makes it easy to organize
Google Takeout Live Photos without using the command line.
"""

import os
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext, ttk
from typing import Optional

from .processor import GoogleTakeoutProcessor


class GoogleTakeoutGUI:
    """Main GUI application class."""

    def __init__(self, root: tk.Tk):
        """Initialize the GUI application."""
        self.root = root
        self.root.title("Google Takeout Live Photos Helper")
        self.root.geometry("800x700")
        self.root.resizable(True, True)

        # Configure style
        style = ttk.Style()
        style.theme_use("clam")

        # Variables for user inputs
        self.root_dir = tk.StringVar()
        self.pairs_dir = tk.StringVar()
        self.leftovers_dir = tk.StringVar()
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

    def setup_ui(self) -> None:
        """Set up the user interface."""
        # Create main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        current_row = 0

        # Title
        title_label = ttk.Label(
            main_frame,
            text="Google Takeout Live Photos Helper",
            font=("Arial", 16, "bold"),
        )
        title_label.grid(row=current_row, column=0, columnspan=3, pady=(0, 20))
        current_row += 1

        # Description
        description = (
            "Organize your Google Takeout exports by matching Live Photos pairs\n"
            "and separating standalone media files into organized directories."
        )
        desc_label = ttk.Label(main_frame, text=description, justify=tk.CENTER)
        desc_label.grid(row=current_row, column=0, columnspan=3, pady=(0, 20))
        current_row += 1

        # Directory selection section
        self.setup_directory_section(main_frame, current_row)
        current_row += 4

        # Options section
        current_row = self.setup_options_section(main_frame, current_row)

        # Action buttons
        current_row = self.setup_action_buttons(main_frame, current_row)

        # Progress section
        current_row = self.setup_progress_section(main_frame, current_row)

        # Results/log section
        self.setup_results_section(main_frame, current_row)

    def setup_directory_section(self, parent: ttk.Frame, start_row: int) -> None:
        """Set up the directory selection section."""
        # Section title
        dir_title = ttk.Label(parent, text="Directory Selection", font=("Arial", 12, "bold"))
        dir_title.grid(row=start_row, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))

        # Google Takeout directory
        ttk.Label(parent, text="Google Takeout Directory:").grid(
            row=start_row + 1, column=0, sticky=tk.W, pady=5
        )
        ttk.Entry(parent, textvariable=self.root_dir, width=50).grid(
            row=start_row + 1, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5
        )
        ttk.Button(
            parent, text="Browse...", command=lambda: self.browse_directory(self.root_dir)
        ).grid(row=start_row + 1, column=2, padx=(5, 0), pady=5)

        # Pairs output directory
        ttk.Label(parent, text="Live Photos Pairs Output:").grid(
            row=start_row + 2, column=0, sticky=tk.W, pady=5
        )
        ttk.Entry(parent, textvariable=self.pairs_dir, width=50).grid(
            row=start_row + 2, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5
        )
        ttk.Button(
            parent, text="Browse...", command=lambda: self.browse_directory(self.pairs_dir)
        ).grid(row=start_row + 2, column=2, padx=(5, 0), pady=5)

        # Leftovers output directory
        ttk.Label(parent, text="Other Media Output:").grid(
            row=start_row + 3, column=0, sticky=tk.W, pady=5
        )
        ttk.Entry(parent, textvariable=self.leftovers_dir, width=50).grid(
            row=start_row + 3, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5
        )
        ttk.Button(
            parent, text="Browse...", command=lambda: self.browse_directory(self.leftovers_dir)
        ).grid(row=start_row + 3, column=2, padx=(5, 0), pady=5)

    def setup_options_section(self, parent: ttk.Frame, start_row: int) -> int:
        """Set up the options section."""
        # Section title
        options_title = ttk.Label(parent, text="Options", font=("Arial", 12, "bold"))
        options_title.grid(row=start_row, column=0, columnspan=3, sticky=tk.W, pady=(20, 10))
        start_row += 1

        # Options frame
        options_frame = ttk.LabelFrame(parent, text="Processing Options", padding="10")
        options_frame.grid(row=start_row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        options_frame.columnconfigure(1, weight=1)

        # Copy files option
        ttk.Checkbutton(
            options_frame,
            text="Copy files instead of creating symbolic links",
            variable=self.copy_files,
        ).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=2)

        # Dry run option
        ttk.Checkbutton(
            options_frame,
            text="Dry run (preview changes without making them)",
            variable=self.dry_run,
        ).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=2)

        # Verbose option
        ttk.Checkbutton(
            options_frame, text="Verbose logging", variable=self.verbose
        ).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=2)

        # Deduplication option
        ttk.Checkbutton(
            options_frame,
            text="Remove duplicate files from leftovers",
            variable=self.dedupe_leftovers,
        ).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=2)

        # Show issues option
        ttk.Checkbutton(
            options_frame,
            text="Show detailed issue report after processing",
            variable=self.show_issues,
        ).grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=2)

        # Max duration setting
        duration_frame = ttk.Frame(options_frame)
        duration_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(duration_frame, text="Max video duration for Live Photos (seconds):").pack(
            side=tk.LEFT
        )
        duration_spinbox = ttk.Spinbox(
            duration_frame,
            from_=0.0,
            to=30.0,
            increment=0.5,
            textvariable=self.max_duration,
            width=10,
        )
        duration_spinbox.pack(side=tk.LEFT, padx=(10, 0))

        ttk.Label(
            options_frame,
            text="💡 Tip: Use dry run first to preview what will happen!",
            foreground="blue",
        ).grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))

        return start_row + 1

    def setup_action_buttons(self, parent: ttk.Frame, start_row: int) -> int:
        """Set up the action buttons."""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=start_row, column=0, columnspan=3, pady=20)

        # Process button
        self.process_button = ttk.Button(
            button_frame,
            text="🚀 Process Photos",
            command=self.start_processing,
            style="Accent.TButton",
        )
        self.process_button.pack(side=tk.LEFT, padx=5)

        # Stop button
        self.stop_button = ttk.Button(
            button_frame, text="⏹ Stop", command=self.stop_processing, state="disabled"
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Clear log button
        clear_button = ttk.Button(button_frame, text="🗑 Clear Log", command=self.clear_log)
        clear_button.pack(side=tk.LEFT, padx=5)

        return start_row + 1

    def setup_progress_section(self, parent: ttk.Frame, start_row: int) -> int:
        """Set up the progress section."""
        # Progress bar
        self.progress = ttk.Progressbar(parent, mode="indeterminate")
        self.progress.grid(row=start_row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)

        # Status label
        self.status_label = ttk.Label(parent, text="Ready to process photos")
        self.status_label.grid(row=start_row + 1, column=0, columnspan=3, pady=5)

        return start_row + 2

    def setup_results_section(self, parent: ttk.Frame, start_row: int) -> None:
        """Set up the results/log section."""
        # Results title
        results_title = ttk.Label(parent, text="Processing Log", font=("Arial", 12, "bold"))
        results_title.grid(row=start_row, column=0, columnspan=3, sticky=tk.W, pady=(20, 5))

        # Log text area
        self.log_text = scrolledtext.ScrolledText(
            parent, height=15, wrap=tk.WORD, font=("Consolas", 10)
        )
        self.log_text.grid(
            row=start_row + 1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5
        )

        # Configure grid weight for resizing
        parent.rowconfigure(start_row + 1, weight=1)

    def center_window(self) -> None:
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def browse_directory(self, var: tk.StringVar) -> None:
        """Open directory browser dialog."""
        directory = filedialog.askdirectory(title="Select Directory")
        if directory:
            var.set(directory)

    def log_message(self, message: str, level: str = "INFO") -> None:
        """Add a message to the log."""
        self.log_text.insert(tk.END, f"[{level}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def clear_log(self) -> None:
        """Clear the log text area."""
        self.log_text.delete(1.0, tk.END)

    def update_status(self, message: str) -> None:
        """Update the status label."""
        self.status_label.config(text=message)
        self.root.update_idletasks()

    def validate_inputs(self) -> bool:
        """Validate user inputs before processing."""
        if not self.root_dir.get():
            messagebox.showerror("Error", "Please select a Google Takeout directory")
            return False

        if not os.path.isdir(self.root_dir.get()):
            messagebox.showerror("Error", "Google Takeout directory does not exist")
            return False

        if not self.pairs_dir.get():
            messagebox.showerror("Error", "Please select an output directory for Live Photos pairs")
            return False

        if not self.leftovers_dir.get():
            messagebox.showerror("Error", "Please select an output directory for other media")
            return False

        # Check if output directories are the same
        if self.pairs_dir.get() == self.leftovers_dir.get():
            messagebox.showerror(
                "Error", "Pairs and leftovers directories must be different"
            )
            return False

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

            # Create processor
            self.processor = GoogleTakeoutProcessor(
                root_dir=self.root_dir.get(),
                pairs_dir=self.pairs_dir.get(),
                leftovers_dir=self.leftovers_dir.get(),
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
                    if (self.processor.stats['duplicate_names'] > 0 or 
                        self.processor.stats['potential_issues'] > 0):
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
        if stats.get('duplicate_names', 0) > 0 or stats.get('potential_issues', 0) > 0:
            result_message += f"\n⚠️ Warnings:\n"
            if stats.get('duplicate_names', 0) > 0:
                result_message += f"• {stats['duplicate_names']} sets of duplicate file names\n"
            if stats.get('potential_issues', 0) > 0:
                result_message += f"• {stats['potential_issues']} potential matching conflicts\n"

        result_message += f"""
📁 Output locations:
• Live Photos pairs: {self.pairs_dir.get()}
• Other media: {self.leftovers_dir.get()}
"""

        if self.dry_run.get():
            result_message += "\n⚠️ This was a dry run - no files were actually moved or copied."

        messagebox.showinfo("Processing Complete", result_message)

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
        
        # Recommendations
        report.append("\n💡 RECOMMENDATIONS:")
        report.append("   1. Check for duplicate exports in your Google Takeout")
        report.append("   2. Consider manually reviewing conflicted files")
        report.append("   3. Use verbose mode for more detailed logging")
        report.append("   4. Ensure proper Google Takeout folder structure")
        report.append("=" * 60)
        
        return "\n".join(report)


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
