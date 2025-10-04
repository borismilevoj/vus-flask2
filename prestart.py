# prestart.py — potegne VUS.db pred zagonom aplikacije
import os, sqlite3, tempfile, shutil, urllib.request, pathlib, time, sys

# URL iz okolja ali fallback (spremeni po potrebi)
URL = os.getenv("VUS_DB_URL") or \
      "https://dl.dropboxusercontent.com/scl/fi/m89w7wllcjhlrz8gbjvn7/VUS.db?rlkey=4gqo3mwjaqa1yin8ksww0uk6l"

dest = pathlib.Path("/var/data/VUS.db")
dest.parent.mkdir(parents=True, exist_ok=True)

fd, tmp_path = tempfile.mkstemp(dir=str(dest.parent), prefix="VUS_", suffix=".tmp")
os.close(fd)

print(f"[prestart] prenos: {URL}")
urllib.request.urlretrieve(URL, tmp_path)

# preveri integriteto + preštej vrstice
con = sqlite3.connect(tmp_path)
ok  = con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
rows = con.execute("SELECT COUNT(*) FROM slovar").fetchone()[0]
con.close()
if not ok:
    print("[prestart] integrity_check FAILED", file=sys.stderr); sys.exit(1)

# varnostna kopija stare datoteke
ts = time.strftime("%Y%m%d-%H%M%S")
if dest.exists():
    bak = dest.with_name(f"VUS_{ts}.db.bak")
    shutil.copy2(dest, bak)
    print(f"[prestart] backup: {bak}")

# zamenjaj
shutil.move(tmp_path, dest)
print(f"[prestart] posodobljeno: {dest} (rows={rows})")
