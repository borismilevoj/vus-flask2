from pathlib import Path
from collections import Counter
from krizanka import pridobi_podatke_iz_xml

XML = Path("static/Krizanke/CrosswordCompilerApp/2025-11/2025-11-19.xml")
cc = pridobi_podatke_iz_xml(XML)

gesla = cc.get("gesla_opisi", [])  # pozor na ime ključa
print("width:", cc.get("width"))
print("height:", cc.get("height"))
print("opisov:", len(gesla))
print("crna:", len(cc.get("crna_polja", [])))
print("smeri:", Counter(g.get("smer") for g in gesla))
for g in gesla[:10]:
    print(g)
