import os
import shutil

# Mapa, kjer ročno naložiš izvoz iz CC
uvozna_mapa = "static/Krizanke/CrosswordCompilerApp"

# Mapa, kamor shrani .html datoteke (namizje)
namizje_html_mapa = os.path.join(os.path.expanduser("~"), "Desktop", "CC_html_arhiv")

# Ustvari mapo za arhiv .html
os.makedirs(namizje_html_mapa, exist_ok=True)

# Premakni .html datoteke na namizje
for ime in os.listdir(uvozna_mapa):
    polna_pot = os.path.join(uvozna_mapa, ime)
    if ime.lower().endswith(".html"):
        shutil.move(polna_pot, os.path.join(namizje_html_mapa, ime))
        print(f"HTML premaknjen: {ime}")
