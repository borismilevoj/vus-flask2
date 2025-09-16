# -*- coding: utf-8 -*-
"""
Zajem mest iz Wikidate po državi, z možnostjo filtra po populaciji in začetnici.
Zapiše CSV v obliki: GESLO, GESLO_NORM, OPIS

Primeri:
  # Francija (communes), min 15000, 25 rezultatov, začne z 'a'
  python gen_mesta_batch.py --qid Q142 --country-name "Francija" --country-in "Franciji" \
    --class-qid Q484170 --min 15000 --limit 25 --offset 0 --timeout 180 \
    --lang "fr,en,sl,it" --starts-with a --outfile mesta_FR_A_0_25.csv --show-sparql

Opombe:
- Če dobiš 0 rezultatov, najprej poskusi brez --starts-with.
- Če imaš CSV odprt v Excelu, boš dobil PermissionError – zapri Excel ali uporabi drugo ime datoteke (--outfile).
"""

import argparse
import csv
import re
import time
import unicodedata
import requests
from typing import List, Optional

WDQS_URL = "https://query.wikidata.org/sparql"

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "VUS/1.0 (contact: example@example.com)",
    "Accept": "application/sparql-results+json"
})


def normalize_geslo(label: str) -> str:
    """Normalizira ime za GESLO_NORM: odstrani diakritiko, zamenja '-' s presledkom,
    odstrani apostrofe, pobriše več presledkov in pretvori v UPPER."""
    # NFD in odstrani diakritiko
    s = unicodedata.normalize("NFD", label)
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    # '-' -> ' ', apostrofi stran
    s = s.replace("-", " ").replace("’", "").replace("'", "")
    # več presledkov -> 1
    s = re.sub(r"\s+", " ", s).strip()
    return s.upper()


def build_query(
        qid_country: str,
        class_qids: List[str],
        min_pop: int,
        limit: int,
        offset: int,
        starts_with: Optional[str],
        lang_chain: str
) -> str:
    """
    Zgradi SPARQL. Ključna točka: SERVICE wikibase:label mora biti PRED BIND/FILTER,
    ker FILTER deluje na ?cityLabel, ki ga doda SERVICE.
    """

    classes_part = ""
    if class_qids:
        classes_part = "VALUES ?cls { " + " ".join(f"wd:{c}" for c in class_qids) + " }"
    else:
        # fallback: human settlement
        classes_part = "VALUES ?cls { wd:Q486972 }"

    starts_filter = ""
    if starts_with:
        # primerjava na lowercased label (francoščina ima diakritiko, a 'achères' se še vedno začne z 'a')
        sw = starts_with.lower()
        starts_filter = f"""
  BIND(LCASE(STR(?cityLabel)) AS ?cityLabelLC)
  FILTER(STRSTARTS(?cityLabelLC, "{sw}"))
"""

    q = f"""
SELECT ?city ?cityLabel ?pop WHERE {{
  ?city wdt:P31/wdt:P279* ?cls .
  {classes_part}
  ?city wdt:P17 wd:{qid_country} .
  ?city wdt:P1082 ?pop .
  FILTER(?pop > {min_pop})

  SERVICE wikibase:label {{
    bd:serviceParam wikibase:language "{lang_chain}" .
  }}
  {starts_filter}
}}
ORDER BY LCASE(STR(?cityLabel))
LIMIT {limit}
OFFSET {offset}
"""
    return q.strip()


def wdqs_post(query: str, timeout: int = 180, max_retries: int = 5, backoff_s: float = 1.5) -> dict:
    """Pošlje poizvedbo na WDQS z retry/backoff zaradi 504/timeout-ov."""
    for attempt in range(1, max_retries + 1):
        try:
            r = SESSION.post(WDQS_URL, data={"query": query}, timeout=timeout)
            # 429/5xx -> retry
            if r.status_code >= 500 or r.status_code == 429:
                raise requests.HTTPError(f"{r.status_code} Server Error")
            r.raise_for_status()
            return r.json()
        except (requests.Timeout, requests.ConnectionError, requests.HTTPError) as e:
            if attempt == max_retries:
                raise
            time.sleep(backoff_s * attempt)
    raise RuntimeError("Nepričakovana napaka pri WDQS poizvedbi.")


