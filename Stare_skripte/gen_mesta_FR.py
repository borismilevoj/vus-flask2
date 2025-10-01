# -*- coding: utf-8 -*-
import sqlite3, argparse, time
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

COUNTRY_QID = "Q142"  # France
COUNTRY_NAME_FALLBACK_SL = "Francija"
WORD_CITY = "mesto"
WORD_REGION = "regija"     # FR: regija
WORD_PROVINCE = "departma" # FR: département

# ----- Stabilna seja za WDQS (POST + retry) -----
SESSION = requests.Session()
retries = Retry(
    total=5,
    backoff_factor=1.0,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET", "POST"]
)
SESSION.mount("https://", HTTPAdapter(max_retries=retries))
HEADERS = {
    "User-Agent": "VUS/1.0 (kontakt: email@primer.si)",
    "Accept": "application/sparql-results+json"
}

def wdqs(sparql: str, timeout=60):
    r = SESSION.post(
        "https://query.wikidata.org/sparql",
        data={"query": sparql, "format": "json"},
        headers=HEADERS,
        timeout=timeout
    )
    r.raise_for_status()
    return r.json()

def build_sparql(min_pop: int, limit: int | None, offset: int | None) -> str:
    lim = f"\nLIMIT {int(limit)}" if limit else ""
    off = f"\nOFFSET {int(offset)}" if offset else ""
    return f"""
SELECT ?city ?cityLabel ?provLabel ?regLabel ?countryLabel WHERE {{
  # mesto (naselbina) v državi
  ?city wdt:P31/wdt:P279* wd:Q486972 .
  ?city wdt:P17 wd:{COUNTRY_QID} .
  ?city wdt:P1082 ?pop .
  FILTER(?pop > {int(min_pop)})

  # 2. nivo (npr. departma) – generično: "second-level administrative division" (Q13220204)
  OPTIONAL {{
    ?city wdt:P131* ?prov .
    ?prov wdt:P31/wdt:P279* wd:Q13220204 .
    ?prov rdfs:label ?provLabel .
    FILTER(LANG(?provLabel) IN ("sl","fr","en","es","it"))
  }}

  # 1. nivo (regija)
  OPTIONAL {{
    ?city wdt:P131* ?reg .
    ?reg wdt:P31/wdt:P279* wd:Q10864048 .
    ?reg rdfs:label ?regLabel .
    FILTER(LANG(?regLabel) IN ("sl","fr","en","es","it"))
  }}

  # ime države (za OPIS)
  wd:{COUNTRY_QID} rdfs:label ?countryLabel .
  FILTER(LANG(?countryLabel) IN ("sl","fr","en","es","it"))

  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "sl,fr,en,es,it". }}
}}
ORDER BY LCASE(?cityLabel){lim}{off}
""".strip()

def to_text(v):
    return v["value"] if v and "value" in v else None

def pick_best_label(*vals):
    # vzemi prvo ne-prazno
    for v in vals:
        if v: return v
    return None

def ensure_table(conn):
    # pričakujemo tabelo 'slovar' (GESLO, OPIS), kot v tvoji app
    pass

def exists(conn, geslo, opis):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM slovar WHERE GESLO=? AND OPIS=?", (geslo, opis))
    return cur.fetchone()[0] > 0

def insert(conn, geslo, opis):
    cur = conn.cursor()
    cur.execute("INSERT INTO slovar (GESLO, OPIS) VALUES (?, ?)", (geslo, opis))
    conn.commit()

def main():
    ap = argparse.ArgumentParser(description="Vstavi francoska mesta > min_pop v VUS.db (tabela slovar).")
    ap.add_argument("--db", default="VUS.db")
    ap.add_argument("--min", type=int, default=10000, help="Minimalna populacija (privzeto 10000)")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--offset", type=int, default=None)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    sparql = build_sparql(args.min, args.limit, args.offset)
    data = wdqs(sparql)

    conn = sqlite3.connect(args.db)
    # ensure_table(conn)  # če bi rabilo

    rows = data.get("results", {}).get("bindings", [])
    dodani = 0
    preskoceni = 0

    for b in rows:
        cityLabel = to_text(b.get("cityLabel"))
        provLabel = to_text(b.get("provLabel"))
        regLabel  = to_text(b.get("regLabel"))
        countryLabel = to_text(b.get("countryLabel"))

        # izberi najboljšo labelo za državo (sl -> fr -> en ...)
        country = pick_best_label(countryLabel, COUNTRY_NAME_FALLBACK_SL) or COUNTRY_NAME_FALLBACK_SL

        # zgradi OPIS (regija/provinca po potrebi)
        parts_mid = []
        if regLabel:  parts_mid.append(f"{WORD_REGION} {regLabel}")
        if provLabel: parts_mid.append(f"{WORD_PROVINCE} {provLabel}")
        middle = ", ".join(parts_mid) if parts_mid else None

        if middle:
            opis = f"{WORD_CITY} v {middle}, {country}"
        else:
            opis = f"{WORD_CITY} v {country}"

        # GESLO = ime mesta z velikimi črkami
        geslo = (cityLabel or "").upper().strip()
        if not geslo or not opis:
            continue

        if exists(conn, geslo, opis):
            preskoceni += 1
            continue

        if args.dry_run:
            print(f"[DRY] {geslo}\t{opis}")
        else:
            insert(conn, geslo, opis)
            dodani += 1

    conn.close()
    print(f"✅ Končano. Dodanih: {dodani}, že obstoječih (preskočenih): {preskoceni}, vse skupaj prebranih: {len(rows)}")

if __name__ == "__main__":
    main()
