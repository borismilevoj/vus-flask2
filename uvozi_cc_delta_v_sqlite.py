#!/usr/bin/env python3
"""
Uvoz Crossword Compiler (CC) CSV → VUS.db (SQLite).

Privzeto:
- uvozi VSE vrstice (brez Citation filtra)
- če želiš filtrirati po Citation, uporabi: --only-citation-contains "vpis"
- če podaš --all, se Citation filter ignorira

Ciljna tabela: slovar(id INTEGER PK, geslo TEXT, opis TEXT)
Upsert:
- če geslo obstaja (case-insensitive):
    - update opis, če je drugačen in je dovoljeno overwrite
- če ne obstaja: insert
Robustnost:
- odstrani BOM
- autodetect delimiter (, ali ;)
- normalizira NBSP in presledke
- varno ravnanje pri konfliktih
- varno transaction rollback (samo če je aktiven)
- ASCII-safe izpisi (brez emoji), da Windows cp1250 ne sesuje procesa
"""

import argparse
import csv
import os
import sqlite3
import sys
from contextlib import closing

POSSIBLE_WORD_COLS = {"word", "geslo", "entry", "answer"}
POSSIBLE_CLUE_COLS = {"clue", "opis", "definition", "hint"}


def _safe_reconfigure_stdio():
    """Poskusi preklopit stdout/stderr na utf-8; če ne gre, ignoriraj.
    Izpisi so sicer ASCII-safe."""
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def try_open_csv(path, forced_encoding=None):
    encodings = [forced_encoding] if forced_encoding else [
        "utf-8-sig", "utf-8", "cp1250", "windows-1250", "latin1"
    ]
    last_err = None
    for enc in encodings:
        try:
            f = open(path, "r", encoding=enc, newline="")
            head = f.read(2048)
            f.seek(0)
            return f, enc, head
        except Exception as e:
            last_err = e
    raise RuntimeError(
        f"Ne morem odpreti CSV '{path}' (poskusi: {encodings}). Zadnja napaka: {last_err}"
    )


