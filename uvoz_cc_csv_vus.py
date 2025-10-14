#!/usr/bin/env python3
"""
Uvoz Crossword Compiler (CC) CSV → VUS.db (SQLite), robustna različica s filtrom po Citation.

Privzeto uvozi SAMO vrstice, kjer stolpec 'Citation' vsebuje niz 'vpis'.
Filter lahko spremeniš z --only-citation-contains ali izklopiš z --all.

- Ciljna tabela: slovar(id INTEGER PK, geslo TEXT, opis TEXT, ...),
  upošteva UNIQUE(geslo, opis) v tvoji bazi.
- Upsert:
    * če (geslo) obstaja (case-insensitive):
        - update opis samo, če je drugačen IN ne krši UNIQUE(geslo, opis)
        - sicer skip
    * če ne obstaja: insert
- Robustnosti:
    * odstrani BOM iz glave
    * autodetect CSV ločilo (comma/semicolon)
    * normalizira NBSP in presledke
    * varno preskoči konfliktnen UPDATE/INSERT
"""

import argparse
import csv
import os
import sqlite3
import sys
from contextlib import closing

POSSIBLE_WORD_COLS = {"word", "geslo", "entry", "answer"}
POSSIBLE_CLUE_COLS = {"clue", "opis", "definition", "hint"}

def try_open_csv(path, forced_encoding=None):
    encodings = [forced_encoding] if forced_encoding else ["utf-8-sig", "utf-8", "cp1250", "windows-1250", "latin1"]
    last_err = None
    for enc in encodings:
        try:
            f = open(path, "r", encoding=enc, newline="")
            head = f.read(2048)
            f.seek(0)
            return f, enc, head
        except Exception as e:
            last_err = e
    raise RuntimeError(f"Ne morem odpreti CSV '{path}' (poskusi: {encodings}). Zadnja napaka: {last_err}")

def sniff_dialect(sample_text: str):
    sc = sample_text.count(';')
    cc = sample_text.count(',')
    if sc > cc:
        class Semi(csv.excel):
            delimiter = ';'
        return Semi()
    return csv.excel()

def normalize_text(s: str) -> str:
    if s is None:
        return ""
    s = s.replace("\u00A0", " ").replace("\u2007", " ").replace("\u202F", " ")
    s = " ".join(s.strip().split())
    return s

def ensure_schema(conn: sqlite3.Connection):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS slovar (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            geslo TEXT NOT NULL,
            opis  TEXT NOT NULL
        );
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_slovar_geslo_nocase ON slovar(geslo COLLATE NOCASE);")

def detect_columns(header, word_col_opt=None, clue_col_opt=None):
    cols = [h.strip().lower().lstrip('\ufeff') for h in header]
    word_idx = clue_idx = None

    if word_col_opt:
        wl = word_col_opt.strip().lower()
        if wl in cols:
            word_idx = cols.index(wl)
    if clue_col_opt:
        cl = clue_col_opt.strip().lower()
        if cl in cols:
            clue_idx = cols.index(cl)

    if word_idx is None:
        for i, h in enumerate(cols):
            if h in POSSIBLE_WORD_COLS:
                word_idx = i; break
    if clue_idx is None:
        for i, h in enumerate(cols):
            if h in POSSIBLE_CLUE_COLS:
                clue_idx = i; break
    return word_idx, clue_idx, cols

def select_existing_id_and_opis(conn: sqlite3.Connection, geslo: str):
    row = conn.execute(
        "SELECT id, opis FROM slovar WHERE lower(geslo)=lower(?) LIMIT 1;",
        (geslo,)
    ).fetchone()
    if row:
        return row[0], row[1]
    return None, None

def pair_exists_elsewhere(conn: sqlite3.Connection, geslo: str, opis: str, exclude_id: int) -> bool:
    row = conn.execute(
        "SELECT 1 FROM slovar WHERE lower(geslo)=lower(?) AND opis=? AND id<>? LIMIT 1;",
        (geslo, opis, exclude_id)
    ).fetchone()
    return row is not None

