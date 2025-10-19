import csv, os, sqlite3, sys, glob, argparse
from pathlib import Path
from datetime import datetime

# ------------------ Nastavitve ------------------
DB_PATH = os.environ.get("DB_PATH", "VUS.db")

CANDIDATE_PATTERNS = [
    "cc_clues_DISPLAY_UTF8*.csv",
    "cc_clues*.csv",
]

# mapiranje možnih glav (angleško/slovensko)
COL_ALIASES = {
    "word": {"word", "geslo", "gesla"},
    "clue": {"clue", "opis", "opisi"},
    "date": {"date", "datum"},
    "citation": {"citation", "cit", "vir"},
}
REQUIRED = {"word", "clue"}
# ------------------------------------------------

def norm(s): return (s or "").strip()

def detect_delimiter(sample_text: str, fallback=","):
    try:
        dialect = csv.Sniffer().sniff(sample_text)
        return dialect.delimiter
    except Exception:
        return ";" if ";" in sample_text and "," not in sample_text else fallback

def looks_like_header(first_row):
    tokens = [norm(x).lower() for x in first_row]
    return any(t in COL_ALIASES["word"] for t in tokens) or any(t in COL_ALIASES["clue"] for t in tokens)

def map_header(raw_headers):
    idx = {}
    for i, h in enumerate(raw_headers):
        h_clean = norm(h).lower()
        for canon, aliases in COL_ALIASES.items():
            if h_clean in aliases:
                idx[canon] = i
    return idx

def open_csv_rows(path: Path):
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        sample = f.read(4096)
        f.seek(0)
        delim = detect_delimiter(sample)
        reader = csv.reader(f, delimiter=delim)
        rows = list(reader)
    return rows, delim

# ---------- ODKRIVANJE SHEME V BAZI -------------
def get_tables(conn):
    cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    return [r[0] for r in cur.fetchall()]

def get_columns(conn, table):
    cur = conn.execute(f"PRAGMA table_info({table})")
    return [r[1] for r in cur.fetchall()]

def detect_table_and_columns(conn):
    aliases_word = COL_ALIASES["word"]
    aliases_clue = COL_ALIASES["clue"]

    candidates = get_tables(conn)
    if "slovar" in candidates:
        cols = get_columns(conn, "slovar")
        low = {c.lower(): c for c in cols}
        word_col = next((low[a] for a in aliases_word if a in low), None)
        clue_col = next((low[a] for a in aliases_clue if a in low), None)
        if word_col and clue_col:
            return "slovar", word_col, clue_col

    for t in candidates:
        cols = get_columns(conn, t)
        low = {c.lower(): c for c in cols}
        word_col = next((low[a] for a in aliases_word if a in low), None)
        clue_col = next((low[a] for a in aliases_clue if a in low), None)
        if word_col and clue_col:
            return t, word_col, clue_col

    conn.execute("""
        CREATE TABLE IF NOT EXISTS slovar (
            geslo TEXT,
            opis  TEXT,
            UNIQUE(geslo, opis)
        )
    """)
    conn.commit()
    return "slovar", "geslo", "opis"

# --------- Operacije nad bazo -------------------
def insert_pair(conn, table, col_word, col_clue, geslo, opis):
    conn.execute(
        f"INSERT OR IGNORE INTO {table} ({col_word}, {col_clue}) VALUES (?, ?)",
        (geslo, opis),
    )

def delete_by_word(conn, table, col_word, geslo):
    conn.execute(f"DELETE FROM {table} WHERE {col_word}=?", (geslo,))

# ------------- ISKANJE CSV ----------------------
def candidate_dirs():
    here = Path(__file__).resolve().parent
    home = Path.home()
    dirs = [here]

    for desk in [
        home / "Desktop",
        home / "Namizje",
        home / "OneDrive" / "Desktop",
        home / "OneDrive" / "Namizje",
        home / "OneDrive - Personal" / "Desktop",
        home / "OneDrive - Personal" / "Namizje",
    ]:
        if desk.exists(): dirs.append(desk)

    for dl in [home / "Downloads", home / "Prenosi"]:
        if dl.exists(): dirs.append(dl)

    if (here / "out").exists(): dirs.append(here / "out")
    if here.parent.exists(): dirs.append(here.parent)

    seen, uniq = set(), []
    for d in dirs:
        if d not in seen:
            uniq.append(d); seen.add(d)
    return uniq

