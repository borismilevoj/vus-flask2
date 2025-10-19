import sqlite3, os
p = r".\var\data\VUS.db"   # <- UI-jeva baza
w = "BRUNKOW"
print("DB:", os.path.abspath(p))
con = sqlite3.connect(p)
rows = con.execute("SELECT opis FROM slovar WHERE TRIM(geslo)=? COLLATE NOCASE", (w,)).fetchall()
print("Najdeno:", len(rows))
for (o,) in rows[:5]:
    print("→", o)
con.close()
