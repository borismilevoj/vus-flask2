import sqlite3, os
p = r".\VUS.db"  # hard-link na var\data\VUS.db
con = sqlite3.connect(p)
cur = con.cursor()

print("DB:", os.path.abspath(p))
print("BRUNKOW:", cur.execute(
    "SELECT COUNT(*) FROM slovar_sortiran WHERE TRIM(geslo)=? COLLATE NOCASE", ("BRUNKOW",)
).fetchone()[0])

print("KEATON – vrstni red:")
for (o,) in cur.execute(
    "SELECT opis FROM slovar_sortiran WHERE TRIM(geslo)=? COLLATE NOCASE", ("KEATON",)
):
    print("→", o)

con.close()
