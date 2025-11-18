import csv, sqlite3, sys, os

DB = "VUS.db"

def main(csv_path):
    if not os.path.exists(csv_path):
        print(f"CSV ne obstaja: {csv_path}")
        sys.exit(1)

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("CREATE INDEX IF NOT EXISTS idx_slovar_geslo_upper ON slovar(UPPER(GESLO))")

    added = 0
    skipped = 0

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        # pričakujemo stolpca GESLO in OPIS (kot generira tvoja skripta)
        # če so imena drugačna, prilagodi tu:
        field_geslo = "GESLO" if "GESLO" in reader.fieldnames else reader.fieldnames[-2]
        field_opis  = "OPIS"  if "OPIS"  in reader.fieldnames else reader.fieldnames[-1]

        for row in reader:
            geslo = row[field_geslo].strip()
            opis  = row[field_opis].strip()

            # podvojitve: ista kombinacija GESLO+OPIS?
            cur.execute("SELECT 1 FROM slovar WHERE UPPER(GESLO)=UPPER(?) AND OPIS=?", (geslo, opis))
            if cur.fetchone():
                skipped += 1
                continue

            cur.execute("INSERT INTO slovar (GESLO, OPIS) VALUES (?, ?)", (geslo, opis))
            added += 1

    conn.commit()
    conn.close()
    print(f"✔ Dodano: {added}, preskočeno (dvojnik): {skipped}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uporaba: python apply_csv_to_vus.py pot/do/datoteke.csv")
        sys.exit(1)
    main(sys.argv[1])
