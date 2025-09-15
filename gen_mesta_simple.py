# -*- coding: utf-8 -*-
import argparse, csv, sys, re, unicodedata
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

CLASS_MAP = {
    "Q142": "Q484170",   # France -> commune of France
    "Q29":  "Q2074737",  # Spain  -> municipality of Spain
    "Q38":  "Q747074",   # Italy  -> comune of Italy
}

def make_session():
    s = requests.Session()
    retry = Retry(
        total=10, connect=5, read=5,
        backoff_factor=1.5,
        status_forcelist=(502, 503, 504),
        allowed_methods=("GET", "POST"),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry, pool_connections=10, pool_maxsize=10)
    s.mount("https://", adapter); s.mount("http://", adapter)
    s.headers.update({
        "User-Agent": "VUS/1.0 (+kontakt: email@primer.si)",
        "Accept": "application/sparql-results+json"
    })
    return s

# --- NOVO: normalizacija za GESLO (brez diakritike, vezajev, apostrofov, presledkov) ---
def normalize_geslo(s: str) -> str:
    if not s:
        return ""
    s = unicodedata.normalize('NFD', s)
    s = ''.join(ch for ch in s if unicodedata.category(ch) != 'Mn')  # odstrani diakritiko
    s = s.replace("’", "'")  # poenoti tipograf. apostrof
    s = re.sub(r"[-'\s]+", "", s)  # odstrani -, ' in presledke
    return s.upper()

def run(country_qid, country_name, min_pop, limit, offset, timeout, class_qid=None, starts_with=None):
    class_qid = class_qid or CLASS_MAP.get(country_qid, "Q486972")

    starts_filter = ""
    if starts_with:
        starts_filter = f'FILTER(STRSTARTS(LCASE(?cityLabel), "{starts_with.lower()}"))'

    sparql = f"""
SELECT ?city ?cityLabel WHERE {{
  ?city wdt:P31/wdt:P279* wd:{class_qid} .
  ?city wdt:P17 wd:{country_qid} .
  ?city wdt:P1082 ?pop .
  FILTER(?pop > {int(min_pop)})
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "sl,fr,en,it,es". }}
  {starts_filter}
}}
ORDER BY LCASE(?cityLabel)
LIMIT {int(limit)}
OFFSET {int(offset)}
""".strip()

    sess = make_session()
    r = sess.post(
        "https://query.wikidata.org/sparql",
        data={"query": sparql},
        headers={"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"},
        timeout=timeout
    )
    r.raise_for_status()
    data = r.json().get("results", {}).get("bindings", [])

    rows = []
    for b in data:
        name = b.get("cityLabel", {}).get("value", "").strip()
        if not name:
            continue
        city_uri = b.get("city", {}).get("value", "")
        q = city_uri.rpartition("/")[-1]
        opis = f"mesto v {country_name}"
        geslo = normalize_geslo(name)   # <-- uporabljamo normalizirano GESLO
        rows.append({
            "QID": q,
            "MESTO": name,   # izvirno ime z akcenti naj ostane za pregled
            "GESLO": geslo,  # normalizirano za VUS
            "OPIS": opis,
            "DRŽAVA": country_name
        })

    out = f"preview_simple_{country_qid}_{offset}_{limit}.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["QID","MESTO","GESLO","OPIS","DRŽAVA"])
        w.writeheader(); w.writerows(rows)

    print(f"✅ Shranjeno: {out}  (vrstic: {len(rows)})")
    for i, r in enumerate(rows[:10], 1):
        print(f"{i:>2}. {r['MESTO']:<28} | {r['GESLO']:<22} | {r['OPIS']}")
    if len(rows) > 10:
        print(f"... (+{len(rows)-10} vrstic)")

def main():
    p = argparse.ArgumentParser("Lahek zajem občin (mesta) iz Wikidate")
    p.add_argument("--qid", required=True, help="QID države (Q142 Francija, Q29 Španija, Q38 Italija …)")
    p.add_argument("--country-name", required=True, help="Ime države v slovenščini v pravem sklonu (npr. 'Franciji')")
    p.add_argument("--min", type=int, default=15000, help="Minimalna populacija")
    p.add_argument("--limit", type=int, default=15)
    p.add_argument("--offset", type=int, default=0)
    p.add_argument("--timeout", type=int, default=240)
    p.add_argument("--class-qid", help="(Neobvezno) prepiši razred P31, če želiš kaj posebnega")
    p.add_argument("--starts-with", help="(Neobvezno) samo kraji, ki se začnejo na to črko (npr. 'a')")
    args = p.parse_args()

    try:
        run(
            country_qid=args.qid,
            country_name=args.country_name,
            min_pop=args.min,
            limit=args.limit,
            offset=args.offset,
            timeout=args.timeout,
            class_qid=args.class_qid,
            starts_with=args.starts_with,
        )
    except requests.RequestException as e:
        print(f"Napaka pri WDQS: {e}")
        return 2
    return 0

if __name__ == "__main__":
    sys.exit(main())
