import sqlite3

conn = sqlite3.connect('../VUS.db')
cursor = conn.cursor()

with open('../VUS_izvoz_iz_cc.txt', encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) >= 2:
            geslo = parts[0].strip()
            opis = parts[1].strip().strip('"')
            if geslo and opis:
                cursor.execute(
                    "INSERT INTO slovar (geslo, opis) VALUES (?, ?)",
                    (geslo, opis)
                )

conn.commit()
conn.close()
print("Uvoz končan.")
