import sqlite3, os
p = r".\var\data\VUS.db"
print("DB:", os.path.abspath(p))
con = sqlite3.connect(p)
cur = con.cursor()

# shema slovar_sortiran
cols = [ (c[1], c[2]) for c in cur.execute("PRAGMA table_info(slovar_sortiran)").fetchall() ]
print("slovar_sortiran columns:", cols)

# koliko je zapisov skupaj
total = cur.execute("SELECT COUNT(*) FROM slovar_sortiran").fetchone()[0]
print("slovar_sortiran COUNT:", total)

# BRUNKOW v slovar_sortiran
n = cur.execute("SELECT COUNT(*) FROM slovar_sortiran WHERE TRIM(geslo)=? COLLATE NOCASE", ("BRUNKOW",)).fetchone()[0]
print("BRUNKOW v slovar_sortiran:", n)

# pokaži en primer KEATON, če obstaja
k = cur.execute("SELECT opis FROM slovar_sortiran WHERE TRIM(geslo)=? COLLATE NOCASE LIMIT 1", ("KEATON",)).fetchone()
if k: print("KEATON (sortiran) →", k[0])

con.close()
