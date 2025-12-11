import sqlite3, os

db_path = r".\data\VUS.db"
print("Obstaja:", os.path.exists(db_path), db_path)

con = sqlite3.connect(db_path)
cur = con.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tabele:", cur.fetchall())

try:
    cur.execute("SELECT COUNT(*) FROM slovar;")
    print("Vrstic v slovar:", cur.fetchone()[0])
except Exception as e:
    print("Napaka pri branju 'slovar':", e)

con.close()
