import argparse, sqlite3, sys

def main():
    ap = argparse.ArgumentParser(description="Odstrani generične opise, če za isto geslo obstaja tudi bolj specifičen opis.")
    ap.add_argument("--db", default="VUS.db", help="pot do SQLite baze (privzeto VUS.db)")
    ap.add_argument("--generic", required=True, help='generični opis, npr. "mesto v Franciji"')
    ap.add_argument("--apply", action="store_true", help="če dodaš ta flag, bo dejansko brisalo (brez – je samo predogled)")
    ap.add_argument("--limit", type=int, default=50, help="koliko vrstic pokaže v predogledu")
    args = ap.parse_args()

    db = sqlite3.connect(args.db)
    db.row_factory = sqlite3.Row
    cur = db.cursor()

    gen = args.generic.strip().upper()

    # Predogled gesel, kjer je generični opis in hkrati obstaja še drugačen opis
    cur.execute("""
      SELECT a.geslo,
             GROUP_CONCAT(b.opis, '  ||  ') AS vsi_opisi
      FROM slovar a
      JOIN slovar b ON b.geslo = a.geslo
      WHERE UPPER(TRIM(a.opis)) = ?
        AND EXISTS (
          SELECT 1 FROM slovar c
          WHERE c.geslo = a.geslo
            AND UPPER(TRIM(c.opis)) <> ?
        )
      GROUP BY a.geslo
      ORDER BY a.geslo
    """, (gen, gen))
    rows = cur.fetchall()

    print(f"Najdenih gesel za čiščenje (generic='{args.generic}'): {len(rows)}")
    for r in rows[:args.limit]:
        print("-", r["geslo"], "=>", r["vsi_opisi"])

    if not args.apply:
        print("\n(Predogled) Nič ni bilo izbrisano. Za brisanje dodaj --apply.")
        return 0

    # Dejansko brisanje generičnih opisov
    cur.execute("""
      WITH tgt AS (
        SELECT a.id
        FROM slovar a
        WHERE UPPER(TRIM(a.opis)) = ?
          AND EXISTS (
            SELECT 1 FROM slovar b
            WHERE b.geslo = a.geslo
              AND UPPER(TRIM(b.opis)) <> ?
          )
      )
      DELETE FROM slovar WHERE id IN (SELECT id FROM tgt)
    """, (gen, gen))
    deleted = cur.rowcount
    db.commit()
    print(f"Izbrisanih zapisov: {deleted}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
