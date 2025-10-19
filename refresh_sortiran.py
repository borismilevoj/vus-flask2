import sqlite3
p = r".\var\data\VUS.db"
con = sqlite3.connect(p)
cur = con.cursor()
cur.execute("BEGIN")
cur.execute("DELETE FROM slovar_sortiran")
cur.execute("INSERT OR IGNORE INTO slovar_sortiran(geslo, opis) SELECT geslo, opis FROM slovar")
cur.execute("COMMIT")
# preveri
b = cur.execute("SELECT COUNT(*) FROM slovar_sortiran WHERE TRIM(geslo)=? COLLATE NOCASE", ("BRUNKOW",)).fetchone()[0]
k = cur.execute("SELECT opis FROM slovar_sortiran WHERE TRIM(geslo)=? COLLATE NOCASE LIMIT 1", ("KEATON",)).fetchone()
print("BRUNKOW v slovar_sortiran:", b)
print("KEATON (sortiran) →", k[0] if k else "—")
con.close()
