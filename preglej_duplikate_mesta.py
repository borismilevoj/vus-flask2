# preglej_duplikate_mesta.py
import csv
import os
import sqlite3
import unicodedata
import re
import argparse

# --- Normalizacija gesla: šumnike -> ASCII, vezaj -> presledek, odvečni znaki ven, stisni presledke, UPPER
def norm_key(s: str) -> str:
    if s is None:
        return ""
    s = unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode("utf-8")
    s = s.replace("-", " ")  # pomišljaj -> presledek (kot v VUS)
    s = re.sub(r"[’'`^~.,;:()\\[\\]{}]", "", s)
    s = re.sub(r"\\s+", " ", s).strip()
    return s.upper()

def load_db_norm_map(db_path: str, opis_prefix: str = "mesto v "):
    """
    Vrne mapo: NORMALIZIRANO_GESLO -> [obstoječi_opisi, ...],
    vendar samo za zapise, kjer OPIS začne z 'mesto v ' (case-insensitive).
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # case-insensitive filter; SQLite LIKE je za ASCII že case-insensitive
    cur.execute("SELECT GESLO, OPIS FROM slovar WHERE lower(OPIS) LIKE ?", (opis_prefix.lower() + "%",))
    m = {}
    for geslo, opis in cur.fetchall():
        k = norm_key(geslo)
        m.setdefault(k, []).append(opis or "")
    conn.close()
    return m

def read_csv(input_csv: str):
    rows = []
    with open(input_csv, newline="", encoding="utf-8-sig") as f:
        r = csv.DictReader(f)
        # pričakovani stolpci iz tvojega batch-a: GESLO, GESLO_NORM (opcijsko), OPIS
        for row in r:
            rows.append({
                "GESLO": (row.get("GESLO") or "").strip(),
                "OPIS": (row.get("OPIS") or "").strip(),
                "GESLO_NORM": (row.get("GESLO_NORM") or "").strip()
            })
    return rows

def write_csv(rows, out_path):
    # vedno zapišemo glavo, tudi če je prazno
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["GESLO","GESLO_NORM","OPIS","STATUS","OBSTOJEČI_OPISI"])
        for r in rows:
            w.writerow([r["GESLO"], r["GESLO_NORM"], r["OPIS"], r["STATUS"], r.get("OBSTOJEČI_OPISI","")])

def apply_inserts(db_path: str, rows_new):
    if not rows_new:
        return 0
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    for r in rows_new:
        cur.execute("INSERT INTO slovar (GESLO, OPIS) VALUES (?, ?)", (r["GESLO"], r["OPIS"]))
    conn.commit()
    conn.close()
    return len(rows_new)

def main():
    ap = argparse.ArgumentParser(description="Pred-uvozni pregled za mesta (duplikati le, če OPIS začne z 'mesto v ').")
    ap.add_argument("--in", dest="infile", required=True, help="Vhodni CSV iz gen_mesta_batch.py")
    ap.add_argument("--db", dest="db", default="VUS.db", help="Pot do VUS.db (privzeto VUS.db)")
    ap.add_argument("--out-prefix", dest="out_prefix", help="Izhodni prefix (privzeto ime vhoda brez .csv)")
    ap.add_argument("--opis-prefix", dest="opis_prefix", default="mesto v ",
                    help="Prefix opisa za detekcijo dvojnikov (privzeto 'mesto v ')")
    ap.add_argument("--apply", action="store_true", help="Takoj vstavi NOVO zapise v bazo")
    args = ap.parse_args()

    infile = args.infile
    if not os.path.exists(infile):
        print("Napaka: vhodni CSV ne obstaja.")
        return 2

    base_prefix = args.out_prefix or os.path.splitext(os.path.basename(infile))[0]
    out_new = f"{base_prefix}_NOVO.csv"
    out_dup = f"{base_prefix}_DUPLIKATI.csv"

    print("• Nalagam bazo ...")
    db_map = load_db_norm_map(args.db, opis_prefix=args.opis_prefix)  # samo 'mesto v %'
    print(f"  (baza ima {len(db_map)} unikatnih normaliziranih mest)")

    print("• Berem CSV ...")
    rows = read_csv(infile)
    print(f"  (vhodnih vrstic: {len(rows)})")

    rows_new = []
    rows_dup = []

    # tudi znotraj batcha ujemi dvojnike (če se isti city pojavi dvakrat v CSV)
    seen_in_batch = set()

    for r in rows:
        g = r["GESLO"].strip()
        o = r["OPIS"].strip()
        if not g:
            # prazne preskoči
            continue

        k = r["GESLO_NORM"].strip() or norm_key(g)

        # najprej batch-dup (isti key dvakrat v CSV)
        if k in seen_in_batch:
            rows_dup.append({
                "GESLO": g, "GESLO_NORM": k, "OPIS": o,
                "STATUS": "DUP_BATCH", "OBSTOJEČI_OPISI": "že v tem CSV"
            })
            continue
        seen_in_batch.add(k)

        # nato DB-dup: le če v bazi obstaja isto geslo med zapisi z OPIS, ki začne z 'mesto v '
        existing_opisi = db_map.get(k, [])
        if existing_opisi:
            rows_dup.append({
                "GESLO": g, "GESLO_NORM": k, "OPIS": o,
                "STATUS": "DUP_DB_MESTO", "OBSTOJEČI_OPISI": " | ".join(existing_opisi[:10])
            })
        else:
            rows_new.append({
                "GESLO": g, "GESLO_NORM": k, "OPIS": o,
                "STATUS": "NOVO", "OBSTOJEČI_OPISI": ""
            })

    # zapiši oba CSV
    write_csv(rows_new, out_new)
    write_csv(rows_dup, out_dup)

    print(f"✔ NOVO: {len(rows_new)} zapisov -> {out_new}")
    print(f"✔ DUPLIKATI: {len(rows_dup)} zapisov -> {out_dup}")

    # po želji takoj uvozi NOVO
    if args.apply and rows_new:
        n = apply_inserts(args.db, rows_new)
        print(f"✅ V bazo dodano: {n} zapisov.")
    elif args.apply:
        print("Ni ničesar za dodati (NOVO = 0).")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