def sniff_dialect(sample_text: str):
    sc = sample_text.count(";")
    cc = sample_text.count(",")
    if sc > cc:
        class Semi(csv.excel):
            delimiter = ";"
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
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            geslo TEXT NOT NULL,
            opis  TEXT NOT NULL
        );
    """)
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_slovar_geslo_nocase ON slovar(geslo COLLATE NOCASE);"
    )


def detect_columns(header, word_col_opt=None, clue_col_opt=None):
    cols_raw = header[:]
    cols = [h.strip().lower().lstrip("\ufeff") for h in header]
    word_idx = clue_idx = None

    if word_col_opt:
        wl = word_col_opt.strip().lower()
        if wl in cols:
            word_idx = cols.index(wl)
    if clue_col_opt:
        cl = clue_col_opt.strip().lower()
        if cl in cols:
            clue_idx = cols.index(cl)

    looks_like_header = any(x in cols for x in POSSIBLE_WORD_COLS) or any(
        x in cols for x in POSSIBLE_CLUE_COLS
    )

    if word_idx is None and looks_like_header:
        for i, h in enumerate(cols):
            if h in POSSIBLE_WORD_COLS:
                word_idx = i
                break
    if clue_idx is None and looks_like_header:
        for i, h in enumerate(cols):
            if h in POSSIBLE_CLUE_COLS:
                clue_idx = i
                break

    return word_idx, clue_idx, cols_raw, looks_like_header


def select_existing_id_and_opis(conn: sqlite3.Connection, geslo: str):
    row = conn.execute(
        "SELECT id, opis FROM slovar WHERE lower(geslo)=lower(?) LIMIT 1;",
        (geslo,),
    ).fetchone()
    if row:
        return row[0], row[1]
    return None, None


def pair_exists_elsewhere(conn: sqlite3.Connection, geslo: str, opis: str, exclude_id: int) -> bool:
    row = conn.execute(
        "SELECT 1 FROM slovar WHERE lower(geslo)=lower(?) AND opis=? AND id<>? LIMIT 1;",
        (geslo, opis, exclude_id),
    ).fetchone()
    return row is not None


def exact_pair_exists(conn: sqlite3.Connection, geslo: str, opis: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM slovar WHERE lower(geslo)=lower(?) AND opis=? LIMIT 1;",
        (geslo, opis),
    ).fetchone()
    return row is not None


def upsert_row(conn: sqlite3.Connection, geslo: str, opis: str, overwrite: bool):
    geslo = normalize_text(geslo)
    opis = normalize_text(opis)

    if not geslo:
        return ("skip", None)

    # Ne ruši obstoječih opisov s praznim
    if not opis:
        existing_id, _ = select_existing_id_and_opis(conn, geslo)
        return ("skip", existing_id)

    existing_id, existing_opis = select_existing_id_and_opis(conn, geslo)

    # Insert
    if existing_id is None:
        if exact_pair_exists(conn, geslo, opis):
            return ("skip", None)
        try:
            cur = conn.execute(
                "INSERT INTO slovar(geslo, opis) VALUES (?, ?);",
                (geslo, opis),
            )
            return ("insert", cur.lastrowid)
        except sqlite3.IntegrityError:
            return ("skip", None)

    # Update
    if opis != (existing_opis or "") and (overwrite or not existing_opis):
        if pair_exists_elsewhere(conn, geslo, opis, existing_id):
            return ("skip", existing_id)
        try:
            conn.execute("UPDATE slovar SET opis=? WHERE id=?;", (opis, existing_id))
            return ("update", existing_id)
        except sqlite3.IntegrityError:
            return ("skip", existing_id)

    return ("skip", existing_id)


def refresh_slovar_sortiran(db_path: str):
    """Rebuild tabela slovar_sortiran v svoji povezavi. Če pade, naj ne sesuje uvoza."""
    con = sqlite3.connect(db_path)
    try:
        con.execute("BEGIN;")
        con.execute("CREATE TABLE IF NOT EXISTS slovar_sortiran (geslo TEXT, opis TEXT);")
        con.execute("DELETE FROM slovar_sortiran;")
        con.execute("""
            INSERT OR IGNORE INTO slovar_sortiran(geslo, opis)
            SELECT geslo, opis
            FROM slovar
            ORDER BY
              CASE
                WHEN instr(opis, ' - ') > 0
                  THEN lower(trim(substr(opis, instr(opis, ' - ')+3)))
                ELSE lower(opis)
              END
        """)
        con.execute("COMMIT;")
    except Exception:
        try:
            if con.in_transaction:
                con.execute("ROLLBACK;")
        except Exception:
            pass
        raise
    finally:
        con.close()


def run(
    csv_path: str,
    db_path: str,
    word_col: str | None = None,
    clue_col: str | None = None,
    encoding: str | None = None,
    overwrite: bool = True,
    dry_run: bool = False,
    commit_every: int = 1000,
    verbose: bool = False,
    only_citation_contains: str | None = None,
    import_all: bool = False,
    refresh_sortiran: bool = True,
):
    _safe_reconfigure_stdio()

    db_existed = os.path.exists(db_path)

    f, used_enc, head = try_open_csv(csv_path, forced_encoding=encoding)
    dialect = sniff_dialect(head)

    with f:
        reader = csv.reader(f, dialect=dialect)

        header = next(reader, None)
        if not header:
            print("ERROR: CSV je prazen ali nima glave/prve vrstice.")
            sys.exit(1)

        w_idx, c_idx, cols_raw, looks_like_header = detect_columns(header, word_col, clue_col)

        if w_idx is None or c_idx is None:
            if not looks_like_header:
                w_idx, c_idx = 0, 1
            else:
                print(f"ERROR: Ne najdem stolpcev za geslo/word in opis/clue v glavi: {header}")
                print("       Uporabi npr.: --word-col Answer --clue-col Clue")
                sys.exit(1)

        # Citation indeks
        citation_idx = None
        if looks_like_header:
            for i, h in enumerate([h.strip().lower() for h in cols_raw]):
                if h == "citation":
                    citation_idx = i
                    break
        else:
            # brez headerja: CC tipično: Word, Clue, Date, Citation
            if len(header) > 3:
                citation_idx = 3

        # --all vedno izklopi filter
        if import_all:
            only_citation_contains = None

        if (only_citation_contains is not None) and (citation_idx is None):
            print("ERROR: Zahtevan je filter po Citation, a stolpec 'Citation' v CSV ne obstaja.")
            sys.exit(1)

        with closing(sqlite3.connect(db_path)) as conn:
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA synchronous=NORMAL;")
            conn.execute("PRAGMA temp_store=MEMORY;")

            ensure_schema(conn)

            inserted = updated = skipped = 0
            filtered_out = 0
            processed = 0

            if verbose:
                mode = "ALL (brez filtra)" if (import_all or only_citation_contains is None) else (
                    f"Citation contains '{only_citation_contains}'"
                )
                delim = getattr(dialect, "delimiter", ",")
                print(f"[run] mode = {mode}; encoding={used_enc}; delimiter='{delim}', header={'DA' if looks_like_header else 'NE'}")

            def row_passes_filter(row_) -> bool:
                if only_citation_contains is None:
                    return True
                cit = row_[citation_idx] if (citation_idx is not None and citation_idx < len(row_)) else ""
                return (only_citation_contains.lower() in (cit or "").lower())

            try:
                conn.execute("BEGIN;")

                # Če ni headerja, je 'header' dejansko prva data vrstica
                if not looks_like_header:
                    row = header
                    if row and row_passes_filter(row):
                        word = row[w_idx] if w_idx < len(row) else ""
                        clue = row[c_idx] if c_idx < len(row) else ""
                        action, _ = upsert_row(conn, word, clue, overwrite=overwrite)
                        if action == "insert":
                            inserted += 1
                        elif action == "update":
                            updated += 1
                        else:
                            skipped += 1
                        processed += 1
                    else:
                        filtered_out += 1

                for row in reader:
                    if not row:
                        continue

                    if not row_passes_filter(row):
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

                    processed += 1

                    if processed % commit_every == 0 and not dry_run:
                        conn.execute("COMMIT;")
                        conn.execute("BEGIN;")

                    if verbose and processed % 20000 == 0:
                        print(f"... obdelanih {processed} (+ {inserted}, * {updated}, >> {skipped}, filter_out {filtered_out})")

                if dry_run:
                    if conn.in_transaction:
                        conn.execute("ROLLBACK;")
                else:
                    conn.execute("COMMIT;")

                    if refresh_sortiran:
                        try:
                            refresh_slovar_sortiran(db_path)
                            if verbose:
                                print("[refresh] slovar_sortiran: osvezen (sort po delu za ' - ')")
                        except Exception as e:
                            print(f"[warn] slovar_sortiran refresh ni uspel: {e}")

            except KeyboardInterrupt:
                # Če user prekine: commitaj, kar je že v batchih (razen dry-run), pa dvigni naprej
                if not dry_run:
                    try:
                        if conn.in_transaction:
                            conn.execute("COMMIT;")
                    except Exception:
                        pass
                raise
            except Exception:
                try:
                    if conn.in_transaction:
                        conn.execute("ROLLBACK;")
                except Exception:
                    pass
                raise

    delim = getattr(dialect, "delimiter", ",")
    print("-------- Povzetek --------")
    print(f"CSV:  {csv_path}  (encoding: {used_enc}, delimiter: {delim})")
    print(f"DB:   {db_path}  ({'obstajala' if db_existed else 'nova'})")
    if only_citation_contains is not None:
        print(f"Filter: Citation contains '{only_citation_contains}'")
        print(f"Filter_out: {filtered_out}")
    else:
        print("Filter: (brez) - uvozene vse vrstice")
    print(f"Inserted: {inserted}")
    print(f"Updated:  {updated}")
    print(f"Skipped:  {skipped}")
    print(f"Overwrite: {'DA' if overwrite else 'NE'}")
    print("--------------------------")

    return {
        "inserted": inserted,
        "updated": updated,
        "skipped": skipped,
        "filtered_out": filtered_out,
        "import_all": import_all,
        "only_citation_contains": only_citation_contains,
    }


def main():
    ap = argparse.ArgumentParser(description="Uvoz CC CSV v VUS.db (tabela 'slovar').")
    ap.add_argument("csv", help="Pot do .csv (npr. out/cc_clues_UTF8.csv)")
    ap.add_argument("db", help="Pot do SQLite baze (npr. VUS.db)")

    ap.add_argument("--word-col", default=None, help="Ime stolpca za geslo (npr. Answer/Word/Geslo)")
    ap.add_argument("--clue-col", default=None, help="Ime stolpca za opis (npr. Clue/Opis/Definition)")
    ap.add_argument("--encoding", default=None, help="Prisili kodiranje (utf-8, cp1250, ...)")

    ap.add_argument("--no-overwrite", action="store_true",
                    help="Ne prepisuj obstoječih opisov (posodobi samo, če je prazen).")
    ap.add_argument("--dry-run", action="store_true", help="Samo simulacija brez zapisovanja.")
    ap.add_argument("--commit-every", type=int, default=1000, help="Commit na N vrstic (privzeto 1000).")
    ap.add_argument("--verbose", action="store_true", help="Vmesni izpisi napredka.")

    ap.add_argument("--only-citation-contains", default=None,
                    help="Uvozi samo vrstice, kjer Citation vsebuje to vrednost (npr. 'vpis').")

    ap.add_argument("--all", dest="import_all", action="store_true", default=False,
                    help="Ignoriraj Citation filter in uvozi vse vrstice (ALL mode).")

    ap.add_argument("--refresh-sortiran", dest="refresh_sortiran", action="store_true", default=True,
                    help="Po uvozu rebuild slovar_sortiran (privzeto vklopljeno).")
    ap.add_argument("--no-refresh-sortiran", dest="refresh_sortiran", action="store_false",
                    help="Ne rebuildaj slovar_sortiran po uvozu.")

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
        refresh_sortiran=args.refresh_sortiran,
    )


if __name__ == "__main__":
    main()
