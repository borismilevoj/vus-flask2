import sqlite3
import re

conn = sqlite3.connect('VUS.db')
cur = conn.cursor()

# Poišči vse zapise, kjer so datumi ločeni z 'šč' namesto '†'
cur.execute("SELECT rowid, OPIS FROM slovar WHERE OPIS LIKE '%šč%'")
zapisi = cur.fetchall()

popravljeno_skupaj = 0

# Zamenjava vzorca: "(xxxxščxxxx)" v "(xxxx†xxxx)"
pattern = re.compile(r'(\d{4})šč(\d{4})')

for rowid, opis in zapisi:
    if pattern.search(opis):
        nov_opis = pattern.sub(r'\1†\2', opis)
        cur.execute("UPDATE slovar SET OPIS = ? WHERE rowid = ?", (nov_opis, rowid))
        popravljeno_skupaj += 1

print(f"Skupaj popravljenih zapisov: {popravljeno_skupaj}")
conn.commit()
conn.close()
