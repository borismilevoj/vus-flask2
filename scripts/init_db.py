import sqlite3

conn = sqlite3.connect('../Stare_skripte/VUS.db')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS slovar (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    GESLO TEXT NOT NULL,
    OPIS TEXT NOT NULL
)
''')

conn.commit()
conn.close()

print("Tabela 'slovar' ustvarjena.")
