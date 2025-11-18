# scripts/uvozi_csv_vus.py
import sys, csv, sqlite3, re, unicodedata

DB  = "VUS.db"
TBL = "slovar"

# --- konzola UTF-8 (Windows) ---
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# --- normalizacija ---
def strip_diacritics(s: str) -> str:
    if s is None:
        return ""
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")

def norm_geslo(s: str) -> str:
    # odstrani naglase, vezaje -> presledki, zlepi več presledkov, UPPER, trim
    s = strip_diacritics(s).replace("-", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s.upper()

def norm_opis(s: str) -> str:
    # obreži, odstrani zaključne . , ; in primerjaj case-insensitive
    s = (s or "").strip()
    s = s.strip(" .;,")
    return s.lower()

def exists_normalized(cur: sqlite3.Cursor, g: str, o: str) -> bool:
    gN = norm_geslo(g)
    oN = norm_opis(o)
    row = cur.execute(
        """
        SELECT 1
          FROM slovar
         WHERE REPLACE(UPPER(TRIM(geslo)),'-',' ') = ?
           AND lower(trim(trim(opis), '.,; ')) = ?
         LIMIT 1
        """,
        (gN, oN)
    ).fetchone()
    return row is not None

def main(csv_path: str):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    # tabela + (točen) unique index kot varovalka
    cur.execute(f"CREATE TABLE IF NOT EXISTS {TBL} (geslo TEXT NOT NULL, opis TEXT NOT NULL)")
    cur.execute(f"CREATE UNIQUE INDEX IF NOT EXISTS uniq_{TBL}_exact ON {TBL}(geslo, opis)")
    con.commit()

    added = skipped = 0

    # UTF-8 z BOM tolerantno
    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        rdr = csv.DictReader(f)
        # toleranca različnih glav
        for r in rdr:
            raw_g = r.get("GESLO_NORM") or r.get("GESLO") or r.get("geslo")
            raw_o = r.get("OPIS") or r.get("opis")
            if not raw_g or not raw_o:
                continue

            # če po normalizaciji že obstaja -> preskoči
            if exists_normalized(cur, raw_g, raw_o):
                skipped += 1
                continue

            # zapišemo *normalizirano* geslo, opis pustimo kot je (trim)
            g_save = norm_geslo(raw_g)
            o_save = (raw_o or "").strip()
            cur.execute(f"INSERT OR IGNORE INTO {TBL}(geslo, opis) VALUES (?,?)", (g_save, o_save))
            if cur.rowcount:
                added += 1
            else:
                skipped += 1

    con.commit()
    con.close()
    print(f"OK: vnešenih {added}, preskočenih {skipped}.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uporaba: python scripts/uvozi_csv_vus.py <pot_do_csv>")
        sys.exit(1)
    main(sys.argv[1])
