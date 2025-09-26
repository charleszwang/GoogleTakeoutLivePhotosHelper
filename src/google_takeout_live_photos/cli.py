#!/usr/bin/env python3
"""
Command line interface for Google Takeout Live Photos Helper.

This module provides the command-line interface for the Google Takeout Live Photos Helper,
supporting both GUI and CLI modes with comprehensive argument validation and error handling.
"""

import argparse
import os
import sys
from pathlib import Path

from .processor import GoogleTakeoutProcessor
from ._version import __version__, DISPLAY_VERSION


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description=f"Google Takeout Live Photos Helper v{__version__} - Organize Live Photos pairs and standalone media files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --gui                                                           # Launch GUI
  %(prog)s --root ./Takeout --output-dir ./ProcessedPhotos                 # Single output dir (recommended)
  %(prog)s --root ./Takeout --out-pairs ./pairs --out-leftovers ./leftovers # Traditional mode
  %(prog)s --root ./Takeout --output-dir ./ProcessedPhotos --copy --verbose
        """)
    
    parser.add_argument("--gui", action="store_true",
                       help="Launch the graphical user interface")
    parser.add_argument("--root",
                       help="Root directory with unzipped Google Takeout data")
    parser.add_argument("--out-pairs",
                       help="Output directory for matched Live Photos pairs")
    parser.add_argument("--out-leftovers",
                       help="Output directory for unmatched media files")
    parser.add_argument("--output-dir",
                       help="Single output directory (will create LivePhotos/ and OtherMedia/ subdirectories)")
    parser.add_argument("--copy", action="store_true",
                       help="Copy files instead of creating symlinks (WARNING: doubles storage usage)")
    parser.add_argument("--dry-run", action="store_true",
                       help="Show what would be done without making changes")
    parser.add_argument("--verbose", action="store_true",
                       help="Enable verbose logging")
    parser.add_argument("--live-max-seconds", type=float, default=6.0,
                       help="Maximum video duration for cross-folder pairing (default: 6.0, 0 disables)")
    parser.add_argument("--dedupe-leftovers", action="store_true",
                       help="Skip duplicate files in leftovers (prevents same file in both output folders)")
    parser.add_argument("--show-issues", action="store_true",
                       help="Show detailed report of potential issues and conflicts")
    parser.add_argument("--version", action="version", version=f"Google Takeout Live Photos Helper {DISPLAY_VERSION}")
    
    args = parser.parse_args()

    # Launch GUI if requested
    if args.gui:
        try:
            from .gui import main as gui_main
            gui_main()
        except ImportError as e:
            print(f"Error: Could not launch GUI: {e}", file=sys.stderr)
            print("Make sure tkinter is installed (usually comes with Python)", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error launching GUI: {e}", file=sys.stderr)
            sys.exit(1)
        return

    # CLI mode - require arguments
    if not args.root:
        parser.error("--root is required when not using --gui")
    
    # Handle output directory configuration
    if args.output_dir:
        # Single output directory mode (recommended)
        output_base = Path(args.output_dir)
        args.out_pairs = str(output_base / "LivePhotos")
        args.out_leftovers = str(output_base / "OtherMedia")
        print(f"📁 Using single output directory mode:")
        print(f"   Live Photos: {args.out_pairs}")
        print(f"   Other Media: {args.out_leftovers}")
    else:
        # Traditional two-directory mode
        if not args.out_pairs:
            parser.error("--out-pairs is required when not using --gui or --output-dir")
        if not args.out_leftovers:
            parser.error("--out-leftovers is required when not using --gui or --output-dir")

    # Validate input directory
    if not os.path.isdir(args.root):
        print(f"Error: Directory does not exist: {args.root}", file=sys.stderr)
        sys.exit(1)

    # Create processor and run
    try:
        processor = GoogleTakeoutProcessor(
            root_dir=args.root,
            pairs_dir=args.out_pairs,
            leftovers_dir=args.out_leftovers,
            copy_files=args.copy,
            dry_run=args.dry_run,
            verbose=args.verbose,
            max_video_duration=args.live_max_seconds,
            dedupe_leftovers=args.dedupe_leftovers
        )
        
        processor.process()
        
        # Show detailed issues if requested
        if args.show_issues and not args.verbose:  # verbose already shows issues
            processor.print_detailed_issues()
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
