import os
import glob

def odstrani_cc_vrstico_iz_html(mapa_base="static"):
    stevec = 0
    for mapa in os.listdir(mapa_base):
        if mapa.startswith("Sudoku_"):
            polna_pot = os.path.join(mapa_base, mapa)
            html_datoteke = glob.glob(os.path.join(polna_pot, "*.html"))
            for datoteka in html_datoteke:
                with open(datoteka, 'r', encoding='utf-8', errors='ignore') as f:
                    vrstice = f.readlines()
                nove = [vr for vr in vrstice if "crossword-compiler.com" not in vr]
                if len(nove) < len(vrstice):
                    with open(datoteka, 'w', encoding='utf-8') as f:
                        f.writelines(nove)
                    print(f"✂️ Očiščeno: {datoteka}")
                    stevec += 1
    print(f"\n✅ Skupaj očiščenih datotek: {stevec}")

# Zaženi
odstrani_cc_vrstico_iz_html()
