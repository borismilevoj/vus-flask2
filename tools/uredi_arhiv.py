# tools/uredi_arhiv.py
import re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "static" / "CrosswordCompilerApp"
DATE_RE = re.compile(r"^(20\d{2}-\d{2})-(\d{2})\.(js|xml)$")  # 2025-06-01.js

def main(dry_run=False):
    moved = 0
    for p in sorted(BASE.glob("*.*")):
        m = DATE_RE.match(p.name)
        if not m:
            continue
        ym = m.group(1)  # YYYY-MM
        target_dir = BASE / ym
        target_dir.mkdir(exist_ok=True)
        target = target_dir / p.name
        if target.exists():
            print(f"SKIP (že obstaja): {target}")
            continue
        print(f"MOVE: {p.relative_to(BASE)}  ->  {target.relative_to(BASE)}")
        if not dry_run:
            shutil.move(str(p), str(target))
        moved += 1
    print(f"OK. Premaknjenih datotek: {moved}")

if __name__ == "__main__":
    # python tools/uredi_arhiv.py --dry-run  (najprej test)
    dry = "--dry-run" in sys.argv
    main(dry_run=dry)
