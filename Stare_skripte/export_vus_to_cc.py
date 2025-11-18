import os, csv, sqlite3, re, sys

# --- Konfiguracija prek okolja ---
DB_PATH     = os.getenv("DB_PATH", "VUS.db")
TABLE_NAME  = os.getenv("TABLE_NAME")          # npr. "slovar"
COL_GESLO   = os.getenv("COL_GESLO")           # npr. "geslo"
COL_OPIS    = os.getenv("COL_OPIS")            # npr. "opis"

# --- Izhodi ---
OUT_DIR = os.path.join(os.getcwd(), "out")
os.makedirs(OUT_DIR, exist_ok=True)

# CP1250 (ANSI) – ZA STAREJŠE CC
WORDS_CP1250 = os.path.join(OUT_DIR, "cc_words.txt")
CLUES_CP1250 = os.path.join(OUT_DIR, "cc_clues_ANSI.csv")

# UTF-8 (z BOM) – ZA Novejše CC, ohrani vse znake († …)
WORDS_UTF8   = os.path.join(OUT_DIR, "cc_words_utf8.txt")
CLUES_UTF8   = os.path.join(OUT_DIR, "cc_clues_UTF8.csv")

# --- Čiščenje ---
INVISIBLES_RE = re.compile(r"[\uFEFF\u200B\u200C\u200D\u2060\u00A0]")  # BOM, ZWSP/ZWJ/ZWNJ/WORD-JOINER, NBSP

def clean_text(s: str) -> str:
    if not s:
        return ""
    s = s.replace("\u00A0", " ")    # NBSP -> space
    s = INVISIBLES_RE.sub("", s)    # odstrani nevidne like
    return s.strip()

def grid_answer(s: str) -> str:
    s = clean_text(s)
    # odstrani presledke, vse vrste vezajev in apostrofe
    s = re.sub(r"[ \-\u2010-\u2015'’`]", "", s)
    return s.upper()

def pick_table_and_columns(con: sqlite3.Connection):
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall()]

    table = None
    if TABLE_NAME:
        if TABLE_NAME in tables:
            table = TABLE_NAME
        else:
            raise RuntimeError(f"TABLE_NAME='{TABLE_NAME}' ni v bazi. Najdene tabele: {tables}")

    if not table:
        for cand in ("slovar", "slovar_sortiran", "slovar_backup"):
            if cand in tables:
                table = cand
                break
    if not table:
        raise RuntimeError(f"V bazi ni pričakovane tabele. Najdene: {tables}")

    cur.execute(f"PRAGMA table_info({table})")
    cols = {r[1].lower(): r[1] for r in cur.fetchall()}  # lower -> original
    g = COL_GESLO or ("geslo" if "geslo" in cols else None)
    o = COL_OPIS  or ("opis"  if "opis"  in cols else None)
    if not (g and o):
        raise RuntimeError(f"V tabeli {table} ni pričakovanih stolpcev. Najdeni: {list(cols.values())}")
    return table, cols[g.lower()], cols[o.lower()]

def fetch_rows(con, table, col_geslo, col_opis):
    cur = con.cursor()
    sql = f"""
      SELECT {col_geslo} AS geslo, {col_opis} AS opis
      FROM {table}
      WHERE {col_geslo} IS NOT NULL AND TRIM({col_geslo}) <> ''
    """
    cur.execute(sql)
    return cur.fetchall()

def write_words(path: str, rows, encoding: str):
    count = 0
    with open(path, "w", encoding=encoding, newline="") as f:
        for geslo, _ in rows:
            ans = grid_answer(geslo)
            if not ans:
                continue
            try:
                f.write(ans + "\r\n")  # CRLF
                count += 1
            except UnicodeEncodeError:
                # pri CP1250 lahko pade na redkih znakih – zamenjaj z 'ignore'
                enc = ans.encode(encoding, "ignore").decode(encoding)
                if enc:
                    f.write(enc + "\r\n")
                    count += 1
    return count

def write_clues(path: str, rows, encoding: str):
    count = 0
    with open(path, "w", encoding=encoding, newline="") as f:
        wr = csv.writer(f, delimiter=",", quotechar='"',
                        quoting=csv.QUOTE_MINIMAL, lineterminator="\r\n")
        wr.writerow(["Answer", "Clue", "Citation", "Display"])
        for geslo, opis in rows:
            display = clean_text(geslo)
            clue    = clean_text(opis)
            ans     = grid_answer(display)
            if not ans:
                continue
            try:
                wr.writerow([ans, clue, "", display])
                count += 1
            except UnicodeEncodeError:
                # CP1250 fallback
                wr.writerow([
                    ans.encode(encoding, "ignore").decode(encoding),
                    clue.encode(encoding, "ignore").decode(encoding),
                    "",
                    display.encode(encoding, "ignore").decode(encoding),
                ])
                count += 1
    return count

def main():
    abs_db = os.path.abspath(DB_PATH)
    size = os.path.getsize(DB_PATH) if os.path.exists(DB_PATH) else 0
    print(f"DB: {abs_db}  ({size} bytes)", file=sys.stderr)
    if size == 0:
        raise FileNotFoundError("DB ne obstaja ali je prazna.")

    con = sqlite3.connect(DB_PATH)
    try:
        table, col_g, col_o = pick_table_and_columns(con)
        print(f"Uporabljam tabelo: {table}  | stolpca: {col_g}/{col_o}", file=sys.stderr)
        rows = fetch_rows(con, table, col_g, col_o)
        print(f"Najdenih vrstic: {len(rows)}", file=sys.stderr)

        # --- CP1250 (ANSI) ---
        w_cp = write_words(WORDS_CP1250, rows, "cp1250")
        c_cp = write_clues(CLUES_CP1250, rows, "cp1250")

        # --- UTF-8 z BOM ---
        w_u8 = write_words(WORDS_UTF8, rows, "utf-8-sig")
        c_u8 = write_clues(CLUES_UTF8, rows, "utf-8-sig")

        print(f"CP1250  -> Words: {WORDS_CP1250} ({w_cp}), Clues: {CLUES_CP1250} ({c_cp})")
        print(f"UTF8-BOM-> Words: {WORDS_UTF8}   ({w_u8}), Clues: {CLUES_UTF8}   ({c_u8})")
    finally:
        con.close()

if __name__ == "__main__":
    main()
