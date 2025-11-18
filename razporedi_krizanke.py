import re
import shutil
from pathlib import Path

# koren projekta (kjer je app.py)
ROOT = Path(__file__).resolve().parent
BASE = ROOT / "static" / "CrosswordCompilerApp"

# tu bomo iskali križanke:
SRC_DIRS = [
    BASE,                   # datoteke direkt v static/CrosswordCompilerApp
    BASE / "CrosswordImages"  # datoteke v CrosswordImages
]

def main():
    for src in SRC_DIRS:
        if not src.exists():
            continue

        print(f"\n[DIR] {src}")
        for path in sorted(src.glob("*.js")):
            name = path.name          # npr. 2025-11-14.js
            m = re.match(r"(\d{4}-\d{2})-\d{2}\.js$", name)
            if not m:
                print("  preskočim (ne poznam formata):", name)
                continue

            year_month = m.group(1)   # 2025-11
            month_dir = BASE / year_month
            month_dir.mkdir(parents=True, exist_ok=True)

            stem = path.stem  # 2025-11-14

            for ext in (".js", ".xml"):
                src_file = src / f"{stem}{ext}"
                if not src_file.exists():
                    continue
                dest_file = month_dir / src_file.name
                print("  MOVE", src_file, "->", dest_file)
                shutil.move(str(src_file), str(dest_file))

    print("\nOK – križanke so razporejene po mesečnih mapah.")

if __name__ == "__main__":
    main()
