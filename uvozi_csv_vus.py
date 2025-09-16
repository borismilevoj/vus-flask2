import csv, sqlite3, sys

DB = "VUS.db"
TBL = "slovar"

def main(csv_path):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS {TBL} (id INTEGER PRIMARY KEY AUTOINCREMENT, geslo TEXT, opis TEXT)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{TBL}_geslo ON {TBL}(geslo)")
    cur.execute(f"CREATE UNIQUE INDEX IF NOT EXISTS uniq_{TBL}_geslo_opis ON {TBL}(geslo, opis)")
    ins, skip = 0, 0
    with open(csv_path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            geslo = row["GESLO"].strip()
            opis = row["OPIS"].strip()
            try:
                cur.execute(f"INSERT INTO {TBL}(geslo, opis) VALUES (?,?)", (geslo, opis))
                ins += 1
            except sqlite3.IntegrityError:
                skip += 1
    con.commit()
    con.close()
    print(f"Vstavljeno: {ins}, preskočeno (duplikati): {skip}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uporaba: python uvozi_csv_vus.py <pot_do_csv>")
        sys.exit(1)
    main(sys.argv[1])
