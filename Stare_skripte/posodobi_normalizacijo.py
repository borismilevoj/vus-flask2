import sqlite3
from pretvornik import normaliziraj_geslo

conn = sqlite3.connect('VUS.db')
cur = conn.cursor()

# posodobitev NORMALIZIRAN_OPIS
cur.execute("SELECT ID, OPIS FROM slovar")
for id, opis in cur.fetchall():
    normaliziran_opis = normaliziraj_geslo(opis).upper()
    cur.execute("UPDATE slovar SET NORMALIZIRAN_OPIS = ? WHERE ID = ?", (normaliziran_opis, id))

conn.commit()
conn.close()

print("Normalizacija je bila uspešno izvedena.")
