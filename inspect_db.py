import sys, os, sqlite3
db = sys.argv[1] if len(sys.argv) > 1 else "VUS.db"
print("DB:", os.path.abspath(db))
con = sqlite3.connect(db)
cur = con.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [t[0] for t in cur.fetchall()]
print("Tabele:", tables)
for t in tables:
    try:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        n = cur.fetchone()[0]
        print(f"{t:25s} -> {n} vrstic")
    except Exception as e:
        print(f"{t:25s} -> napaka: {e}")
con.close()
