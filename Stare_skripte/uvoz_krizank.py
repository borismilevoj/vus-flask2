import os
import shutil

# Poti
osnova = os.path.join("../static", "Krizanke", "CrosswordCompilerApp")
uvozna_podmapa = os.path.join(osnova, "CrosswordCompilerApp")
html_arhiv = os.path.join(os.path.expanduser("~"), "Desktop", "CC_html_arhiv")

# Ustvari mapo za arhiv html (če še ne obstaja)
os.makedirs(html_arhiv, exist_ok=True)

# Premik .js, .xml in .html
if os.path.exists(uvozna_podmapa):
    for ime in os.listdir(uvozna_podmapa):
        izvorna_pot = os.path.join(uvozna_podmapa, ime)

        if ime.endswith(".js") or ime.endswith(".xml"):
            shutil.move(izvorna_pot, os.path.join(osnova, ime))
            print(f"✅ Premaknjeno v CrosswordCompilerApp: {ime}")

        elif ime.endswith(".html"):
            shutil.move(izvorna_pot, os.path.join(html_arhiv, ime))
            print(f"📥 HTML premaknjen na namizje: {ime}")

    # Poskusi zbrisati prazno mapo
    try:
        os.rmdir(uvozna_podmapa)
        print(f"🗑️ Izbrisana prazna mapa: {uvozna_podmapa}")
    except OSError:
        print(f"⚠️ Mapa {uvozna_podmapa} ni prazna.")
else:
    print("❌ Notranja mapa ne obstaja.")
