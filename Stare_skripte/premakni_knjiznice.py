import os
import shutil

# Izhodiščna mapa znotraj projekta
BASE_PATH = os.path.join("../static", "Sudoku_easy", "CrosswordCompilerApp")
CILJNA_MAPA = os.path.join("../static", "CrosswordCompilerApp")

# Datoteke, ki jih bomo premaknili
DATOTEKE_ZA_PRENOS = ["jquery.js", "raphael.js", "crosswordCompiler.js"]

def premakni_knjiznice():
    if not os.path.exists(BASE_PATH):
        print(f"❌ Mapa ne obstaja: {BASE_PATH}")
        return

    if not os.path.exists(CILJNA_MAPA):
        os.makedirs(CILJNA_MAPA)
        print(f"📁 Ustvarjena mapa: {CILJNA_MAPA}")

    for datoteka in DATOTEKE_ZA_PRENOS:
        izvorna_pot = os.path.join(BASE_PATH, datoteka)
        ciljna_pot = os.path.join(CILJNA_MAPA, datoteka)

        if os.path.exists(izvorna_pot):
            shutil.move(izvorna_pot, ciljna_pot)
            print(f"✅ Premaknjeno: {datoteka}")
        else:
            print(f"⚠️ Datoteka ne obstaja: {izvorna_pot}")

    # Opcijsko: izbriši prazno mapo
    try:
        os.rmdir(BASE_PATH)
        print(f"🗑️ Izbrisana prazna mapa: {BASE_PATH}")
    except OSError:
        print(f"📁 Mapa {BASE_PATH} ni prazna ali je ni bilo mogoče izbrisati.")

if __name__ == "__main__":
    premakni_knjiznice()
