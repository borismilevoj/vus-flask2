import csv, sqlite3, os, sys

CSV = os.path.expandvars(r"%OneDrive%\Desktop\cc_clues_DISPLAY_UTF8.csv")
DB  = r".\var\data\VUS.db"
WORD = "KEATON"   # <- po potrebi zamenjaj ali zaženi veèkrat

def sniff_delim(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        head = f.read(4096); f.seek(0)
        return ';' if head.count(';')>head.count(',') else ','

def norm(s): return ("".join(str(s).split())).replace("\u00A0"," ").strip() if s is not None else ""

if not os.path.exists(CSV): 
    print("? CSV ne obstaja:", CSV); sys.exit(1)
if not os.path.exists(DB):
    print("? DB ne obstaja:", DB); sys.exit(1)

delim = sniff_delim(CSV)
rows = []
with open(CSV, "r", encoding="utf-8-sig", newline="") as f:
    R = csv.reader(f, delimiter=delim)
    first = next(R, None)
    # ali ima glavo?
    lower = [ (c or "").strip().lower() for c in (first or []) ]
    looks_header = any(x in lower for x in ("word","geslo","answer","entry")) or any(x in lower for x in ("clue","opis","definition","hint"))
    if not looks_header and first:
        rows.append(first)
    rows.extend(R)

# Privzem: stolpca sta 0=Word, 1=Clue; èe je glava, poišèemo indekse
w_idx, c_idx = 0, 1
if looks_header:
    try:
        w_idx = lower.index("word") if "word" in lower else lower.index("geslo")
    except ValueError: pass
    try:
        c_idx = lower.index("clue") if "clue" in lower else lower.index("opis")
    except ValueError: pass

word = WORD.strip()
clues_new = []
for r in rows:
    if not r: continue
    w = (r[w_idx] if len(r)>w_idx else "").strip()
    c = (r[c_idx] if len(r)>c_idx else "").strip()
    if not w or not c: continue
    if w.strip().lower() == word.lower():
        clues_new.append(c)

if not clues_new:
    print(f"??  V CSV ni najdenih vrstic za '{WORD}'."); sys.exit(0)

con = sqlite3.connect(DB)
cur = con.cursor()
print("DB:", os.path.abspath(DB))
print(f"Geslo: {WORD}")
print(f"Najdenih opisov v CSV: {len(clues_new)}")

cur.execute("BEGIN")
# 1) pobriši vse stare zapise za geslo v obeh tabelah
cur.execute("DELETE FROM slovar WHERE TRIM(geslo)=TRIM(?) COLLATE NOCASE", (word,))
cur.execute("DELETE FROM slovar_sortiran WHERE TRIM(geslo)=TRIM(?) COLLATE NOCASE", (word,))
# 2) vstavi nove opise
ins = 0
for c in clues_new:
    try:
        cur.execute("INSERT OR IGNORE INTO slovar(geslo, opis) VALUES (?,?)", (word, c))
        cur.execute("INSERT OR IGNORE INTO slovar_sortiran(geslo, opis) VALUES (?,?)", (word, c))
        ins += 1
    except sqlite3.IntegrityError:
        pass
cur.execute("COMMIT")

# preveri
n1 = cur.execute("SELECT COUNT(*) FROM slovar WHERE TRIM(geslo)=TRIM(?) COLLATE NOCASE", (word,)).fetchone()[0]
n2 = cur.execute("SELECT COUNT(*) FROM slovar_sortiran WHERE TRIM(geslo)=TRIM(?) COLLATE NOCASE", (word,)).fetchone()[0]
print(f"? Konèano. V slovar: {n1}, v slovar_sortiran: {n2}")
for (o,) in cur.execute("SELECT opis FROM slovar_sortiran WHERE TRIM(geslo)=TRIM(?) COLLATE NOCASE", (word,)):
    print("›", o)
con.close()
