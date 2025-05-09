import sqlite3

conn = sqlite3.connect('VUS.db')
cur = conn.cursor()

with open("opisi_za_cc.txt", "w", encoding="utf-8") as f:
    for row in cur.execute("SELECT GESLO, OPIS FROM slovar"):
        geslo, opis = row
        f.write(f"{geslo};{opis}\n")

conn.close()
