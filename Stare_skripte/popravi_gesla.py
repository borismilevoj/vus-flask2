import sqlite3

conn = sqlite3.connect('VUS.db')
cur = conn.cursor()

# Zamenjaj vse ? z razmikom v stolpcih GESLO in OPIS
cur.execute("UPDATE slovar SET GESLO = REPLACE(GESLO, '?', ' ')")
cur.execute("UPDATE slovar SET OPIS = REPLACE(OPIS, '?', ' ')")

conn.commit()
conn.close()

print("Vsi znaki '?' so bili zamenjani z razmikom.")
