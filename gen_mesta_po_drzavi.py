# -*- coding: utf-8 -*-
# Zahteve: Python 3.10+, paketi: requests, pandas
# Namestitev: pip install requests pandas

import argparse
import re
from pathlib import Path

import pandas as pd
import requests

import time
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

SESSION = requests.Session()
retries = Retry(
    total=5,                 # do 5 poskusov
    backoff_factor=1.0,      # 1s, 2s, 4s, 8s …
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET", "POST"]
)
SESSION.mount("https://", HTTPAdapter(max_retries=retries))

HEADERS = {
    "User-Agent": "VUS/1.0 (kontakt: tvoj-email@primer.si)",
    "Accept": "application/sparql-results+json"
}

def wdqs(sparql: str, timeout=60):
    """Stabilen klic na Wikidata Query Service (POST + retry)."""
    r = SESSION.post(
        "https://query.wikidata.org/sparql",
        data={"query": sparql, "format": "json"},
        headers=HEADERS,
        timeout=timeout
    )
    r.raise_for_status()
    return r.json()


COUNTRY_NAME_TO_QID = {
    # Najpogostejše – lahko dodaš svoje
    "italija": "Q38",
    "slovenija": "Q215",
    "hrvaška": "Q224",
    "avstrija": "Q40",
    "nemčija": "Q183",
    "francija": "Q142",
    "španija": "Q29",
    "srbija": "Q403",
    "madžarska": "Q28",
    "švica": "Q39",
    "velika britanija": "Q145",
    "poljska": "Q36",
    "česka": "Q213",
}

SPARQL_TEMPLATE = r"""
SELECT ?city ?cityLabel ?provLabel ?regLabel WHERE {
  # 1) katerakoli naselbina (human settlement), v državi X, s populacijo > MIN
  ?city wdt:P31/wdt:P279* wd:Q486972 .
  ?city wdt:P17 wd:%(COUNTRY_QID)s .
  ?city wdt:P1082 ?pop .
  FILTER(?pop > %(MIN_POP)s)

  # 2) 2. nivo (provincia/županija/okrožje...) – poskusi ga najti na poti P131*
  OPTIONAL {
    ?city wdt:P131* ?prov .
    ?prov wdt:P31/wdt:P279* wd:Q13220204 .
    ?prov rdfs:label ?provLabel .
    FILTER(LANG(?provLabel) IN (%(LANGS)s))
  }

  # 3) 1. nivo (regija/zvezna dežela...) – poskusi najti
  OPTIONAL {
    ?city wdt:P131* ?reg .
    ?reg  wdt:P31/wdt:P279* wd:Q10864048 .
    ?reg  rdfs:label ?regLabel .
    FILTER(LANG(?regLabel) IN (%(LANGS)s))
  }

  SERVICE wikibase:label { bd:serviceParam wikibase:language %(LANG_CHAIN)s. }
}
ORDER BY LCASE(?cityLabel)
"""

def clean_label(txt: str | None) -> str | None:
    if not txt:
        return None
    t = txt.strip()
    # odstrani generične predpone (če se kje pojavijo v labelu)
    t = re.sub(r"^(Provincia|Province|Provincie|Okrožje|Županija)\s+(di|de|del|della|od)\s+", "", t, flags=re.I)
    t = re.sub(r"^(Città metropolitana|City of|Stadt)\s+(di|de|of)\s+", "", t, flags=re.I)
    return t.strip()

def run(country_qid: str, min_pop: int, lang_pref: str, outfile: Path, country_name_print: str,
        word_province: str, word_region: str):
    # pripravi SPARQL
    langs = ",".join(f'"{l.strip()}"' for l in lang_pref.split(","))
    lang_chain = '"' + ",".join(l.strip() for l in lang_pref.split(",")) + '"'

    query = SPARQL_TEMPLATE % {
        "COUNTRY_QID": country_qid,
        "MIN_POP": min_pop,
        "LANGS": langs,
        "LANG_CHAIN": lang_chain,
    }

    url = "https://query.wikidata.org/sparql"
    headers = {
        "Accept": "application/sparql-results+json",
        "User-Agent": "VUS-Generator/1.0 (contact: user)"
    }
    r = requests.get(url, params={"query": query}, headers=headers, timeout=120)
    r.raise_for_status()
    data = r.json()["results"]["bindings"]

    # v DataFrame
    rows = []
    for b in data:
        city = b["cityLabel"]["value"]
        prov = clean_label(b.get("provLabel", {}).get("value"))
        reg  = clean_label(b.get("regLabel", {}).get("value"))
        rows.append((city, prov, reg))
    df = pd.DataFrame(rows, columns=["city", "prov", "reg"])

    # odstrani dvojnike po imenu mesta (če bi jih bilo)
    df = df.drop_duplicates(subset=["city"]).sort_values("city")

    # sestavi vrstice v željeni obliki
    lines = []
    for _, row in df.iterrows():
        city_up = row["city"].upper()
        prov = row["prov"]
        reg  = row["reg"]

        if prov and reg:
            line = f"{city_up} – mesto in {word_province} {prov} v regiji {reg}, {country_name_print}"
        elif reg:
            line = f"{city_up} – mesto v regiji {reg}, {country_name_print}"
        elif prov:
            line = f"{city_up} – mesto v {word_province} {prov}, {country_name_print}"
        else:
            line = f"{city_up} – mesto v {country_name_print}"

        lines.append(line)

    outfile.write_text("\n".join(lines), encoding="utf-8")
    print(f"OK: {outfile}  |  {len(lines)} vrstic")

def main():
    ap = argparse.ArgumentParser(description="Generičen izvoz mest (>min_pop) za poljubno državo (Wikidata).")
    ap.add_argument("--country", help="Ime države (slovensko; npr. 'Italija', 'Nemčija').", default="Italija")
    ap.add_argument("--qid", help="Wikidata QID države (prednost pred --country), npr. Q38 za Italijo.")
    ap.add_argument("--min-pop", type=int, default=10000, help="Minimalna populacija (default: 10000)")
    ap.add_argument("--lang", default="sl,it,en", help="Jeziki label (prednostni vrstni red), default: sl,it,en")
    ap.add_argument("--outfile", default="mesta_izvoz.txt", help="Izhodni TXT (default: mesta_izvoz.txt)")
    ap.add_argument("--word-province", default="pokrajina",
                    help="Beseda za 2. nivo (default: 'pokrajina'; lahko npr. 'okrožje', 'županija')")
    ap.add_argument("--word-region", default="regiji",
                    help="Uporaba v stavku 'v regiji {REG}', default: 'regiji' (sklon)")

    args = ap.parse_args()

    # določi QID
    country_qid = args.qid
    country_key = (args.country or "").strip().lower()
    if not country_qid:
        country_qid = COUNTRY_NAME_TO_QID.get(country_key)
        if not country_qid:
            raise SystemExit("Ne poznam QID za to državo. Uporabi --qid (npr. --qid Q38 za Italijo).")

    # lep izpis imena države (za konec stavka)
    country_name_print = args.country if args.country else country_qid

    run(
        country_qid=country_qid,
        min_pop=args.min_pop,
        lang_pref=args.lang,
        outfile=Path(args.outfile),
        country_name_print=country_name_print,
        word_province=args.word_province,
        word_region=args.word_region,
    )

if __name__ == "__main__":
    main()

