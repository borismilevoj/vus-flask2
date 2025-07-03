import sqlite3

def zapolni_presledke_v_opisih():
    conn = sqlite3.connect('../VUS.db')
    cur = conn.cursor()

    # Preberi vse opise
    cur.execute("SELECT ID, OPIS FROM slovar")
    podatki = cur.fetchall()

    posodobljenih = 0

    for id_, opis in podatki:
        if ' ' in opis:
            novi_opis = opis.replace(' ', '_')
            cur.execute("UPDATE slovar SET OPIS = ? WHERE ID = ?", (novi_opis, id_))
            posodobljenih += 1

    conn.commit()
    conn.close()
    print(f"✅ Posodobljenih opisov: {posodobljenih}")

if __name__ == '__main__':
    zapolni_presledke_v_opisih()
