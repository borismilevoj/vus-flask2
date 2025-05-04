import sqlite3

render_conn = sqlite3.connect('VUS.db')
render_cur = render_conn.cursor()

lokalna_conn = sqlite3.connect('VUS.db')
lokalna_cur = lokalna_conn.cursor()

zdruzena_conn = sqlite3.connect('VUS_zdruzena.db')
zdruzena_cur = zdruzena_conn.cursor()

zdruzena_cur.execute("""
CREATE TABLE slovar (
    GESLO TEXT NOT NULL,
    OPIS TEXT NOT NULL,
    PRIMARY KEY (GESLO, OPIS)
)
""")

render_cur.execute("SELECT GESLO, OPIS FROM slovar")
render_podatki = render_cur.fetchall()
zdruzena_cur.executemany("INSERT INTO slovar (GESLO, OPIS) VALUES (?, ?)", render_podatki)

lokalna_cur.execute("SELECT GESLO, OPIS FROM slovar")
lokalni_podatki = lokalna_cur.fetchall()

for geslo, opis in lokalni_podatki:
    if (geslo, opis) not in render_podatki:
        zdruzena_cur.execute("INSERT INTO slovar (GESLO, OPIS) VALUES (?, ?)", (geslo, opis))

zdruzena_conn.commit()

render_conn.close()
lokalna_conn.close()
zdruzena_conn.close()

print("✅ Bazi uspešno združeni v datoteko: VUS_zdruzena.db")
