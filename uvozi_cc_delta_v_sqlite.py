import sqlite3, csv, sys, os, re

CSV_PATH = r".\out\cc_delta.csv"
DB_PATH  = r".\VUS.db"
TABLE    = "cc_clues"

def clean(s: str) -> str:
    if s is None: return ""
    # odstrani BOM, NBSP, zunanje dvojne/enojnje narekovaje, whitespace
    s = s.replace("\ufeff","").replace("\xa0"," ")
    s = s.strip().strip('"').strip("'").strip()
    return s

def norm_name(s: str) -> str:
    # normaliziraj ime stolpca za primerjavo
    return clean(s).lower()

if not os.path.exists(CSV_PATH):
    print(f"CSV ne obstaja: {CSV_PATH}"); sys.exit(1)

# zaznaj delimiter + glavo
with open(CSV_PATH, "r", encoding="utf-8", newline="") as f:
    sample = f.read(4096); f.seek(0)
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;|\t")
        delim = dialect.delimiter
    except Exception:
        delim = ","
    reader = csv.reader(f, delimiter=delim)
    raw_header = next(reader, [])
    header = [clean(h) for h in raw_header]
print(f"Zaznan delimiter: '{delim}'")
print("Glava (očiščeno):", header)

# zgradi mapo: normirano ime -> originalno ime
norm2orig = { norm_name(h): h for h in header }

# podprta imena (case-insensitive, očiščena)
word_key_opts = ["word","geslo"]
clue_key_opts = ["clue","opis"]
date_key_opts = ["date","datum"]
cit_key_opts  = ["citation","cit","vir"]

def pick(keys):
    for k in keys:
        if k in norm2orig: return norm2orig[k]
    return None

word_col = pick(word_key_opts)
clue_col = pick(clue_key_opts)
date_col = pick(date_key_opts) or "Date"
cit_col  = pick(cit_key_opts)  or "Citation"

if not word_col or not clue_col:
    print("Ne najdem obveznih stolpcev (Word/GESLO in Clue/OPIS). Najdene:", header)
    sys.exit(1)

# DB setup
con = sqlite3.connect(DB_PATH)
con.execute("PRAGMA journal_mode=WAL;")
con.execute("PRAGMA synchronous=NORMAL;")
con.execute(f"""
CREATE TABLE IF NOT EXISTS {TABLE}(
  Word     TEXT NOT NULL PRIMARY KEY,
  Clue     TEXT NOT NULL,
  Date     TEXT,
  Citation TEXT
);
""")
upsert_sql = f"""
INSERT INTO {TABLE}(Word,Clue,Date,Citation)
VALUES (?,?,?,?)
ON CONFLICT(Word) DO UPDATE SET
  Clue=excluded.Clue,
  Date=excluded.Date,
  Citation=excluded.Citation;
"""

rows, skipped = 0, 0
reasons = {}

with open(CSV_PATH, "r", encoding="utf-8", newline="") as f:
    rdr = csv.DictReader(f, delimiter=delim)
    # očisti imena polj v DictReaderju
    rdr.fieldnames = [clean(x) for x in rdr.fieldnames]
    for r in rdr:
        word = clean(r.get(word_col))
        clue = clean(r.get(clue_col))
        date = clean(r.get(date_col)) if date_col in r else ""
        cit  = clean(r.get(cit_col))  if cit_col  in r else ""
        if not word or not clue:
            skipped += 1
            reasons["prazen word/clue"] = reasons.get("prazen word/clue", 0) + 1
            continue
        con.execute(upsert_sql, (word, clue, date, cit))
        rows += 1

con.commit()
total = con.execute(f"SELECT COUNT(*) FROM {TABLE}").fetchone()[0]
sample = con.execute(f"SELECT Word, substr(Clue,1,60) FROM {TABLE} WHERE Word IN ('TANIN','DEVADZE') ORDER BY Word").fetchall()
con.close()

print(f"Uvoženih/posodobljenih iz delte: {rows}")
print(f"Skupaj v {TABLE}: {total}")
if skipped: print(f"Preskočenih: {skipped} | razlogi: {reasons}")
print("Vzorčni (TANIN/DEVADZE, če obstajata):", sample)
