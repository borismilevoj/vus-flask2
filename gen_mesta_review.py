# -*- coding: utf-8 -*-
"""
Pregled in priprava mest iz Wikidate za VUS.

Način preview:
    - potegne mesta za dano državo (wikidata QID) nad pragom populacije
    - shrani CSV: preview_<QID>_<offset>_<limit>.csv
    - izpiše prvih 10 vrstic za hiter pregled

Način apply:
    - prebere pre-view CSV
    - izdela dva izhoda:
        1) to_insert_<ime>.csv  -> predlogi za uvoz (unikatno po GESLO+OPIS)
        2) duplicates_<ime>.csv -> potencialni dvojniki (po GESLO+OPIS)

Ne piše v bazo, da se izognemo neznani shemi.
"""

import argparse
import csv
import sys
from typing import Dict, Any, List

import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

# ---------- HTTP session z Retry ----------

def _build_session() -> requests.Session:
    sess = requests.Session()
    retry = Retry(
        total=6,
        connect=3,
        read=3,
        backoff_factor=1.2,
        status_forcelist=(502, 503, 504),
        allowed_methods=("GET", "POST"),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry, pool_connections=10, pool_maxsize=10)
    sess.mount("https://", adapter)
    sess.mount("http://", adapter)
    sess.headers.update({
        "User-Agent": "VUS/1.0 (+kontakt: email@primer.si)",
        "Accept": "application/sparql-results+json"
    })
    return sess

SESSION = _build_session()

# ---------- SPARQL klic ----------

def wdqs(sparql: str, timeout: int = 60) -> Dict[str, Any]:
    r = SESSION.post(
        "https://query.wikidata.org/sparql",
        data={"query": sparql},
        headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        timeout=timeout
    )
    r.raise_for_status()
    return r.json()

# ---------- pomožne ----------

def to_text(v: Dict[str, Any]) -> str:
    return v["value"] if v and "value" in v else ""

def build_sparql(country_qid: str, min_pop: int, limit: int, offset: int, langs: str = "sl,it,en") -> str:
    # Q486972 = human settlement
    # P17 = country; P1082 = population
    # P131* = administrative territory path
    # Q13220204 = (drugi nivo – province/županije/okr.) – morda ne pokrije vseh držav, je pa uporaben filter
    # Q10864048 = (prvi nivo – regija/zvezna država ipd.)
    return f"""
SELECT ?city ?cityLabel ?provLabel ?regLabel WHERE {{
  ?city wdt:P31/wdt:P279* wd:Q486972 .
  ?city wdt:P17 wd:{country_qid} .
  ?city wdt:P1082 ?pop .
  FILTER(?pop > {min_pop})

  OPTIONAL {{
    ?city wdt:P131* ?prov .
    ?prov wdt:P31/wdt:P279* wd:Q13220204 .
    ?prov rdfs:label ?provLabel .
    FILTER(LANG(?provLabel) IN ("sl","it","en"))
  }}

  OPTIONAL {{
    ?city wdt:P131* ?reg .
    ?reg wdt:P31/wdt:P279* wd:Q10864048 .
    ?reg rdfs:label ?regLabel .
    FILTER(LANG(?regLabel) IN ("sl","it","en"))
  }}

  SERVICE wikibase:label {{
    bd:serviceParam wikibase:language "{langs}" .
  }}
}}
ORDER BY LCASE(?cityLabel)
LIMIT {int(limit)}
OFFSET {int(offset)}
""".strip()

def make_opis(mesto: str, prov: str, reg: str, drzava: str, word_province: str, word_region: str) -> str:
    parts: List[str] = [f"mesto v {drzava.lower()}"]
    # Po hierarhiji: regija (1. nivo), nato provinca/okraj (2. nivo)
    if reg:
        parts.append(f"{word_region} {reg}")
    if prov and prov.lower() != reg.lower():
        parts.append(f"{word_province} {prov}")
    return ", ".join(parts)

# ---------- Način PREVIEW ----------

