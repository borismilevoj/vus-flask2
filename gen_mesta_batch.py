# -*- coding: utf-8 -*-
"""
Batch zajem mest iz Wikidate -> pregled CSV -> (po želji) vnos v VUS.db

Primeri zagona (PowerShell):
  # 1) Pregled (brez vnosa v bazo), Francija (Q142), prag 15k, po vseh črkah:
  python gen_mesta_batch.py --qid Q142 --country-name "Francija" --min 15000

  # 2) Samo po začetnicah A,B,C, z max 50/črko:
  python gen_mesta_batch.py --qid Q142 --country-name "Francija" --min 15000 --letters ABC --per-letter 50

  # 3) Pregled + takojšen vnos v bazo:
  python gen_mesta_batch.py --qid Q142 --country-name "Francija" --min 15000 --apply

  # 4) Španija (Q29), le črka A, večji timeout:
  python gen_mesta_batch.py --qid Q29 --country-name "Španija" --min 15000 --letters A --timeout 180

CSV izhod:
  - preview_batch_<QID>_<timestamp>.csv   -> kandidati za vnos (brez dvojnikov)
  - duplicates_batch_<QID>_<timestamp>.csv -> zapisi, ki v VUS že obstajajo (GESLO+OPIS)
"""

import argparse
import csv
import os
import re
import sqlite3
import sys
import time
import unicodedata
from datetime import datetime

import requests

WDQS_URL = "https://query.wikidata.org/sparql"


# -------- Normalizacija GESLA --------
def normalize_geslo(label: str) -> str:
    # odstrani diakritiko
    s = unicodedata.normalize("NFD", label)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    # odstrani pomišljaje/apostrofe
    s = s.replace("-", "").replace("–", "").replace("—", "").replace("-", "")
    s = s.replace("'", "").replace("’", "")
    # obdrži samo črke/številke in presledke
    s = re.sub(r"[^A-Za-z0-9 ]+", "", s)
    # odstrani presledke
    s = s.replace(" ", "")
    return s.upper().strip()


# -------- SPARQL poizvedba --------
def make_sparql(country_qid: str, min_pop: int, starts_with: str | None) -> str:
    # starts_with filter na cityLabel (sl,en,fr,it)
    starts_filter = ""
    if starts_with:
        starts = starts_with.lower()
        starts_filter = f'FILTER(STRSTARTS(LCASE(STR(?cityLabel)), "{starts}"))'

    return f"""
SELECT ?city ?cityLabel WHERE {{
  ?city wdt:P31/wdt:P279* wd:Q486972 .   # human settlement (tudi mesta, občine, ipd.)
  ?city wdt:P17 wd:{country_qid} .
  ?city wdt:P1082 ?pop .
  FILTER(?pop > {min_pop})
  {starts_filter}
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "sl,en,fr,it". }}
}}
ORDER BY LCASE(?cityLabel)
"""


# -------- WDQS klic z retry/backoff --------
def wdqs_request(query: str, timeout: int = 120, max_retries: int = 5) -> list[dict]:
    headers = {
        "Accept": "application/sparql-results+json",
        "User-Agent": "VUS/1.0 (contact: your-email@example.com)"
    }
    data = {"query": query}
    backoff = 5
    for attempt in range(1, max_retries + 1):
        try:
            r = requests.post(WDQS_URL, headers=headers, data=data, timeout=timeout)
            if r.status_code == 429:
                # preveč zahtev – spoštljivo počakaj
                wait = backoff * attempt
                print(f"WDQS 429 (Too Many Requests). Spim {wait}s ...")
                time.sleep(wait)
                continue
            r.raise_for_status()
            js = r.json()
            return js.get("results", {}).get("bindings", [])
        except requests.RequestException as e:
            wait = backoff * attempt
            print(f"WDQS napaka ({e}). Poskus {attempt}/{max_retries}. Spim {wait}s ...")
            time.sleep(wait)
    # če odpove:
    print("❌ WDQS: preveč napak/timeoutov, vračam prazen seznam.")
    return []


# -------- Branje obstoječih (za dvojnike) --------
def load_existing(db_path: str) -> set[tuple[str, str]]:
    if not os.path.exists(db_path):
        return set()
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # kombinacija GESLO (case-insensitive) + OPIS
    cur.execute("SELECT UPPER(GESLO), OPIS FROM slovar")
    rows = {(g, o) for (g, o) in cur.fetchall()}
    conn.close()
    return rows


# -------- Vnos v bazo --------
def insert_rows(db_path: str, rows: list[dict]) -> tuple[int, int]:
    if not rows:
        return (0, 0)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("CREATE INDEX IF NOT EXISTS idx_slovar_geslo_upper ON slovar(UPPER(GESLO))")
    added = 0
    skipped = 0
    for r in rows:
        g = r["GESLO"].strip()
        o = r["OPIS"].strip()
        cur.execute("SELECT 1 FROM slovar WHERE UPPER(GESLO)=UPPER(?) AND OPIS=?", (g, o))
        if cur.fetchone():
            skipped += 1
            continue
        cur.execute("INSERT INTO slovar (GESLO, OPIS) VALUES (?, ?)", (g, o))
        added += 1
    conn.commit()
    conn.close()
    return (added, skipped)


