import os

MAPA = os.path.join("static", "Sudoku_easy")
STARI_DEL = "/static/Sudoku_easy/CrosswordCompilerApp/"
NOVA_POT = "/static/CrosswordCompilerApp/"

def popravi_html_poti():
    if not os.path.exists(MAPA):
        print(f"❌ Mapa ne obstaja: {MAPA}")
        return

    for ime_datoteke in os.listdir(MAPA):
        if ime_datoteke.endswith(".html"):
            pot = os.path.join(MAPA, ime_datoteke)

            with open(pot, "r", encoding="utf-8") as f:
                vsebina = f.read()

            if STARI_DEL in vsebina:
                # Shrani varnostno kopijo
                with open(pot + ".bak", "w", encoding="utf-8") as backup:
                    backup.write(vsebina)

                # Zamenjaj poti
                nova_vsebina = vsebina.replace(STARI_DEL, NOVA_POT)

                with open(pot, "w", encoding="utf-8") as f:
                    f.write(nova_vsebina)

                print(f"✅ Popravljeno: {ime_datoteke}")
            else:
                print(f"ℹ️ Brez sprememb: {ime_datoteke}")

if __name__ == "__main__":
    popravi_html_poti()
