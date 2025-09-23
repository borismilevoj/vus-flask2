import sqlite3, pathlib
p = pathlib.Path(r"C:\Users\bormi\Documents\vus-flask2\VUS.db")
p.parent.mkdir(parents=True, exist_ok=True)
con = sqlite3.connect(str(p))
con.execute("CREATE TABLE IF NOT EXISTS slovar (id INTEGER PRIMARY KEY AUTOINCREMENT, geslo TEXT NOT NULL, opis TEXT)")
con.commit(); con.close()
print("OK – skelet baze ustvarjen:", p)
