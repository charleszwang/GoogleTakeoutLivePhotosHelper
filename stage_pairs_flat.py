#!/usr/bin/env python3
import os, sys, argparse, shutil, subprocess, hashlib
from collections import defaultdict

STILL_EXT = {".heic", ".jpg", ".jpeg", ".png"}
VIDEO_EXT = {".mov", ".mp4"}
ALL_EXT   = STILL_EXT | VIDEO_EXT
HASH_CHUNK = 1 << 20  # 1 MiB

def safe_link_or_copy(src, dst, copy=False):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if copy:
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
        return
    try:
        if not os.path.exists(dst):
            os.symlink(src, dst)
    except OSError:
        if not os.path.exists(dst):
            shutil.copy2(src, dst)

def ff_duration(path):
    try:
        r = subprocess.run(
            ["ffprobe","-v","error","-select_streams","v:0",
             "-show_entries","format=duration","-of","default=nw=1:nk=1", path],
            text=True, capture_output=True, check=False
        )
        s = (r.stdout or "").strip()
        return float(s) if s else None
    except Exception:
        return None

def sha1(path):
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(HASH_CHUNK), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser(
        description=("Stage Live pairs into ONE flat folder and ALL remaining photos/videos "
                     "into ONE flat leftovers folder.\n"
                     "Pass A: same-folder exact-name. Pass B: cross-folder exact-name (unique)."))
    ap.add_argument("--root", required=True, help="Top folder with your unzipped Takeout parts (e.g. .../Takeout)")
    ap.add_argument("--out-pairs", required=True, help="Single flat folder for matched pairs")
    ap.add_argument("--out-leftovers", required=True, help="Single flat folder for everything not paired")
    ap.add_argument("--copy", action="store_true", help="Copy files instead of symlinking (better Finder previews)")
    ap.add_argument("--dry-run", action="store_true", help="Plan only; no files written")
    ap.add_argument("--verbose", action="store_true", help="Print per-file actions")
    ap.add_argument("--live-max-seconds", type=float, default=6.0,
                    help="Cross-folder pairing only if video duration <= this (0 disables this check)")
    ap.add_argument("--dedupe-leftovers", action="store_true",
                    help="Skip leftovers whose content hash matches a paired file or a previously-copied leftover")
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    out_pairs = os.path.abspath(args.out_pairs)
    out_left  = os.path.abspath(args.out_leftovers)

    if not os.path.isdir(root):
        print(f"[error] not a directory: {root}", file=sys.stderr); sys.exit(1)
    if not args.dry_run:
        os.makedirs(out_pairs, exist_ok=True)
        os.makedirs(out_left, exist_ok=True)

    # Index by (dir, base) and globally by base
    by_dir_base = defaultdict(lambda: {"stills": [], "videos": []})
    stills_by_base = defaultdict(list)
    videos_by_base = defaultdict(list)

    total_scanned = 0
    for dp, _, files in os.walk(root):
        for f in files:
            total_scanned += 1
            ext = os.path.splitext(f)[1].lower()
            if ext not in ALL_EXT:
                continue
            base = os.path.splitext(f)[0]  # exact basename (no '(1)' stripping)
            full = os.path.join(dp, f)
            key  = (dp, base)
            if ext in STILL_EXT:
                by_dir_base[key]["stills"].append(full)
                stills_by_base[base].append(full)
            else:
                by_dir_base[key]["videos"].append(full)
                videos_by_base[base].append(full)

    # Pass A: same-folder exact 1:1
    used = set()
    pairs = []  # (match_type, base, still, video)
    for (dp, base), rec in by_dir_base.items():
        s_list, v_list = rec["stills"], rec["videos"]
        if len(s_list) == 1 and len(v_list) == 1:
            still, video = s_list[0], v_list[0]
            pairs.append(("same_dir", base, still, video))
            used.add(still); used.add(video)

    # Pass B: cross-folder exact 1:1 (unique globally), optional live-like duration check
    for base in sorted(set(stills_by_base.keys()) | set(videos_by_base.keys())):
        s_cands = [p for p in stills_by_base.get(base, []) if p not in used]
        v_cands = [p for p in videos_by_base.get(base, []) if p not in used]
        if len(s_cands) == 1 and len(v_cands) == 1:
            still, video = s_cands[0], v_cands[0]
            if args.live_max_seconds and args.live_max_seconds > 0:
                dur = ff_duration(video)
                if dur is None or dur > args.live_max_seconds:
                    continue
            pairs.append(("cross_dir", base, still, video))
            used.add(still); used.add(video)

    # Prepare manifests
    pairs_manifest = os.path.join(out_pairs, "manifest_pairs.tsv")
    left_manifest  = os.path.join(out_left,  "manifest_leftovers.tsv")
    if not args.dry_run:
        with open(pairs_manifest, "w") as mf:
            mf.write("pair_id\tmatch_type\tbasename\tstill_src\tvideo_src\tstill_out\tvideo_out\n")
        with open(left_manifest, "w") as lf:
            lf.write("left_id\taction\tsrc\tout_or_reason\n")

    # Stage PAIRS into ONE flat folder (numbered)
    pair_count = 0
    pair_hashes = set()  # content hashes of staged pair files (for dedupe)
    for match_type, base, still, video in pairs:
        pair_count += 1
        prefix = f"{pair_count:05d}_{base}"
        s_ext = os.path.splitext(still)[1]
        v_ext = os.path.splitext(video)[1]
        out_still = os.path.join(out_pairs, f"{prefix}__STILL{s_ext}")
        out_video = os.path.join(out_pairs, f"{prefix}__VIDEO{v_ext}")
        if args.verbose:
            print(f"[pair:{match_type}] {still} + {video} -> {out_still} , {out_video}")
        if not args.dry_run:
            safe_link_or_copy(still, out_still, copy=args.copy)
            safe_link_or_copy(video, out_video, copy=args.copy)
            # log
            with open(pairs_manifest, "a") as mf:
                mf.write(f"{prefix}\t{match_type}\t{base}\t{still}\t{video}\t{out_still}\t{out_video}\n")
            # record hashes for dedupe (hash the staged copies for consistency)
            if args.dedupe_leftovers:
                try: pair_hashes.add(sha1(out_still))
                except Exception: pass
                try: pair_hashes.add(sha1(out_video))
                except Exception: pass

    # Stage LEFTOVERS into ONE flat folder (numbered) with optional dedupe
    left_id = 0
    staged_left = 0
    skipped_dupe = 0
    leftovers_hashes = set()  # hashes of leftovers we've already copied this run

    for dp, _, files in os.walk(root):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext not in ALL_EXT:
                continue
            src = os.path.join(dp, f)
            if src in used:
                continue  # part of a pair already staged
            left_id += 1
            out_path = os.path.join(out_left, f"L{left_id:06d}__{f}")

            if args.dedupe_leftovers and not args.dry_run:
                try:
                    h = sha1(src)
                except Exception:
                    h = None
                if h and (h in pair_hashes or h in leftovers_hashes):
                    # skip duplicate
                    skipped_dupe += 1
                    if args.verbose:
                        print(f"[skip-dup] {src}")
                    with open(left_manifest, "a") as lf:
                        lf.write(f"L{left_id:06d}\tSKIP_DUP\t{src}\tduplicate-of-pairs-or-leftovers\n")
                    continue
                if h:
                    leftovers_hashes.add(h)

            if args.verbose:
                print(f"[leftover] {src} -> {out_path}")
            if not args.dry_run:
                safe_link_or_copy(src, out_path, copy=args.copy)
                with open(left_manifest, "a") as lf:
                    lf.write(f"L{left_id:06d}\tCOPIED\t{src}\t{out_path}\n")
            staged_left += 1

    # Summary
    same_ct  = sum(1 for m,_,_,_ in pairs if m == "same_dir")
    cross_ct = sum(1 for m,_,_,_ in pairs if m == "cross_dir")
    print("\n--- Summary ---")
    print(f"Scanned files:        {total_scanned}")
    print(f"Pairs (same folder):  {same_ct}")
    print(f"Pairs (cross folder): {cross_ct}")
    print(f"Total pairs staged:   {pair_count}")
    print(f"Leftovers staged:     {staged_left}")
    if args.dedupe_leftovers:
        print(f"Leftovers skipped (dupe): {skipped_dupe}")
    print(f"Pairs dir:            {out_pairs}")
    if not args.dry_run:
        print(f"Pairs manifest:       {pairs_manifest}")
        print(f"Leftovers dir:        {out_left}")
        print(f"Leftovers manifest:   {left_manifest}")
    else:
        print(f"Leftovers dir:        {out_left} (dry run)")
        print("(dry run; no files written)")

if __name__ == "__main__":
    main()