def mode_preview(args: argparse.Namespace) -> int:
    sparql = build_sparql(
        country_qid=args.qid,
        min_pop=args.min,
        limit=args.page_size,
        offset=args.offset,
        langs=args.langs
    )
    try:
        data = wdqs(sparql, timeout=args.timeout)
    except requests.RequestException as e:
        print(f"Napaka pri WDQS: {e}")
        return 2

    rows = data.get("results", {}).get("bindings", [])
    outname = f"preview_{args.qid}_{args.offset}_{args.page_size}.csv"

    out_rows: List[Dict[str, str]] = []
    for r in rows:
        mesto = to_text(r.get("cityLabel")).strip()
        prov = to_text(r.get("provLabel")).strip()
        reg  = to_text(r.get("regLabel")).strip()
        qid  = to_text(r.get("city")).rpartition("/")[-1]  # zadnji del URL-ja

        opis = make_opis(
            mesto=mesto,
            prov=prov,
            reg=reg,
            drzava=args.country_name,
            word_province=args.word_province,
            word_region=args.word_region
        )
        geslo = mesto.upper()

        out_rows.append({
            "QID": qid,
            "MESTO": mesto,
            "PROVINCA": prov,
            "REGIJA": reg,
            "OPIS": opis,
            "GESLO": geslo,
            "DRŽAVA": args.country_name
        })

    # zapis
    with open(outname, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["QID", "MESTO", "PROVINCA", "REGIJA", "OPIS", "GESLO", "DRŽAVA"])
        w.writeheader()
        w.writerows(out_rows)

    print(f"\n✅ Shranjeno: {outname}  (vrstic: {len(out_rows)})\n")
    for i, r in enumerate(out_rows[:10], 1):
        print(f"{i:>2}. {r['GESLO']:<25} | {r['OPIS']}")
    if len(out_rows) > 10:
        print(f"... (+{len(out_rows)-10} vrstic)")
    return 0

# ---------- Način APPLY ----------

def mode_apply(args: argparse.Namespace) -> int:
    if not args.infile:
        print("Napaka: --infile manjka.")
        return 2

    try:
        with open(args.infile, encoding="utf-8") as f:
            rdr = csv.DictReader(f)
            rows = list(rdr)
    except OSError as e:
        print(f"Napaka pri branju {args.infile}: {e}")
        return 2

    seen = set()
    to_insert: List[Dict[str, str]] = []
    duplicates: List[Dict[str, str]] = []

    for r in rows:
        key = (r.get("GESLO", ""), r.get("OPIS", ""))
        if key in seen:
            duplicates.append(r)
        else:
            seen.add(key)
            to_insert.append(r)

    base = args.infile.rsplit(".", 1)[0]
    out_ok = f"{base}_to_insert.csv"
    out_dup = f"{base}_duplicates.csv"

    with open(out_ok, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(to_insert)

    with open(out_dup, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(duplicates)

    print(f"✅ Pripravljeno za uvoz: {out_ok} (vrstic: {len(to_insert)})")
    print(f"⚠️  Potencialni dvojniki: {out_dup} (vrstic: {len(duplicates)})")
    print("\nNamig: to_insert.csv lahko uvoziš v VUS, duplicates.csv pa pregledaš ročno.")
    return 0

# ---------- CLI ----------

def main() -> int:
    p = argparse.ArgumentParser(description="Wikidata mesta → pregled/CSV za VUS")
    p.add_argument("--mode", choices=["preview", "apply"], default="preview")
    p.add_argument("--qid", help="Wikidata QID države (npr. Q142 za Francijo, Q29 za Španijo)", default="Q38")
    p.add_argument("--country-name", help="Ime države v slovenščini (za opis)", default="Italiji")

    p.add_argument("--min", type=int, default=10000, help="Minimalna populacija (default 10000)")
    p.add_argument("--page-size", type=int, default=25, help="Število rezultatov na stran")
    p.add_argument("--offset", type=int, default=0, help="Odmik (za paginacijo)")
    p.add_argument("--langs", default="sl,it,en", help="Jeziki label (wikibase:language)")

    p.add_argument("--timeout", type=int, default=120, help="HTTP timeout za WDQS")

    # apply
    p.add_argument("--infile", help="CSV iz preview načina (za razcep v to_insert/duplicates)")

    # lokacijske besede
    p.add_argument("--word-province", default="provinca", help="Beseda za 2. nivo (npr. departma/okrug/županija/provinca)")
    p.add_argument("--word-region", default="regija", help="Beseda za 1. nivo (npr. regija/zvezna dežela)")

    args = p.parse_args()

    if args.mode == "preview":
        return mode_preview(args)
    else:
        return mode_apply(args)

if __name__ == "__main__":
    sys.exit(main())
