"""
Clean up the station data directory structure.
================================================
Current mess:
  data/Station/               <- 51 loose 2025 .STA files (duplicate)
  data/2025_station_data/Station/  <- same 51 files, nested one level too deep
  data/Station_Data_Extract_Pipe_Delimited_CleanData_2021.txt  <- loose duplicate

After cleanup:
  data/2025_station_data/     <- flat .STA files (matching 2022-2024 pattern)
  data/Station/               <- DELETED (duplicate)
  loose 2021 .txt             <- DELETED (already in 2021_station_data/)
  Notebook 1 updated to point to new path
"""

import sys
import shutil
import json
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_DIR = Path(r"C:\Users\owner\Downloads\Masters\Masters_Spring_2026"
                   r"\Advanced Deep Learning\Traffic Project 2")
DATA_DIR = PROJECT_DIR / "data"

print("=" * 65)
print("  Station Data Cleanup")
print("=" * 65)

# ── 1. Fix 2025_station_data: flatten the nested Station/ subfolder ──
nested = DATA_DIR / "2025_station_data" / "Station"
target = DATA_DIR / "2025_station_data"

if nested.is_dir():
    files_moved = 0
    for f in sorted(nested.iterdir()):
        if f.is_file():
            dest = target / f.name
            if not dest.exists():
                shutil.move(str(f), str(dest))
                files_moved += 1
            else:
                # Already exists at target level — just remove the nested copy
                f.unlink()
                files_moved += 1
    # Remove the now-empty Station/ subfolder
    if nested.exists():
        shutil.rmtree(nested)
    print(f"\n  [OK] Flattened 2025_station_data/Station/ → moved {files_moved} files up")
    print(f"       Deleted empty nested Station/ subfolder")
else:
    print(f"\n  [SKIP] No nested Station/ folder in 2025_station_data/")

# ── 2. Delete the duplicate data/Station/ folder ──
dup_station = DATA_DIR / "Station"
if dup_station.is_dir():
    count = sum(1 for _ in dup_station.iterdir())
    shutil.rmtree(dup_station)
    print(f"\n  [DEL] Removed data/Station/ ({count} duplicate 2025 .STA files)")
else:
    print(f"\n  [SKIP] data/Station/ does not exist")

# ── 3. Delete the loose 2021 .txt file from data/ root ──
loose_2021 = DATA_DIR / "Station_Data_Extract_Pipe_Delimited_CleanData_2021.txt"
if loose_2021.is_file():
    # Verify the copy inside 2021_station_data exists first
    inside = DATA_DIR / "2021_station_data" / "Station_Data_Extract_Pipe_Delimited_CleanData_2021.txt"
    if inside.is_file():
        loose_2021.unlink()
        print(f"\n  [DEL] Removed loose Station_Data_Extract_..._2021.txt from data/ root")
        print(f"        (confirmed copy exists in 2021_station_data/)")
    else:
        # Move it instead of deleting
        shutil.move(str(loose_2021), str(inside))
        print(f"\n  [MOVE] Moved loose 2021 .txt → 2021_station_data/")
else:
    print(f"\n  [SKIP] No loose 2021 .txt in data/ root")

# ── 4. Update Notebook 1 station path to match new structure ──
nb_path = PROJECT_DIR / "01_Data_Pipeline.ipynb"
with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

updated = False
for cell in nb["cells"]:
    if cell.get("cell_type") != "code":
        continue
    src = cell["source"]
    new_src = []
    for line in src:
        # Old primary: DATA_DIR / "Station" / "CT_2025 (TMAS).STA"
        # New primary: DATA_DIR / "2025_station_data" / "CT_2025 (TMAS).STA"
        if '"Station" / "CT_2025 (TMAS).STA"' in line:
            line = line.replace('"Station"', '"2025_station_data"')
            updated = True
        new_src.append(line)
    cell["source"] = new_src

if updated:
    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1)
    print(f"\n  [OK] Updated 01_Data_Pipeline.ipynb:")
    print(f'       Primary path: DATA_DIR / "2025_station_data" / "CT_2025 (TMAS).STA"')
    print(f'       Fallback:     DATA_DIR / "2024_station_data" / "CT_2024 (TMAS).STA"')
else:
    print(f"\n  [SKIP] Notebook already uses correct paths")

# ── 5. Summary ──
print(f"\n{'=' * 65}")
print("  Final station data structure:")
print("=" * 65)
for item in sorted(DATA_DIR.iterdir()):
    name = item.name
    if "station" in name.lower():
        if item.is_dir():
            contents = list(item.iterdir())
            ct_files = [f for f in contents if f.name.startswith("CT_")]
            print(f"  [DIR]  {name}/  ({len(contents)} files, CT: {[f.name for f in ct_files]})")
        else:
            print(f"  [FILE] {name}  ← SHOULD NOT BE HERE")

print(f"\n  Done! All station data organized by year.\n")
