"""
Delete all non-CT state files from station_data folders.
Keep ONLY CT_*.STA files and CT-related .txt extracts.
Also check traffic (ccs_data) folders for non-CT files.
"""
import sys
import os
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

DATA_DIR = Path(r"C:\Users\owner\Downloads\Masters\Masters_Spring_2026"
                r"\Advanced Deep Learning\Traffic Project 2\data")

print("=" * 65)
print("  Purge Non-CT Files")
print("=" * 65)

total_deleted = 0
total_bytes_freed = 0

# ── 1. Clean station_data folders (2022-2025 have per-state .STA files) ──
print("\n--- Station Data Folders ---")
for year in range(2012, 2026):
    folder = DATA_DIR / f"{year}_station_data"
    if not folder.is_dir():
        continue

    deleted_count = 0
    deleted_bytes = 0
    for f in list(folder.rglob("*")):
        if not f.is_file():
            continue
        name = f.name.upper()
        # Keep CT files and any file that doesn't start with a state code
        if name.startswith("CT_") or name.startswith("CT "):
            continue
        # Keep generic files (Station_Data_Extract... etc)
        if not any(name.startswith(f"{st}_") for st in [
            "AK","AL","AR","AZ","CA","CO","DC","DE","FL","GA","HI",
            "IA","ID","IL","IN","KS","KY","LA","MA","MD","ME","MI",
            "MN","MO","MS","MT","NC","ND","NE","NH","NJ","NM","NV",
            "NY","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT",
            "VA","VT","WA","WI","WV","WY"
        ]):
            continue  # Not a state file, keep it

        size = f.stat().st_size
        f.unlink()
        deleted_count += 1
        deleted_bytes += size

    if deleted_count > 0:
        print(f"  {folder.name}: deleted {deleted_count} non-CT files "
              f"({deleted_bytes / 1024 / 1024:.1f} MB freed)")
        total_deleted += deleted_count
        total_bytes_freed += deleted_bytes
    else:
        remaining = list(folder.iterdir())
        print(f"  {folder.name}: clean ({len(remaining)} file(s) kept)")

# ── 2. Check traffic data folders for non-CT .VOL files ──
print("\n--- Traffic Data Folders (ccs_data) ---")
ccs_folders = sorted([d for d in DATA_DIR.iterdir()
                       if d.is_dir() and "ccs_data" in d.name.lower()])

non_ct_traffic = 0
for folder in ccs_folders:
    for f in list(folder.rglob("*.VOL")):
        name = f.name.upper()
        if not name.startswith("CT_") and not name.startswith("CT "):
            size = f.stat().st_size
            f.unlink()
            non_ct_traffic += 1
            total_deleted += 1
            total_bytes_freed += size
    for f in list(folder.rglob("*.STA")):
        name = f.name.upper()
        if not name.startswith("CT_") and not name.startswith("CT "):
            size = f.stat().st_size
            f.unlink()
            non_ct_traffic += 1
            total_deleted += 1
            total_bytes_freed += size

if non_ct_traffic > 0:
    print(f"  Deleted {non_ct_traffic} non-CT traffic files from ccs_data folders")
else:
    print(f"  All {len(ccs_folders)} ccs_data folders already CT-only")

# ── 3. Remove empty subdirectories left behind ──
print("\n--- Cleaning Empty Directories ---")
empty_removed = 0
for dirpath, dirnames, filenames in os.walk(str(DATA_DIR), topdown=False):
    p = Path(dirpath)
    if p == DATA_DIR:
        continue
    if not any(p.iterdir()):
        p.rmdir()
        empty_removed += 1

if empty_removed:
    print(f"  Removed {empty_removed} empty directories")
else:
    print(f"  No empty directories found")

# ── 4. Summary ──
print(f"\n{'=' * 65}")
print(f"  TOTAL: {total_deleted} files deleted, "
      f"{total_bytes_freed / 1024 / 1024:.1f} MB freed")
print(f"{'=' * 65}")

# Show remaining size
total_size = sum(f.stat().st_size for f in DATA_DIR.rglob("*") if f.is_file())
file_count = sum(1 for f in DATA_DIR.rglob("*") if f.is_file())
print(f"\n  Remaining data: {file_count} files, {total_size / 1024 / 1024:.1f} MB")
print(f"  All CT-only. Ready for git!\n")
