#!/usr/bin/env python3
import os, shutil, glob
from datetime import datetime

VAR_DATA = "/var/data"
DB_NAME  = "VUS.db"
DB_PATH  = os.path.join(VAR_DATA, DB_NAME)

def ensure_var_data():
    os.makedirs(VAR_DATA, exist_ok=True)

def sanitize_vus_db_url() -> str:
    """Odstrani \r/\n iz VUS_DB_URL in doda &dl=1, nato vrne očiščeni URL."""
    url = os.environ.get("VUS_DB_URL", "")
    if not url:
        print("prestart: VUS_DB_URL ni nastavljen.")
        return ""
    url = url.replace("\r", "").replace("\n", "").strip()
    if "dl=1" not in url:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}dl=1"
    os.environ["VUS_DB_URL"] = url
    print("prestart: VUS_DB_URL očiščen (ena vrstica, z dl=1).")
    return url

def maybe_copy_db_from_app_root():
    """Če /var/data/VUS.db še ne obstaja, poskusi kopirati iz projekta."""
    if os.path.exists(DB_PATH):
        return
    for c in ("VUS.db", "static/VUS.db", "data/VUS.db"):
        if os.path.exists(c):
            shutil.copy2(c, DB_PATH)
            print(f"prestart: kopiral {c} -> {DB_PATH}")
            return
    print("prestart: opozorilo: /var/data/VUS.db še ne obstaja in vira nisem našel.")

def daily_backup_and_prune(keep:int=2):
    """Naredi dnevni .bak in obdrži samo zadnja 'keep' backup-a."""
    if not os.path.exists(DB_PATH):
        return
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    bak = os.path.join(VAR_DATA, f"VUS_{stamp}.db.bak")
    try:
        shutil.copy2(DB_PATH, bak)
        print(f"prestart: backup -> {bak}")
    except Exception as e:
        print(f"prestart: backup ni uspel: {e}")
    baks = sorted(glob.glob(os.path.join(VAR_DATA, "VUS_*.db.bak")), key=os.path.getmtime, reverse=True)
    for old in baks[keep:]:
        try:
            os.remove(old)
            print(f"prestart: delete old backup {old}")
        except Exception as e:
            print(f"prestart: delete fail {old}: {e}")

if __name__ == "__main__":
    ensure_var_data()
    maybe_copy_db_from_app_root()
    sanitize_vus_db_url()  # <<< ključni del
    daily_backup_and_prune()
    print("prestart: OK")
