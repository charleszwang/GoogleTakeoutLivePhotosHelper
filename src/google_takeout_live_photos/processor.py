"""
Core processing logic for Google Takeout Live Photos Helper.
"""

import os
import shutil
import subprocess
import hashlib
import logging
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional, Union

# Constants
STILL_EXTENSIONS = {".heic", ".jpg", ".jpeg", ".png"}
VIDEO_EXTENSIONS = {".mov", ".mp4"}
ALL_EXTENSIONS = STILL_EXTENSIONS | VIDEO_EXTENSIONS
HASH_CHUNK_SIZE = 1 << 20  # 1 MiB

# Type aliases
FilePath = Union[str, Path]
MatchType = str
PairInfo = Tuple[MatchType, str, str, str]  # (match_type, base, still, video)


class GoogleTakeoutProcessor:
    """Main class for processing Google Takeout Live Photos."""
    
    def __init__(self, root_dir: FilePath, pairs_dir: FilePath, leftovers_dir: FilePath,
                 copy_files: bool = False, dry_run: bool = False, verbose: bool = False,
                 max_video_duration: float = 6.0, dedupe_leftovers: bool = False):
        """Initialize the processor with configuration."""
        self.root_dir = Path(root_dir).resolve()
        self.pairs_dir = Path(pairs_dir).resolve()
        self.leftovers_dir = Path(leftovers_dir).resolve()
        self.copy_files = copy_files
        self.dry_run = dry_run
        self.verbose = verbose
        self.max_video_duration = max_video_duration
        self.dedupe_leftovers = dedupe_leftovers
        
        # Setup logging
        log_level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(level=log_level, format='%(levelname)s: %(message)s')
        self.logger = logging.getLogger(__name__)
        
        # Statistics
        self.stats = {
            'total_scanned': 0,
            'same_dir_pairs': 0,
            'cross_dir_pairs': 0,
            'leftovers_staged': 0,
            'leftovers_skipped': 0,
            'duplicate_names': 0,
            'potential_issues': 0,
            'takeout_folders_found': 0
        }
        
        # Issue tracking
        self.issues = {
            'duplicate_names': [],  # Files with same base name in different locations
            'structure_warnings': [],  # Structure issues
            'matching_conflicts': []  # Potential matching problems
        }

    def safe_link_or_copy(self, src: FilePath, dst: FilePath) -> None:
        """Safely create symlink or copy file, with fallback handling."""
        dst = Path(dst)
        dst.parent.mkdir(parents=True, exist_ok=True)
        
        if dst.exists():
            self.logger.debug(f"Destination already exists: {dst}")
            return
            
        try:
            if self.copy_files:
                shutil.copy2(src, dst)
                self.logger.debug(f"Copied: {src} -> {dst}")
            else:
                os.symlink(src, dst)
                self.logger.debug(f"Linked: {src} -> {dst}")
        except OSError as e:
            # Fallback to copy if symlink fails
            if not self.copy_files:
                self.logger.warning(f"Symlink failed, copying instead: {e}")
                shutil.copy2(src, dst)
            else:
                raise

    @staticmethod
    def get_video_duration(video_path: FilePath) -> Optional[float]:
        """Get video duration using ffprobe."""
        try:
            result = subprocess.run([
                "ffprobe", "-v", "error", "-select_streams", "v:0",
                "-show_entries", "format=duration", "-of", "default=nw=1:nk=1",
                str(video_path)
            ], text=True, capture_output=True, check=False, timeout=30)
            
            duration_str = (result.stdout or "").strip()
            return float(duration_str) if duration_str else None
        except (subprocess.TimeoutExpired, ValueError, FileNotFoundError) as e:
            logging.getLogger(__name__).warning(f"Failed to get duration for {video_path}: {e}")
            return None

    def validate_takeout_structure(self) -> bool:
        """Validate that the root directory looks like a proper Google Takeout structure."""
        self.logger.info("Validating Google Takeout structure...")
        
        # Look for typical Google Takeout folder patterns
        takeout_indicators = [
            "Google Photos",
            "Takeout",
            "Photos from",
            "Google Foto",  # International versions
        ]
        
        found_indicators = []
        for root, dirs, _ in os.walk(self.root_dir):
            for dir_name in dirs:
                for indicator in takeout_indicators:
                    if indicator in dir_name:
                        found_indicators.append(os.path.join(root, dir_name))
                        self.stats['takeout_folders_found'] += 1
        
        if not found_indicators:
            self.issues['structure_warnings'].append(
                "No typical Google Takeout folder structure detected. "
                "Expected folders like 'Google Photos', 'Photos from YYYY', etc."
            )
            self.logger.warning("Directory structure doesn't look like Google Takeout")
            return False
        
        self.logger.info(f"Found {len(found_indicators)} Google Takeout folders")
        for folder in found_indicators[:5]:  # Show first 5
            self.logger.info(f"  - {folder}")
        if len(found_indicators) > 5:
            self.logger.info(f"  ... and {len(found_indicators) - 5} more")
        
        return True

    def detect_duplicate_names(self, stills_by_base: Dict, videos_by_base: Dict) -> None:
        """Detect and warn about files with duplicate base names."""
        self.logger.info("Checking for duplicate file names...")
        
        # Check for still images with duplicate names
        for base_name, file_list in stills_by_base.items():
            if len(file_list) > 1:
                self.stats['duplicate_names'] += 1
                self.issues['duplicate_names'].append({
                    'type': 'still',
                    'base_name': base_name,
                    'files': file_list,
                    'count': len(file_list)
                })
        
        # Check for videos with duplicate names
        for base_name, file_list in videos_by_base.items():
            if len(file_list) > 1:
                self.stats['duplicate_names'] += 1
                self.issues['duplicate_names'].append({
                    'type': 'video',
                    'base_name': base_name,
                    'files': file_list,
                    'count': len(file_list)
                })
        
        if self.stats['duplicate_names'] > 0:
            self.logger.warning(f"Found {self.stats['duplicate_names']} sets of files with duplicate names")
            self.logger.warning("This may cause incorrect Live Photo pairing!")

    def detect_matching_conflicts(self, stills_by_base: Dict, videos_by_base: Dict) -> None:
        """Detect potential conflicts in Live Photo matching."""
        self.logger.info("Checking for potential matching conflicts...")
        
        conflicts = 0
        for base_name in set(stills_by_base.keys()) & set(videos_by_base.keys()):
            still_count = len(stills_by_base[base_name])
            video_count = len(videos_by_base[base_name])
            
            # Multiple stills or videos with same name = potential conflict
            if still_count > 1 or video_count > 1:
                conflicts += 1
                self.issues['matching_conflicts'].append({
                    'base_name': base_name,
                    'still_count': still_count,
                    'video_count': video_count,
                    'still_files': stills_by_base[base_name],
                    'video_files': videos_by_base[base_name]
                })
        
        self.stats['potential_issues'] = conflicts
        if conflicts > 0:
            self.logger.warning(f"Found {conflicts} potential matching conflicts")
            self.logger.warning("Some Live Photos may not pair correctly due to duplicate names")

    @staticmethod
    def calculate_sha1(file_path: FilePath) -> str:
        """Calculate SHA1 hash of a file."""
        hash_obj = hashlib.sha1()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(HASH_CHUNK_SIZE), b""):
                    hash_obj.update(chunk)
            return hash_obj.hexdigest()
        except IOError as e:
            raise IOError(f"Failed to calculate hash for {file_path}: {e}") from e

    def scan_media_files(self) -> Tuple[Dict, Dict, Dict]:
        """Scan root directory and index all media files."""
        by_dir_base = defaultdict(lambda: {"stills": [], "videos": []})
        stills_by_base = defaultdict(list)
        videos_by_base = defaultdict(list)

        self.logger.info(f"Scanning directory: {self.root_dir}")
        
        for root, _, files in os.walk(self.root_dir):
            for filename in files:
                self.stats['total_scanned'] += 1
                
                ext = Path(filename).suffix.lower()
                if ext not in ALL_EXTENSIONS:
                    continue
                    
                base_name = Path(filename).stem
                full_path = os.path.join(root, filename)
                key = (root, base_name)
                
                if ext in STILL_EXTENSIONS:
                    by_dir_base[key]["stills"].append(full_path)
                    stills_by_base[base_name].append(full_path)
                else:
                    by_dir_base[key]["videos"].append(full_path)
                    videos_by_base[base_name].append(full_path)

        self.logger.info(f"Scanned {self.stats['total_scanned']} files")
        
        # Run validation and issue detection
        self.detect_duplicate_names(stills_by_base, videos_by_base)
        self.detect_matching_conflicts(stills_by_base, videos_by_base)
        
        return by_dir_base, stills_by_base, videos_by_base

    def find_pairs(self, by_dir_base: Dict, stills_by_base: Dict, videos_by_base: Dict) -> Tuple[List[PairInfo], Set[str]]:
        """Find matching photo-video pairs using two-pass algorithm."""
        used_files = set()
        pairs = []

        # Pass A: Same-folder exact 1:1 matching
        for (directory, base_name), file_lists in by_dir_base.items():
            still_list = file_lists["stills"]
            video_list = file_lists["videos"]
            
            if len(still_list) == 1 and len(video_list) == 1:
                still_path, video_path = still_list[0], video_list[0]
                pairs.append(("same_dir", base_name, still_path, video_path))
                used_files.update([still_path, video_path])
                self.stats['same_dir_pairs'] += 1

        # Pass B: Cross-folder exact 1:1 matching with optional duration check
        all_base_names = set(stills_by_base.keys()) | set(videos_by_base.keys())
        
        for base_name in sorted(all_base_names):
            unused_stills = [p for p in stills_by_base.get(base_name, []) if p not in used_files]
            unused_videos = [p for p in videos_by_base.get(base_name, []) if p not in used_files]
            
            if len(unused_stills) == 1 and len(unused_videos) == 1:
                still_path, video_path = unused_stills[0], unused_videos[0]
                
                # Check video duration if specified
                if self.max_video_duration and self.max_video_duration > 0:
                    duration = self.get_video_duration(video_path)
                    if duration is None or duration > self.max_video_duration:
                        continue
                
                pairs.append(("cross_dir", base_name, still_path, video_path))
                used_files.update([still_path, video_path])
                self.stats['cross_dir_pairs'] += 1

        self.logger.info(f"Found {len(pairs)} pairs ({self.stats['same_dir_pairs']} same-dir, {self.stats['cross_dir_pairs']} cross-dir)")
        return pairs, used_files

    def process_pairs(self, pairs: List[PairInfo]) -> Set[str]:
        """Process and stage matched pairs."""
        if not self.dry_run:
            self.pairs_dir.mkdir(parents=True, exist_ok=True)
            
        pairs_manifest = self.pairs_dir / "manifest_pairs.tsv"
        pair_hashes = set()
        
        if not self.dry_run:
            with open(pairs_manifest, "w") as f:
                f.write("pair_id\tmatch_type\tbasename\tstill_src\tvideo_src\tstill_out\tvideo_out\n")

        for i, (match_type, base_name, still_path, video_path) in enumerate(pairs, 1):
            prefix = f"{i:05d}_{base_name}"
            still_ext = Path(still_path).suffix
            video_ext = Path(video_path).suffix
            
            out_still = self.pairs_dir / f"{prefix}__STILL{still_ext}"
            out_video = self.pairs_dir / f"{prefix}__VIDEO{video_ext}"
            
            if self.verbose:
                self.logger.info(f"[pair:{match_type}] {still_path} + {video_path} -> {out_still}, {out_video}")
            
            if not self.dry_run:
                self.safe_link_or_copy(still_path, out_still)
                self.safe_link_or_copy(video_path, out_video)
                
                # Log to manifest
                with open(pairs_manifest, "a") as f:
                    f.write(f"{prefix}\t{match_type}\t{base_name}\t{still_path}\t{video_path}\t{out_still}\t{out_video}\n")
                
                # Record hashes for deduplication
                if self.dedupe_leftovers:
                    try:
                        pair_hashes.add(self.calculate_sha1(out_still))
                        pair_hashes.add(self.calculate_sha1(out_video))
                    except IOError:
                        pass  # Continue if hash calculation fails

        return pair_hashes

    def process_leftovers(self, used_files: Set[str], pair_hashes: Set[str]) -> None:
        """Process and stage leftover files."""
        if not self.dry_run:
            self.leftovers_dir.mkdir(parents=True, exist_ok=True)
            
        leftovers_manifest = self.leftovers_dir / "manifest_leftovers.tsv"
        leftovers_hashes = set()
        leftover_id = 0
        
        if not self.dry_run:
            with open(leftovers_manifest, "w") as f:
                f.write("left_id\taction\tsrc\tout_or_reason\n")

        for root, _, files in os.walk(self.root_dir):
            for filename in files:
                ext = Path(filename).suffix.lower()
                if ext not in ALL_EXTENSIONS:
                    continue
                    
                src_path = os.path.join(root, filename)
                if src_path in used_files:
                    continue  # Skip files that are part of pairs
                
                leftover_id += 1
                out_path = self.leftovers_dir / f"L{leftover_id:06d}__{filename}"
                
                # Handle deduplication
                if self.dedupe_leftovers and not self.dry_run:
                    try:
                        file_hash = self.calculate_sha1(src_path)
                        if file_hash in pair_hashes or file_hash in leftovers_hashes:
                            self.stats['leftovers_skipped'] += 1
                            if self.verbose:
                                self.logger.info(f"[skip-dup] {src_path}")
                            with open(leftovers_manifest, "a") as f:
                                f.write(f"L{leftover_id:06d}\tSKIP_DUP\t{src_path}\tduplicate-of-pairs-or-leftovers\n")
                            continue
                        leftovers_hashes.add(file_hash)
                    except IOError:
                        pass  # Continue if hash calculation fails
                
                if self.verbose:
                    self.logger.info(f"[leftover] {src_path} -> {out_path}")
                
                if not self.dry_run:
                    self.safe_link_or_copy(src_path, out_path)
                    with open(leftovers_manifest, "a") as f:
                        f.write(f"L{leftover_id:06d}\tCOPIED\t{src_path}\t{out_path}\n")
                
                self.stats['leftovers_staged'] += 1

    def process(self) -> None:
        """Main processing method."""
        if not self.root_dir.is_dir():
            raise FileNotFoundError(f"Root directory does not exist: {self.root_dir}")
        
        # Validate Google Takeout structure
        structure_valid = self.validate_takeout_structure()
        if not structure_valid and not self.dry_run:
            self.logger.warning("⚠️  Directory structure validation failed!")
            self.logger.warning("This may not be a proper Google Takeout directory.")
            self.logger.warning("Expected structure: Takeout/Google Photos/Photos from YYYY/...")
        
        # Scan and index files
        by_dir_base, stills_by_base, videos_by_base = self.scan_media_files()
        
        # Find pairs
        pairs, used_files = self.find_pairs(by_dir_base, stills_by_base, videos_by_base)
        
        # Process pairs
        pair_hashes = self.process_pairs(pairs)
        
        # Process leftovers
        self.process_leftovers(used_files, pair_hashes)
        
        # Print summary
        self.print_summary()
        
        # Print detailed issues if there are any significant problems
        if (self.stats['duplicate_names'] > 0 or self.stats['potential_issues'] > 0) and self.verbose:
            self.print_detailed_issues()

    def print_summary(self) -> None:
        """Print processing summary."""
        print("\n" + "="*50)
        print("📊 PROCESSING SUMMARY")
        print("="*50)
        
        # File statistics
        print(f"📁 Files scanned:        {self.stats['total_scanned']:,}")
        print(f"📸 Live Photos found:")
        print(f"   Same folder pairs:    {self.stats['same_dir_pairs']:,}")
        print(f"   Cross folder pairs:   {self.stats['cross_dir_pairs']:,}")
        print(f"   Total pairs:          {self.stats['same_dir_pairs'] + self.stats['cross_dir_pairs']:,}")
        print(f"📄 Other media files:    {self.stats['leftovers_staged']:,}")
        
        if self.dedupe_leftovers:
            print(f"🗑️  Duplicates skipped:    {self.stats['leftovers_skipped']:,}")
        
        # Output locations
        print(f"\n📂 Output locations:")
        print(f"   Live Photos pairs:    {self.pairs_dir}")
        print(f"   Other media:          {self.leftovers_dir}")
        
        if not self.dry_run:
            print(f"   Pairs manifest:       {self.pairs_dir / 'manifest_pairs.tsv'}")
            print(f"   Leftovers manifest:   {self.leftovers_dir / 'manifest_leftovers.tsv'}")
        
        # Warnings and issues
        if self.stats['duplicate_names'] > 0 or self.stats['potential_issues'] > 0:
            print(f"\n⚠️  WARNINGS:")
            
            if self.stats['duplicate_names'] > 0:
                print(f"   🔄 {self.stats['duplicate_names']} sets of files with duplicate names found")
                print(f"      This may affect Live Photo pairing accuracy!")
                
            if self.stats['potential_issues'] > 0:
                print(f"   ❗ {self.stats['potential_issues']} potential matching conflicts detected")
                print(f"      Some Live Photos may not pair correctly")
        
        if self.issues['structure_warnings']:
            print(f"\n📋 STRUCTURE NOTES:")
            for warning in self.issues['structure_warnings']:
                print(f"   ℹ️  {warning}")
        
        if self.dry_run:
            print(f"\n🧪 DRY RUN MODE - No files were actually moved or copied")
        else:
            print(f"\n✅ Processing completed successfully!")
            
        print("="*50)

    def print_detailed_issues(self) -> None:
        """Print detailed information about detected issues."""
        if not (self.issues['duplicate_names'] or self.issues['matching_conflicts']):
            return
            
        print(f"\n" + "="*60)
        print("🔍 DETAILED ISSUE REPORT")
        print("="*60)
        
        # Duplicate names details
        if self.issues['duplicate_names']:
            print(f"\n📋 DUPLICATE FILE NAMES ({len(self.issues['duplicate_names'])} issues):")
            print("-" * 40)
            
            for i, issue in enumerate(self.issues['duplicate_names'][:10], 1):  # Show first 10
                print(f"{i}. {issue['type'].upper()}: '{issue['base_name']}' ({issue['count']} files)")
                for file_path in issue['files']:
                    print(f"   📄 {file_path}")
                print()
            
            if len(self.issues['duplicate_names']) > 10:
                print(f"   ... and {len(self.issues['duplicate_names']) - 10} more duplicate name issues")
        
        # Matching conflicts details  
        if self.issues['matching_conflicts']:
            print(f"\n⚡ MATCHING CONFLICTS ({len(self.issues['matching_conflicts'])} conflicts):")
            print("-" * 40)
            
            for i, conflict in enumerate(self.issues['matching_conflicts'][:5], 1):  # Show first 5
                print(f"{i}. '{conflict['base_name']}':")
                print(f"   📸 {conflict['still_count']} still image(s)")
                print(f"   🎥 {conflict['video_count']} video(s)")
                print(f"   ❗ Cannot determine correct Live Photo pairing")
                print()
            
            if len(self.issues['matching_conflicts']) > 5:
                print(f"   ... and {len(self.issues['matching_conflicts']) - 5} more conflicts")
        
        print("\n💡 RECOMMENDATIONS:")
        print("   1. Check for duplicate exports in your Google Takeout")
        print("   2. Consider manually reviewing conflicted files")
        print("   3. Use --verbose flag for more detailed logging")
        print("   4. Run with --dry-run first to preview results")
        print("="*60)
