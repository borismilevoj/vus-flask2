# -*- coding: utf-8 -*-
"""
odstrani_generic.py
-------------------
Odstrani generične opise (npr. "mesto v Franciji") samo tam,
kjer pri istem geslu obstaja tudi bolj specifičen opis.

Primeri:
  # samo predogled (nič se ne briše)
  python scripts/odstrani_generic.py --generic "mesto v Franciji"

  # dejanski izbris + varnostna kopija
  python scripts/odstrani_generic.py --generic "mesto v Franciji" --apply

Parametri:
  --db         pot do SQLite baze (privzeto: VUS.db)
  --generic    generični opis, ki ga želiš čistiti
  --show       koliko primerov naj izpiše v predogledu (privzeto: 20)
  --apply      izvedi izbris (brez tega je samo predogled)
"""
import argparse
import os
import shutil
import sqlite3
from datetime import datetime
import sys
try:
    # Forsira UTF-8 izpis tudi v CP-1250 konzoli (Windows).
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass


def sql_norm(expr: str) -> str:
    """
    Vrne SQL izraz, ki normalizira opis:
    - odstrani zunanje presledke in pikice/vejice/podpičja
    - pretvori v lower()
    """
    # dvojni trim: trim(opis) in trim(..., '.,; ')
    return f"lower(trim(trim({expr}), '.,; '))"


def main():
    ap = argparse.ArgumentParser(description="Odstrani generične opise, če obstaja tudi specifičen.")
    ap.add_argument("--db", default="VUS.db", help="Pot do SQLite baze (privzeto: VUS.db)")
    ap.add_argument("--generic", required=True, help="Generični opis (npr. 'mesto v Franciji')")
    ap.add_argument("--show", type=int, default=20, help="Koliko primerov pokažem v predogledu")
    ap.add_argument("--apply", action="store_true", help="Izvedi izbris (sicer samo predogled)")
    args = ap.parse_args()

    if not os.path.exists(args.db):
        raise SystemExit(f"Ne najdem baze: {args.db}")

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    generic_norm = args.generic.strip().lower()

    # 1) Najdi vse GESLA, kjer imamo generik + vsaj en ne-generik
    #    (primerjava gre čez normaliziran opis)
    norm_opis = sql_norm("opis")
    sql_gesla = f"""
        SELECT DISTINCT s.geslo
        FROM slovar s
        WHERE {norm_opis} = ?
          AND EXISTS (
                SELECT 1 FROM slovar x
                WHERE x.geslo = s.geslo
                  AND {sql_norm('x.opis')} <> ?
          )
        ORDER BY s.geslo
    """
    cur.execute(sql_gesla, (generic_norm, generic_norm))
    gesla = [r["geslo"] for r in cur.fetchall()]

    print(f"Najdenih gesel za čiščenje (generic='{args.generic}'): {len(gesla)}")

    # 2) V predogledu pokaži nekaj primerov (katere opise ima geslo)
    if gesla:
        sql_opisi = "SELECT opis FROM slovar WHERE geslo = ? ORDER BY opis"
        for i, g in enumerate(gesla[: args.show], start=1):
            cur.execute(sql_opisi, (g,))
            opisi = [r["opis"] for r in cur.fetchall()]
            # izpiši generik + ostale, lepo ločeno
            generiki = [o for o in opisi if o.strip().lower() == args.generic.strip().lower()]
            ostali = [o for o in opisi if o.strip().lower() != args.generic.strip().lower()]
            prikaz = "  ||  ".join([*generiki, *ostali])
            print(f"- {g} => {prikaz}")

    if not args.apply:
        print("\n(Predogled) Nič ni bilo izbrisano. Za brisanje dodaj --apply.")
        conn.close()
        return

    # 3) Varnostna kopija baze
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("backups", exist_ok=True)
    backup_path = os.path.join("backups", f"VUS_backup_before_generic_{ts}.db")
    shutil.copyfile(args.db, backup_path)
    print(f"\n✔ Backup: {backup_path}")

    # 4) Dejanski izbris – odstrani samo generične opise (po norm primerjavi),
    #    kjer obstaja vsaj en drugi ne-generični opis pri istem geslu.
    delete_sql = f"""
        DELETE FROM slovar
        WHERE {norm_opis} = ?
          AND EXISTS (
                SELECT 1 FROM slovar x
                WHERE x.geslo = slovar.geslo
                  AND {sql_norm('x.opis')} <> ?
          )
    """
    cur.execute(delete_sql, (generic_norm, generic_norm))
    # koliko vrstic je izbrisal zadnji stavek
    cur.execute("SELECT changes()")
    deleted = cur.fetchone()[0]
    conn.commit()

    print(f"Izbrisanih zapisov: {deleted}")

    conn.close()


if __name__ == "__main__":
    main()
