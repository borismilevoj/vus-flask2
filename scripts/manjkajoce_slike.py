import sqlite3
import os
import unicodedata
import re

def normaliziraj_naziv(ime):
    ime = unicodedata.normalize('NFD', ime).encode('ascii', 'ignore').decode('utf-8')
    ime = ime.lower()
    ime = ime.replace('-', ' ').replace('(', '').replace(')', '').replace(':', '').replace('.', '')
    besede = re.findall(r'\w+', ime)
    return '_'.join(besede[:8])[:64]

def preveri_manjkajoci(ime_baze, mapa_slik):
    conn = sqlite3.connect(ime_baze)
    cur = conn.cursor()
    cur.execute("SELECT opis FROM slovar")
    opisi = [row[0] for row in cur.fetchall()]
    conn.close()

    manjkajoce = []

    for opis in opisi:
        ime_slike = f"{normaliziraj_naziv(opis)}.jpg"
        pot = os.path.join(mapa_slik, ime_slike)
        if not os.path.exists(pot):
            manjkajoce.append((opis, ime_slike))

    print(f"\n📂 Manjkajoče slike ({len(manjkajoce)}):\n")
    for opis, ime in manjkajoce[:50]:
        print(f"❌ {opis} → {ime}")
    if len(manjkajoce) > 50:
        print(f"... in še {len(manjkajoce) - 50} drugih")

    # Zapis v datoteko
    with open("../Stare_skripte/manjkajoce_slike.txt", "w", encoding="utf-8") as f:
        f.write(f"Manjkajoče slike ({len(manjkajoce)}):\n\n")
        for opis, ime in manjkajoce:
            f.write(f"{opis} → {ime}\n")

    print("\n✅ Shranjeno v 'manjkajoce_slike.txt'")

if __name__ == '__main__':
    preveri_manjkajoci('VUS.db', os.path.join('../static', 'Images'))
