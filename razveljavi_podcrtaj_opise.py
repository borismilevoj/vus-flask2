import sqlite3

def razveljavi_podcrtaj_opise():
    conn = sqlite3.connect('VUS.db')
    cur = conn.cursor()

    cur.execute("SELECT ID, OPIS FROM slovar")
    podatki = cur.fetchall()

    razveljavljenih = 0

    for id_, opis in podatki:
        if '_' in opis:
            popravljeno = opis.replace('_', ' ')
            cur.execute("UPDATE slovar SET OPIS = ? WHERE ID = ?", (popravljeno, id_))
            razveljavljenih += 1

    conn.commit()
    conn.close()
    print(f"🔁 Razveljavljenih opisov: {razveljavljenih}")

if __name__ == '__main__':
    razveljavi_podcrtaj_opise()