def rows_from_result(data: dict) -> List[dict]:
    out = []
    for b in data.get("results", {}).get("bindings", []):
        city_label = b.get("cityLabel", {}).get("value", "").strip()
        pop = b.get("pop", {}).get("value")
        if not city_label:
            continue
        # GESLO: zamenjaj '-' s presledkom zaradi VUS konsistence
        geslo = city_label.replace("-", " ")
        geslo = re.sub(r"\s+", " ", geslo).strip()
        geslo_norm = normalize_geslo(city_label)
        out.append({
            "GESLO": geslo,
            "GESLO_NORM": geslo_norm,
            "POP": pop
        })
    return out


def write_csv(rows: List[dict], outfile: str, country_in: str):
    # OPIS = "mesto v {country_in}"
    with open(outfile, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["GESLO", "GESLO_NORM", "OPIS"])
        for r in rows:
            opis = f"mesto v {country_in}"
            w.writerow([r["GESLO"], r["GESLO_NORM"], opis])


def main():
    ap = argparse.ArgumentParser(description="Zajem mest iz Wikidate v CSV (za VUS)")
    ap.add_argument("--qid", required=True, help="QID države (npr. Q142 za Francijo)")
    ap.add_argument("--country-name", required=True, help="Ime države v imenovalniku (npr. 'Francija')")
    ap.add_argument("--country-in", default=None,
                    help="Ime države v mestniku/rodilniku (npr. 'Franciji'); če manjka, se vzame country-name + 'i'")
    ap.add_argument("--class-qid", action="append",
                    help="QID razredov (npr. Q484170 commune, Q486972 human settlement, Q515 city, Q3957 town). Lahko večkrat.")
    ap.add_argument("--min", type=int, default=10000, help="Minimalna populacija (privzeto 10000)")
    ap.add_argument("--limit", type=int, default=25, help="LIMIT")
    ap.add_argument("--offset", type=int, default=0, help="OFFSET")
    ap.add_argument("--timeout", type=int, default=180, help="WDQS timeout (sekunde)")
    ap.add_argument("--starts-with", default=None, help="Filtriraj po začetnici (npr. 'a')")
    ap.add_argument("--lang", default="fr,en,sl,it", help="Veriga jezikov za label (privzeto 'fr,en,sl,it')")
    ap.add_argument("--outfile", default=None, help="Ime izhodne CSV (privzeto: mesta_<qid>_<offset>_<limit>.csv)")
    ap.add_argument("--show-sparql", action="store_true", help="Izpiši SPARQL poizvedbo (debug)")

    args = ap.parse_args()

    country_in = args.country_in if args.country_in else (args.country_name + "i")

    outfile = args.outfile or f"mesta_{args.qid}_{args.offset}_{args.limit}.csv"

    query = build_query(
        qid_country=args.qid,
        class_qids=args.class_qid or ["Q484170"],  # privzeto communes
        min_pop=args.min,
        limit=args.limit,
        offset=args.offset,
        starts_with=args.starts_with,
        lang_chain=args.lang
    )

    if args.show_sparql:
        print("\n--- SPARQL ---\n", query, "\n--------------\n")

    try:
        data = wdqs_post(query, timeout=args.timeout)
    except Exception as e:
        print(f"Napaka WDQS: {e}")
        # vseeno napišemo prazen CSV, da ni polovičnega stanja
        write_csv([], outfile, country_in)
        print(f"✅ Shranjeno (prazno): {outfile}  (vrstic: 0)")
        return

    rows = rows_from_result(data)

    if not rows:
        print("Ni rezultatov (morda prevelik filter ali prag populacije).")
        write_csv([], outfile, country_in)
        print(f"✅ Shranjeno (prazno): {outfile}  (vrstic: 0)")
        return

    # odstrani dvojnike po GESLO_NORM, ohrani prvi vnos
    seen = set()
    dedup = []
    for r in rows:
        key = r["GESLO_NORM"]
        if key in seen:
            continue
        seen.add(key)
        dedup.append(r)

    write_csv(dedup, outfile, country_in)
    print(f"✅ Shranjeno: {outfile}  (vrstic: {len(dedup)})")
    # konzolni pregled
    for i, r in enumerate(dedup[:10], 1):
        print(f"{i:2}. {r['GESLO']:<28} | {r['GESLO_NORM']:<24} | mesto v {country_in}")
    if len(dedup) > 10:
        print(f"... (+{len(dedup) - 10} vrstic)")


if __name__ == "__main__":
    main()