def exact_pair_exists(conn: sqlite3.Connection, geslo: str, opis: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM slovar WHERE lower(geslo)=lower(?) AND opis=? LIMIT 1;",
        (geslo, opis)
    ).fetchone()
    return row is not None

def upsert_row(conn: sqlite3.Connection, geslo: str, opis: str, overwrite: bool):
    """
    Vrne: ("insert"/"update"/"skip", id ali None)
    """
    geslo = normalize_text(geslo)
    opis  = normalize_text(opis)

    if not geslo:
        return ("skip", None)
    if not opis:
        existing_id, _ = select_existing_id_and_opis(conn, geslo)
        return ("skip", existing_id)

    existing_id, existing_opis = select_existing_id_and_opis(conn, geslo)
    if existing_id is None:
        if exact_pair_exists(conn, geslo, opis):
            return ("skip", None)
        try:
            cur = conn.execute("INSERT INTO slovar(geslo, opis) VALUES (?, ?);", (geslo, opis))
            return ("insert", cur.lastrowid)
        except sqlite3.IntegrityError:
            return ("skip", None)

    # UPDATE – samo če drugačen opis in dovoljeno prepisovanje ali je obstoječi prazen
    if opis != (existing_opis or "") and (overwrite or not existing_opis):
        if pair_exists_elsewhere(conn, geslo, opis, existing_id):
            return ("skip", existing_id)
        try:
            conn.execute("UPDATE slovar SET opis=? WHERE id=?;", (opis, existing_id))
            return ("update", existing_id)
        except sqlite3.IntegrityError:
            return ("skip", existing_id)

    return ("skip", existing_id)

def run(csv_path: str, db_path: str, word_col: str = None, clue_col: str = None,
        encoding: str = None, overwrite: bool = True, dry_run: bool = False,
        commit_every: int = 1000, verbose: bool = False,
        only_citation_contains: str | None = "vpis", import_all: bool = False):
    if not os.path.exists(csv_path):
        print(f"❌ CSV ne obstaja: {csv_path}"); sys.exit(1)

    db_existed = os.path.exists(db_path)

    f, used_enc, head = try_open_csv(csv_path, forced_encoding=encoding)
    dialect = sniff_dialect(head)

    with f:
        reader = csv.reader(f, dialect=dialect)
        header = next(reader, None)
        if not header:
            print("❌ CSV je prazen ali nima glave."); sys.exit(1)

        w_idx, c_idx, cols = detect_columns(header, word_col, clue_col)
        if w_idx is None or c_idx is None:
            print(f"❌ Ne najdem stolpcev za geslo/word in opis/clue v glavi: {header}")
            print("   Uporabi npr.: --word-col Answer --clue-col Clue")
            sys.exit(1)

        # Citation index (za filter)
        citation_idx = None
        for i, h in enumerate(cols):
            if h == "citation":
                citation_idx = i
                break
        if (only_citation_contains is not None) and import_all:
            only_citation_contains = None  # --all izklopi filter
        if (only_citation_contains is not None) and (citation_idx is None):
            print("❌ Zahtevan je filter po Citation, a stolpec 'Citation' v CSV ne obstaja.")
            sys.exit(1)

        with closing(sqlite3.connect(db_path)) as conn:
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA synchronous=NORMAL;")
            conn.execute("PRAGMA temp_store=MEMORY;")

            ensure_schema(conn)

            inserted = updated = skipped = 0
            filtered_out = 0
            batch = 0

            try:
                conn.execute("BEGIN;")
                for row in reader:
                    if not row:
                        continue

                    # Filter po Citation (privzeto: 'vpis')
                    if only_citation_contains is not None:
                        cit = row[citation_idx] if (citation_idx is not None and citation_idx < len(row)) else ""
                        if only_citation_contains.lower() not in (cit or "").lower():
                            filtered_out += 1
                            continue

                    word = row[w_idx] if w_idx < len(row) else ""
                    clue = row[c_idx] if c_idx < len(row) else ""

                    action, _ = upsert_row(conn, word, clue, overwrite=overwrite)
                    if action == "insert":
                        inserted += 1
                    elif action == "update":
                        updated += 1
                    else:
                        skipped += 1

                    batch += 1
                    if verbose and batch % 20000 == 0:
                        print(f"… obdelanih {batch} (➕ {inserted}, ✏️ {updated}, ⏭️ {skipped}, 🔎 filter out {filtered_out})")
                    if batch % commit_every == 0 and not dry_run:
                        conn.execute("COMMIT;")
                        conn.execute("BEGIN;")

                if dry_run:
                    conn.execute("ROLLBACK;")
                else:
                    conn.execute("COMMIT;")
            except KeyboardInterrupt:
                if not dry_run:
                    conn.execute("COMMIT;")
                raise
            except Exception:
                conn.execute("ROLLBACK;")
                raise

    delim = ';' if hasattr(dialect, 'delimiter') and getattr(dialect, 'delimiter', ',') == ';' else ','
    print("──────── Povzetek ────────")
    print(f"📄 CSV:        {csv_path}  (encoding: {used_enc}, delimiter: {delim})")
    print(f"🗄️  Baza:       {db_path}  ({'obstajala' if db_existed else 'nova'})")
    if only_citation_contains is not None:
        print(f"🔎 Filter:     Citation contains \"{only_citation_contains}\"")
        print(f"🚫 Preskočenih zaradi filtra: {filtered_out}")
    else:
        print(f"🔎 Filter:     (brez) — uvoženo vse vrstice")
    print(f"➕ Dodanih:    {inserted}")
    print(f"✏️  Posodobljenih: {updated}")
    print(f"⏭️  Preskočenih:   {skipped}")
    print(f"🔁 Overwrite:  {'DA' if overwrite else 'NE'}")
    print("──────────────────────────")