def find_latest_csv():
    if len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
        p = Path(sys.argv[1]).expanduser()
        if p.exists() and p.suffix.lower() == ".csv":
            return p

    hits = []
    for d in candidate_dirs():
        for pat in CANDIDATE_PATTERNS:
            hits.extend(Path(d).glob(pat))

    if not hits:
        return None

    hits.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    # DEBUG: izpisi najdene datoteke
    if "--debug" in sys.argv:
        print("Najdene CSV datoteke:")
        for p in hits[:10]:
            print("  -", p)
    return hits[0]

# ------------------ MAIN ------------------------
def main():
    parser = argparse.ArgumentParser(description="Uvoz CC delta v SQLite")
    parser.add_argument("csv", nargs="?", help="Pot do CSV (neobvezno)")
    parser.add_argument("--mode", choices=["replace","append"], default="replace",
    help="replace: zamenja vse opise za gesla iz CSV; append: samo doda nove pare")
    args = parser.parse_args()

    csv_path = find_latest_csv()
    if args.debug:
        print("Uporabljam CSV:", csv_path)
    if not csv_path:
        print("CSV nisem našel. Daj mi pot kot argument ali shrani datoteko kot 'cc_clues_DISPLAY_UTF8*.csv' na Namizje/OneDrive Namizje/Prenosi/out.")
        sys.exit(1)

    rows, delim = open_csv_rows(csv_path)
    if not rows:
        print("CSV je prazen.")
        sys.exit(1)

    first = rows[0]
    data_start = 1
    header_idx = {}
    if looks_like_header(first):
        header_idx = map_header(first)
    else:
        data_start = 0
        header_idx = {"word": 0, "clue": 1}
        if len(first) > 2: header_idx["date"] = 2
        if len(first) > 3: header_idx["citation"] = 3

    if not REQUIRED.issubset(header_idx):
        print(f"Ne najdem obveznih stolpcev (Word/GESLO in Clue/OPIS). Najdene glave/indeksi: {header_idx}")
        preview = rows[:2]
        print("Predogled prvih vrstic:", preview)
        sys.exit(1)

    # 1) Zberi vrstice (samo citation == 'vpis')
    entries = []
    for r in rows[data_start:]:
        if not r or all(not norm(x) for x in r):
            continue
        word = norm(r[header_idx["word"]]) if len(r) > header_idx["word"] else ""
        clue = norm(r[header_idx["clue"]]) if len(r) > header_idx["clue"] else ""
        cit  = norm(r[header_idx["citation"]]) if "citation" in header_idx and len(r) > header_idx["citation"] else ""
        if not word or not clue:
            continue
        if (cit or "").lower() != "vpis":
            continue
        entries.append((word, clue))

    if not entries:
        print("Ni vnosov s citation='vpis'. Ni kaj uvoziti.")
        sys.exit(0)

    # 2) Po geslih združi vnose iz CSV
    by_word = {}
    for w, c in entries:
        by_word.setdefault(w, []).append(c)

    conn = sqlite3.connect(DB_PATH)
    table = col_word = col_clue = None
    replaced_words = inserted_pairs = appended_pairs = 0

    try:
        table, col_word, col_clue = detect_table_and_columns(conn)
        print(f"Uporabljam tabelo: {table} | stolpca: {col_word} (geslo), {col_clue} (opis)")
        conn.execute("BEGIN")
        for w, clues in by_word.items():
            if args.mode == "replace":
                delete_by_word(conn, table, col_word, w)
                replaced_words += 1
                for c in clues:
                    insert_pair(conn, table, col_word, col_clue, w, c)
                    inserted_pairs += 1
            else:  # append
                for c in clues:
                    insert_pair(conn, table, col_word, col_clue, w, c)
                    appended_pairs += 1
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    ts = datetime.fromtimestamp(csv_path.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
    print(f"Najden CSV: {csv_path} (zadnja sprememba: {ts}) | delimiter: '{delim}'")
    print(f"DB: {DB_PATH}")
    if args.mode == "replace":
        print(f"Zamenjanih gesel: {replaced_words}")
        print(f"Vstavljenih parov (po zamenjavi): {inserted_pairs}")
    else:
        print(f"Dodanih novih parov (append): {appended_pairs}")
