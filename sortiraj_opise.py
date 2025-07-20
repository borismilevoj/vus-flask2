import sqlite3
import re

DB_PATH = 'VUS.db'
NOVA_TABELA = 'slovar_sortiran'

def key_za_sort(opis):
    m = re.search(r'-\s*([A-ZČŠŽ][^,]*)', opis)
    if m:
        return m.group(1).strip().lower()
    return ""

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Drop and create new table (with id)
    cur.execute(f'DROP TABLE IF EXISTS {NOVA_TABELA}')
    cur.execute(f'''
        CREATE TABLE {NOVA_TABELA} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            geslo TEXT,
            opis TEXT
        )
    ''')

    cur.execute('SELECT DISTINCT geslo FROM slovar')
    gesla = [row[0] for row in cur.fetchall()]

    for geslo in gesla:
        cur.execute('SELECT opis FROM slovar WHERE geslo = ?', (geslo,))
        opisi = [row[0] for row in cur.fetchall()]
        sortirani = [o for o in opisi if re.search(r'-\s*[A-ZČŠŽ]', o)]
        sortirani = sorted(sortirani, key=lambda o: key_za_sort(o) or "")
        nesortirani = [o for o in opisi if not re.search(r'-\s*[A-ZČŠŽ]', o)]
        for opis in sortirani + nesortirani:
            cur.execute(f'INSERT INTO {NOVA_TABELA} (geslo, opis) VALUES (?, ?)', (geslo, opis))

    conn.commit()
    print(f"Vsi podatki so shranjeni v tabelo '{NOVA_TABELA}' (v bazi {DB_PATH}).")
    conn.close()

if __name__ == "__main__":
    main()