def main():
    ap = argparse.ArgumentParser(description="Uvoz CC CSV v VUS.db (tabela 'slovar').")
    ap.add_argument("csv", help="Pot do .csv (npr. out/cc_clues_UTF8.csv)")
    ap.add_argument("db",  help="Pot do SQLite baze (npr. VUS.db)")
    ap.add_argument("--word-col", help="Ime stolpca za geslo (npr. Answer/Word/Geslo)", default=None)
    ap.add_argument("--clue-col", help="Ime stolpca za opis (npr. Clue/Opis/Definition)", default=None)
    ap.add_argument("--encoding", help="Prisili kodiranje (utf-8, cp1250, ...)", default=None)
    ap.add_argument("--no-overwrite", action="store_true", help="Ne prepisuj obstoječih opisov (posodobi samo, če je prazen).")
    ap.add_argument("--dry-run", action="store_true", help="Samo simulacija brez zapisovanja.")
    ap.add_argument("--commit-every", type=int, default=1000, help="Commit na N vrstic (privzeto 1000).")
    ap.add_argument("--verbose", action="store_true", help="Vmesni izpisi napredka.")

    # NOVO: filter po Citation
    ap.add_argument("--only-citation-contains", default="vpis",
                    help="Uvozi samo vrstice, kjer Citation vsebuje to vrednost. Privzeto: 'vpis'.")
    ap.add_argument("--all", dest="import_all", action="store_true",
                    help="Ignoriraj Citation filter (uvozi vse vrstice).")

    args = ap.parse_args()

    run(
        csv_path=args.csv,
        db_path=args.db,
        word_col=args.word_col,
        clue_col=args.clue_col,
        encoding=args.encoding,
        overwrite=not args.no_overwrite,
        dry_run=args.dry_run,
        commit_every=args.commit_every,
        verbose=args.verbose,
        only_citation_contains=args.only_citation_contains,
        import_all=args.import_all,
    )

if __name__ == "__main__":
    main()
