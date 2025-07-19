import sqlite3
import re

DB_PATH = 'Stare_skripte/VUS-backup.db'
NOVA_TABELA = 'slovar_sortiran'


def key_za_sort(opis):
    # Išče Ime/priimek za vezajem (npr. "– Iris" => "Iris")
    m = re.search(r'-\s*([A-ZČŠŽ][^,]*)', opis)
    if m:
        return m.group(1).strip().lower()
    return None

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Pripravimo novo tabelo (če želiš, izbriši staro najprej)
    cur.execute(f'''
        DROP TABLE IF EXISTS {NOVA_TABELA}
    ''')
    cur.execute(f'''
        CREATE TABLE {NOVA_TABELA} (
            geslo TEXT,
            opis TEXT
        )
    ''')

    # Vse unikatne gesle
    cur.execute('SELECT DISTINCT geslo FROM slovar')
    gesla = [row[0] for row in cur.fetchall()]

    for geslo in gesla:
        cur.execute('SELECT opis FROM slovar WHERE geslo = ?', (geslo,))
        opisi = [row[0] for row in cur.fetchall()]
        if geslo == 'BERGMAN':
            print(f"BERGMAN - št. opisov: {len(opisi)}")
            for opis in opisi:
                print(repr(opis))
        # ... dalje kot prej ...

        # sortirani (po imenu za vezajem)
        sortirani = [o for o in opisi if re.search(r'-\s*[A-ZČŠŽ]', o)]
        sortirani = sorted(sortirani, key=lambda o: key_za_sort(o) or "")

        # nesortirani (vsi ostali)
        nesortirani = [o for o in opisi if not re.search(r'-\s*[A-ZČŠŽ]', o)]

        # Shrani v novo tabelo v pravem vrstnem redu
        for opis in sortirani + nesortirani:
            cur.execute(f'INSERT INTO {NOVA_TABELA} (geslo, opis) VALUES (?, ?)', (geslo, opis))

    conn.commit()
    print(f"Vsi podatki so shranjeni v tabelo '{NOVA_TABELA}' (v bazi {DB_PATH}).")
    conn.close()

if __name__ == "__main__":
    main()