def main():
    ap = argparse.ArgumentParser(description="Batch zajem mest iz Wikidate -> CSV -> (opcijsko) VUS.db")
    ap.add_argument("--qid", required=True, help="QID države (npr. Q142 = Francija, Q29 = Španija, Q38 = Italija)")
    ap.add_argument("--country-name", required=True, help='Ime države za opis, npr. "Francija" -> "mesto v Francija"')
    ap.add_argument("--min", type=int, default=15000, help="Minimalna populacija (privzeto: 15000)")
    ap.add_argument("--letters", default="ABCDEFGHIJKLMNOPQRSTUVWXYZ", help="Začetnice (privzeto A..Z)")
    ap.add_argument("--per-letter", type=int, default=50,
                    help="Maks. število na črko (lokalno filtriranje po rezultatu)")
    ap.add_argument("--timeout", type=int, default=120, help="Timeout za WDQS (sekunde)")
    ap.add_argument("--db", default="VUS.db", help="Pot do baze VUS (privzeto VUS.db v trenutni mapi)")
    ap.add_argument("--apply", action="store_true", help="Po generiranju CSV takoj vpiši nove vnose v bazo")
    args = ap.parse_args()

    country_qid = args.qid.strip()
    country_name = args.country_name.strip()
    opis_template = f"mesto v {country_name}"

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_preview = f"preview_batch_{country_qid}_{ts}.csv"
    out_dupes = f"duplicates_batch_{country_qid}_{ts}.csv"

    existing = load_existing(args.db)
    candidates = []
    duplicates = []

    print(f"Država: {country_name} ({country_qid}) | min populacija: {args.min}")
    print(f"Začetnice: {args.letters} | timeout: {args.timeout}s | per-letter: {args.per_letter}")
    print("Začenjam prenos ...")

    for ch in args.letters:
        ch = ch.strip()
        if not ch:
            continue
        print(f"\n-- Črka: {ch} --")
        query = make_sparql(country_qid, args.min, ch.lower())
        bindings = wdqs_request(query, timeout=args.timeout, max_retries=6)

        # Pretvori v (NAZIV, GESLO, OPIS) in lokalno odreži na per-letter
        rows = []
        for b in bindings:
            label = b.get("cityLabel", {}).get("value", "").strip()
            if not label:
                continue
            geslo_norm = normalize_geslo(label)
            # filtriraj smeti (npr. delitve sektorjev ipd., če se prebijejo skozi)
            if not geslo_norm or len(geslo_norm) < 2:
                continue
            rows.append({
                "NAZIV": label,
                "GESLO": geslo_norm,
                "OPIS": opis_template
            })

        # lokalni limit po črki
        if args.per_letter and len(rows) > args.per_letter:
            rows = rows[:args.per_letter]

        print(f"Najdeno (po filtrih): {len(rows)}")

        # razdeli na nove / dvojnike
        for r in rows:
            key = (r["GESLO"].upper(), r["OPIS"])
            if key in existing:
                duplicates.append(r)
            else:
                candidates.append(r)

        print(f"   + novi kandidati: {sum(1 for r in rows if (r['GESLO'].upper(), r['OPIS']) not in existing)}")
        print(f"   = dvojniki:        {sum(1 for r in rows if (r['GESLO'].upper(), r['OPIS']) in existing)}")

        # Ne obremenjuj WDQS
        time.sleep(1.0)

    # Zapiši CSV-je
    def write_csv(path, rows):
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["NAZIV", "GESLO", "OPIS"])
            w.writeheader()
            w.writerows(rows)

    write_csv(out_preview, candidates)
    write_csv(out_dupes, duplicates)

    print(f"\n✅ Shranjeno: {out_preview}  (vrstic: {len(candidates)})")
    print(f"✅ Shranjeno: {out_dupes}    (vrstic: {len(duplicates)})")

    if args.apply:
        print("\n-- Vnos v bazo --")
        added, skipped = insert_rows(args.db, candidates)
        print(f"✔ Dodano: {added}, preskočeno (dvojnik): {skipped}")
        print("Končano.")
    else:
        print("\nNi bilo izbrano --apply, zato v bazo ni bilo nič vpisano.")
        print("Odpri preview CSV v Excelu, preglej, in nato (če želiš) zaženI z --apply.")
        print(
            f"Primer: python gen_mesta_batch.py --qid {country_qid} --country-name \"{country_name}\" --min {args.min} --apply")
        print("Opomba: dvojnike imaš posebej v duplicates CSV.")


if __name__ == "__main__":
    main()
