import sqlite3, os
p = r".\var\data\VUS.db"
print("DB:", os.path.abspath(p))
con = sqlite3.connect(p)
cur = con.cursor()

# katere tabele obstajajo
tabs = [t[0] for t in cur.execute("SELECT name FROM sqlite_master WHERE type='table'")]
print("Tabele:", tabs)

# koliko zapisov v slovar
cnt = cur.execute("SELECT COUNT(*) FROM slovar").fetchone()[0] if "slovar" in tabs else 0
print("slovar COUNT:", cnt)

# preveri BRUNKOW in KEATON v 'slovar'
for w in ("BRUNKOW","KEATON"):
    n = cur.execute("SELECT COUNT(*) FROM slovar WHERE TRIM(geslo)=? COLLATE NOCASE", (w,)).fetchone()[0] if "slovar" in tabs else 0
    print(f"{w} v slovar:", n)
    if n:
        for (o,) in cur.execute("SELECT opis FROM slovar WHERE TRIM(geslo)=? COLLATE NOCASE LIMIT 1", (w,)):
            print(f"→ {w} opis:", o)

# pokaži morebitne FTS tabele (če admin išče prek njih)
fts = [t for t in tabs if "fts" in t.lower()]
print("FTS tabele:", fts)

con.close()
