import os
import shutil

# Nastavi težavnost: "easy", "medium", "hard", "very_easy"
tezavnost = "easy"

# Poti
uvozna_mapa = os.path.join("../static", "Sudoku_export")
ciljna_mapa = os.path.join("../static", f"Sudoku_{tezavnost}")
html_arhiv = os.path.join(os.path.expanduser("~"), "Desktop", "Sudoku_html_arhiv")

# Ustvari mapi, če še ne obstajata
os.makedirs(ciljna_mapa, exist_ok=True)
os.makedirs(html_arhiv, exist_ok=True)

# Premik .js in .html datotek
if os.path.exists(uvozna_mapa):
    for ime in os.listdir(uvozna_mapa):
        izvorna_pot = os.path.join(uvozna_mapa, ime)

        if ime.endswith(".js"):
            shutil.move(izvorna_pot, os.path.join(ciljna_mapa, ime))
            print(f"✅ Premaknjen JS: {ime}")

        elif ime.endswith(".html"):
            shutil.move(izvorna_pot, os.path.join(html_arhiv, ime))
            print(f"📥 HTML premaknjen na namizje: {ime}")

else:
    print("❌ Uvozna mapa ne obstaja.")
