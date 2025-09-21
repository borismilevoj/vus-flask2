import sqlite3
import unicodedata

DB_PATH = '../VUS.db'
NOVA_TABELA = 'slovar_sortiran'

def normalize_text(text):
    return unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8').lower()

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Drop and create new table
    cur.execute(f'DROP TABLE IF EXISTS {NOVA_TABELA}')
    cur.execute(f'''
        CREATE TABLE {NOVA_TABELA} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            geslo TEXT,
            opis TEXT
        )
    ''')

    # Pridobi vsa gesla
    cur.execute('SELECT DISTINCT geslo FROM slovar')
    gesla = [row[0] for row in cur.fetchall()]

    # Sortiraj gesla po normaliziranem imenu
    gesla_sorted = sorted(gesla, key=normalize_text)

    for geslo in gesla_sorted:
        # Pridobi vse opise za geslo
        cur.execute('SELECT opis FROM slovar WHERE geslo = ?', (geslo,))
        opisi = [row[0] for row in cur.fetchall()]
        # Sortiraj opise po normaliziranem besedilu
        opisi_sorted = sorted(opisi, key=normalize_text)
        # Vstavi sortirane v novo tabelo
        for opis in opisi_sorted:
            cur.execute(f'INSERT INTO {NOVA_TABELA} (geslo, opis) VALUES (?, ?)', (geslo, opis))

    conn.commit()
    print(f"Vsi podatki so shranjeni v tabelo '{NOVA_TABELA}' (v bazi {DB_PATH}).")
    conn.close()

if __name__ == "__main__":
    main()
