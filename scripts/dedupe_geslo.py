import argparse
import sqlite3
import unicodedata
import re
from collections import defaultdict
from textwrap import shorten

DB_PATH = "VUS.db"
TBL = "slovar"


def strip_accents(s: str) -> str:
    return "".join(ch for ch in unicodedata.normalize("NFD", s) if unicodedata.category(ch) != "Mn")


def norm_exact(opis: str) -> str:
    # skoraj nič – le whitespace trim + lower
    return opis.strip().lower()


def norm_light(opis: str) -> str:
    # brez šumnikov, brez ločil, ohrani besede
    x = strip_accents(opis)
    x = x.lower()
    x = re.sub(r"[^\w\s]", " ", x)  # ven ločila
    x = re.sub(r"_", " ", x)
    x = re.sub(r"\s+", " ", x).strip()
    return x


def norm_strong(opis: str) -> str:
    # kot light + odstrani ( ... ) – ponavadi letnice ipd.
    x = re.sub(r"\([^)]*\)", " ", opis)  # ven oklepaji z vsebino
    x = strip_accents(x).lower()
    x = re.sub(r"[^\w\s]", " ", x)  # ven ločila
    x = re.sub(r"\s+", " ", x).strip()
    return x


NORMALIZERS = {
    "exact": norm_exact,
    "light": norm_light,
    "strong": norm_strong,
}


def fetch_rows(geslo: str):
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(f"SELECT id, geslo, opis FROM {TBL} WHERE UPPER(geslo)=UPPER(?) ORDER BY id", (geslo,))
    rows = cur.fetchall()
    con.close()
    return rows


def delete_ids(ids):
    if not ids:
        return 0
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    qmarks = ",".join("?" for _ in ids)
    cur.execute(f"DELETE FROM {TBL} WHERE id IN ({qmarks})", ids)
    affected = cur.rowcount
    con.commit()
    con.close()
    return affected


def main():
    ap = argparse.ArgumentParser(description="Preglej in (po želji) izbriši skoraj-dvojne opise za dano geslo.")
    ap.add_argument("--geslo", required=True, help="npr. TAYLOR")
    ap.add_argument("--key", choices=["exact", "light", "strong"], default="strong",
                    help="kako agresivno normalizirati opise (privzeto strong)")
    ap.add_argument("--interactive", action="store_true", help="interaktivno izberi ID-je za brisanje")
    ap.add_argument("--apply", action="store_true", help="dejansko izbriši (brez tega je suhi tek)")
    ap.add_argument("--show-all", action="store_true", help="najprej izpiši VSE zapise (za orientacijo)")
    args = ap.parse_args()

    rows = fetch_rows(args.geslo)
    print(f"Najdenih zapisov za geslo '{args.geslo}': {len(rows)}")

    if not rows:
        return

    if args.show_all:
        print("\n— Vsi zapisi —")
        for r in rows:
            print(f"  [{r['id']:>6}] {shorten(r['opis'], width=120, placeholder='…')}")
        print()

    normalizer = NORMALIZERS[args.key]
    groups = defaultdict(list)
    for r in rows:
        k = normalizer(r["opis"])
        groups[k].append(r)

    # Kandidati so le skupine z >1 elementom
    candidates = {k: v for k, v in groups.items() if len(v) > 1}

    if not candidates:
        print("Ni zaznanih 'skoraj dvojnikov' (po izbranem ključu normalizacije).")
        print("Namig: poskusi --key light ali --key exact, ali pa za drugo geslo.")
        return

    print(f"\nSkupin kandidatov: {len(candidates)} (normalizacija: {args.key})")
    to_delete = []

    for gi, (k, items) in enumerate(sorted(candidates.items(), key=lambda kv: len(kv[1]), reverse=True), start=1):
        print(f"\nSkupina #{gi} – velikost {len(items)} – ključ: {shorten(k, 100, placeholder='…')}")
        for r in items:
            print(f"  [{r['id']:>6}] {shorten(r['opis'], width=120, placeholder='…')}")

        if args.interactive:
            choice = input("Vnesi ID-je za brisanje (ločene z vejico) ali Enter za preskok: ").strip()
            if choice:
                try:
                    ids = [int(x) for x in re.split(r"[,\s]+", choice) if x.strip()]
                    to_delete.extend(ids)
                except ValueError:
                    print("⚠️ Neveljaven vnos. Preskakujem skupino.")
        else:
            # brez interakcije ne brišemo ničesar – samo predlagamo
            # (običajno bi pustili prvega kot 'keeper')
            pass

    # Povzetek
    uniq_ids = sorted(set(to_delete))
    if not uniq_ids:
        print("\nNi izbranih ID-jev za brisanje.")
        return

    print("\n— Povzetek za brisanje —")
    print(", ".join(str(i) for i in uniq_ids))

    if args.apply:
        affected = delete_ids(uniq_ids)
        print(f"✅ Izbrisanih {affected} zapisov.")
    else:
        print("Suhi tek. Za dejanski izbris dodaj --apply.")
        print("Namig: pred izbrisom imaš že backup – po potrebi obnovi datoteko VUS.db iz kopije.")


if __name__ == "__main__":
    main()
