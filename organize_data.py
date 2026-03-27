"""
Traffic Project 2 - Data Organizer
===================================
1. Unzips every .zip file into a folder named after the zip.
2. Verifies the extracted folder exists.
3. Deletes the original .zip after successful extraction.
4. Cleans up any loose .VOL/.STA files left in the root.
5. Moves all data folders into the `data/` subfolder.
6. Reports which months between 2011-2025 are present and which are missing.
"""

import os
import sys
import zipfile
import shutil
from pathlib import Path

# Force UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# -- Configuration ----------------------------------------------------------
PROJECT_DIR = Path(r"C:\Users\owner\Downloads\Masters\Masters_Spring_2026"
                   r"\Advanced Deep Learning\Traffic Project 2")
DATA_DIR = PROJECT_DIR / "data"

MONTH_ABBR = [
    "jan", "feb", "mar", "apr", "may", "jun",
    "jul", "aug", "sep", "oct", "nov", "dec",
]
MONTH_FULL = [
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december",
]
ABBR_TO_NUM = {m: i + 1 for i, m in enumerate(MONTH_ABBR)}
FULL_TO_NUM = {m: i + 1 for i, m in enumerate(MONTH_FULL)}


# -- Step 1-3: Unzip into named folders, verify, delete ---------------------
def unzip_all(directory: Path) -> None:
    zip_files = sorted(directory.glob("*.zip"))
    if not zip_files:
        print("[OK] No .zip files found -- nothing to extract.\n")
        return

    print(f"Found {len(zip_files)} zip file(s) to extract:\n")
    for zf in zip_files:
        print(f"  Extracting: {zf.name}")
        target_folder = directory / zf.stem
        try:
            # Always extract into a folder named after the zip
            target_folder.mkdir(exist_ok=True)
            with zipfile.ZipFile(zf, "r") as z:
                z.extractall(target_folder)

            if target_folder.is_dir() and any(target_folder.iterdir()):
                print(f"    [OK] Extracted into folder: {target_folder.name}/")
            else:
                print(f"    [WARN] Folder {target_folder.name}/ appears empty")
                continue

            # Delete the original zip
            zf.unlink()
            print(f"    [DEL] Deleted: {zf.name}")

        except zipfile.BadZipFile:
            print(f"    [ERR] {zf.name} is not a valid zip file -- skipped.")
        except Exception as e:
            print(f"    [ERR] Extracting {zf.name}: {e}")

    print()


# -- Step 4: Clean up loose .VOL and .STA files from prior bad extract ------
def cleanup_loose_files(directory: Path) -> None:
    """Remove .VOL and .STA files that were extracted loose into the root."""
    extensions = {".vol", ".sta"}
    loose_files = [f for f in directory.iterdir()
                   if f.is_file() and f.suffix.lower() in extensions]

    if not loose_files:
        print("  [OK] No loose .VOL/.STA files in root.\n")
        return

    print(f"  Cleaning up {len(loose_files)} loose .VOL/.STA files from root...")
    for f in loose_files:
        f.unlink()
    print(f"  [DEL] Removed {len(loose_files)} loose files.\n")


# -- Step 5: Move all data folders into data/ -------------------------------
def is_data_folder(name: str) -> bool:
    """Return True if the folder name looks like a monthly/yearly data folder."""
    name_lower = name.lower()
    for prefix in MONTH_ABBR + MONTH_FULL:
        if name_lower.startswith(prefix + "_"):
            return True
    if len(name_lower) >= 4 and name_lower[:4].isdigit() and "station_data" in name_lower:
        return True
    return False


def move_folders_to_data(project_dir: Path, data_dir: Path) -> None:
    data_dir.mkdir(exist_ok=True)

    items = sorted(project_dir.iterdir())
    moved = 0
    for item in items:
        if not item.is_dir():
            continue
        if item == data_dir:
            continue
        if not is_data_folder(item.name):
            continue

        dest = data_dir / item.name
        if dest.exists():
            print(f"  [SKIP] Already in data/: {item.name}")
            shutil.rmtree(item)
            print(f"    [DEL] Removed duplicate from root")
            moved += 1
            continue

        shutil.move(str(item), str(dest))
        print(f"  [MOVE] {item.name} -> data/{item.name}")
        moved += 1

    if moved == 0:
        print("  [OK] No folders to move -- all data already in data/.")
    else:
        print(f"\n  [OK] Processed {moved} folder(s).")
    print()


# -- Step 6: Validate all months 2011-2025 are present ---------------------
def parse_month_year(folder_name: str):
    """Extract (year, month_num) from a folder name. Returns None on failure."""
    name = folder_name.lower()
    for abbr, num in ABBR_TO_NUM.items():
        if name.startswith(abbr + "_"):
            rest = name[len(abbr) + 1:]
            year_str = rest[:4]
            if year_str.isdigit():
                return (int(year_str), num)
    for full, num in FULL_TO_NUM.items():
        if name.startswith(full + "_"):
            rest = name[len(full) + 1:]
            year_str = rest[:4]
            if year_str.isdigit():
                return (int(year_str), num)
    return None


def check_coverage(data_dir: Path) -> None:
    present = set()
    for item in data_dir.iterdir():
        if item.is_dir():
            result = parse_month_year(item.name)
            if result:
                present.add(result)

    all_months = {(y, m) for y in range(2011, 2026) for m in range(1, 13)}
    missing = sorted(all_months - present)
    found = sorted(all_months & present)

    print(f"  Coverage: {len(found)} / {len(all_months)} months present")
    print(f"  Missing:  {len(missing)} month(s)\n")

    if missing:
        print("  Missing months:")
        current_year = None
        for year, month in missing:
            if year != current_year:
                current_year = year
                print(f"\n    {year}:", end="")
            print(f"  {MONTH_ABBR[month - 1].capitalize()}", end="")
        print("\n")
    else:
        print("  ALL months from Jan 2011 - Dec 2025 are present!\n")


# -- Main ------------------------------------------------------------------
def main():
    print("=" * 65)
    print("  Traffic Project 2 - Data Organizer")
    print("=" * 65)
    print(f"\n  Working directory: {PROJECT_DIR}\n")

    print("-" * 65)
    print("  STEP 1-3: Unzip -> Verify -> Delete originals")
    print("-" * 65)
    unzip_all(PROJECT_DIR)

    print("-" * 65)
    print("  STEP 4: Clean up loose files from prior extraction")
    print("-" * 65)
    cleanup_loose_files(PROJECT_DIR)

    print("-" * 65)
    print("  STEP 5: Move all data folders into data/")
    print("-" * 65)
    move_folders_to_data(PROJECT_DIR, DATA_DIR)

    print("-" * 65)
    print("  STEP 6: Validate month coverage (2011-2025)")
    print("-" * 65)
    check_coverage(DATA_DIR)

    # Quick summary of what's left in root
    print("-" * 65)
    print("  Remaining items in project root:")
    print("-" * 65)
    for item in sorted(PROJECT_DIR.iterdir()):
        if item == DATA_DIR:
            print(f"  [DIR]  {item.name}/  (all data inside)")
        elif item.is_dir():
            print(f"  [DIR]  {item.name}/")
        else:
            print(f"  [FILE] {item.name}")


if __name__ == "__main__":
    main()
