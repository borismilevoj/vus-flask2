import os, sqlite3, pathlib, sys
DB = os.environ.get("DB_PATH", "../var/data/VUS.db")
p = pathlib.Path(DB)
print("DB_PATH =", p.resolve())
if not p.exists():
    print("❌ Datoteka NE obstaja."); sys.exit(0)
print("Velikost:", p.stat().st_size, "bytes")
con = sqlite3.connect(str(p))
rows = con.execute("SELECT name, type FROM sqlite_master WHERE type IN ('table','view') ORDER BY name").fetchall()
print("Tabele/Views:", rows)
con.close()
