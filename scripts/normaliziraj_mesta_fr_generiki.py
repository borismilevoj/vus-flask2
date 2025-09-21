# scripts/normaliziraj_mesta_fr_generiki.py
import sqlite3, unicodedata, re, argparse, os, shutil

DB = "VUS.db"
TBL = "slovar"
GEN = "mesto v Franciji"

def normalize_geslo(s: str) -> str:
    # diakritika -> osnovne črke
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    # vezaj -> presledek
    s = s.replace("-", " ")
    # odstranimo apostrofe in ostalo ločilo
    s = re.sub(r"[^A-Za-z0-9 ]+", "", s)
    # več presledkov -> en
    s = re.sub(r"\s+", " ", s).strip()
    return s.upper()

def main(apply: bool):
    con = sqlite3.connect(DB)
    cur = con.cursor()

    # varnostna kopija (samo ob --apply)
    if apply:
        os.makedirs("backups", exist_ok=True)
        bak = f"backups/VUS_backup_norm_fr_{__import__('time').strftime('%Y%m%d_%H%M%S')}.db"
        shutil.copyfile(DB, bak)
        print(f"✅ Backup: {bak}")

    # potegnemo samo generike "mesto v Franciji"
    cur.execute(f"""
        SELECT rowid, geslo, opis
        FROM {TBL}
        WHERE lower(trim(trim(opis), '.,; '))=?
    """, (GEN.lower(),))
    rows = cur.fetchall()

    if not rows:
        print("Ni nič za normalizirati.")
        return

    updates = []
    deletes = []

    for rowid, geslo, opis in rows:
        new = normalize_geslo(geslo)
        if new == geslo:
            continue
        # ali po normalizaciji ta par že obstaja?
        cur.execute(f"SELECT rowid FROM {TBL} WHERE geslo=? AND opis=?", (new, opis))
        exists = cur.fetchone()
        if exists:
            # isti (geslo, opis) že obstaja -> tega starega lahko zbrišemo
            deletes.append(rowid)
        else:
            updates.append((new, rowid, geslo))

    print(f"Najdenih generikov: {len(rows)}")
    print(f"Za posodobit (rename GESLO): {len(updates)}")
    for new, rowid, old in updates:
        print(f"  {old}  ->  {new}")

    print(f"Za brisat zaradi dvojnika po normalizaciji: {len(deletes)}")

    if not apply:
        print("\n(Predogled) Nič ni bilo izvedeno. Za izvedbo dodaj --apply.")
        return

    # izvedba
    for new, rowid, old in updates:
        cur.execute(f"UPDATE {TBL} SET geslo=? WHERE rowid=?", (new, rowid))
    if deletes:
        cur.executemany(f"DELETE FROM {TBL} WHERE rowid=?", [(rid,) for rid in deletes])

    con.commit()
    # koliko dejanskih sprememb po mnenju SQLite
    cur.execute("SELECT changes()")
    print(f"\n✔ Sprememb (SQLite changes): {cur.fetchone()[0]}")
    con.close()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="izvedi spremembe (brez tega je samo predogled)")
    args = ap.parse_args()
    main(args.apply)
