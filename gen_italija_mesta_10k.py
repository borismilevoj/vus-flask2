# -*- coding: utf-8 -*-
# Zahteve: Python 3.10+, paketi: requests, pandas
# pip install requests pandas

import re
import requests
import pandas as pd
from pathlib import Path

OUT = Path("italija_mesta_10k.txt")

SPARQL = r"""
SELECT ?comune ?comuneLabel ?provLabel ?regLabel ?pop WHERE {
  # Comune v Italiji
  ?comune wdt:P31/wdt:P279* wd:Q747074 .       # instance of / subclass of "comune of Italy"
  ?comune wdt:P17 wd:Q38 .                     # v državi Italija
  ?comune wdt:P1082 ?pop .                     # populacija
  FILTER (?pop > 10000)

  # Pokrajina / metropolitansko mesto / libero consorzio (karkoli je na 2. nivoju)
  OPTIONAL {
    ?comune wdt:P131 ?parent .
    ?parent wdt:P31 ?parentType .
    FILTER (?parentType IN (
      wd:Q15060218,   # provincia italiana
      wd:Q15110,      # città metropolitana d'Italia
      wd:Q21190155    # libero consorzio comunale (Sicilia)
    ))
    BIND(STR(?parent) AS ?provUri)
    ?parent rdfs:label ?provLabel FILTER(LANG(?provLabel) = "it")
  }

  # Regija (3. nivo)
  OPTIONAL {
    ?comune wdt:P131* ?reg .
    ?reg wdt:P31 wd:Q16110 .                   # regione d'Italia
    ?reg rdfs:label ?regLabel FILTER(LANG(?regLabel) = "it")
  }

  SERVICE wikibase:label { bd:serviceParam wikibase:language "it,en". }
}
ORDER BY LCASE(?comuneLabel)
"""

def fetch_wikidata():
    url = "https://query.wikidata.org/sparql"
    headers = {
        "Accept": "application/sparql-results+json",
        "User-Agent": "VUS-Generator/1.0 (contact: user)"
    }
    r = requests.get(url, params={"query": SPARQL}, headers=headers, timeout=60)
    r.raise_for_status()
    data = r.json()["results"]["bindings"]
    rows = []
    for b in data:
        name = b["comuneLabel"]["value"]
        prov = b.get("provLabel", {}).get("value")
        reg  = b.get("regLabel", {}).get("value")
        pop  = int(float(b.get("pop", {}).get("value", "0")))
        rows.append((name, prov, reg, pop))
    return pd.DataFrame(rows, columns=["comune", "provincia_raw", "regija", "populacija"])

def clean_provincia(p):
    if not p:
        return None
    # Odstrani "città metropolitana di", "Provincia di", "Libero consorzio comunale di", ipd.
    p = re.sub(r"^(Città metropolitana|Citta metropolitana)\s+di\s+", "", p, flags=re.I)
    p = re.sub(r"^Provincia\s+(autonoma\s+di\s+|di\s+|del\s+|dell'\s+)", "", p, flags=re.I)
    p = re.sub(r"^Libero consorzio comunale\s+(di\s+|del\s+|della\s+)", "", p, flags=re.I)
    # Enotnosti: “Monza e della Brianza” naj ostane tako
    return p.strip()

def main():
    df = fetch_wikidata()

    # Očisti pokrajino
    df["pokrajina"] = df["provincia_raw"].apply(clean_provincia)

    # Če pokrajine ni dobil: pusti prazno (user lahko sam dopolni)
    # Podvojenim občinam se izognemo po imenu (Wikidata vrne unikatno, ampak just in case)
    df = df.sort_values(["comune"]).drop_duplicates(subset=["comune"], keep="first")

    # Sestavi vrstico v željeni obliki
    def line(row):
        ime = row["comune"].upper()
        reg = row["regija"] or ""
        prov = row["pokrajina"] or (row["provincia_raw"] or "").strip()
        if prov:
            return f"{ime} – mesto in pokrajina {prov} v regiji {reg}, Italija"
        else:
            # fallback brez pokrajine, če je res ni (redko)
            return f"{ime} – mesto v regiji {reg}, Italija"

    vrstice = [line(r) for _, r in df.iterrows()]

    # Shrani TXT
    OUT.write_text("\n".join(vrstice), encoding="utf-8")

    print(f"Zapisal: {OUT}  | vrstic: {len(vrstice)}  | primer:")
    print("\n".join(vrstice[:5]))

if __name__ == "__main__":
    main()
