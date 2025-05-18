import os

KOREN_STATIC = "static"
STARI_DEL = "/static/Sudoku_"
NOVA_POT = "/static/CrosswordCompilerApp/"

def popravi_vse_sudoku_html():
    for mapa in os.listdir(KOREN_STATIC):
        polna_mapa = os.path.join(KOREN_STATIC, mapa)

        # Obravnavaj samo mape, ki se začnejo s "Sudoku_"
        if os.path.isdir(polna_mapa) and mapa.startswith("Sudoku_"):
            print(f"\n🔍 Preverjam mapo: {polna_mapa}")
            for ime_datoteke in os.listdir(polna_mapa):
                if ime_datoteke.endswith(".html"):
                    pot = os.path.join(polna_mapa, ime_datoteke)

                    with open(pot, "r", encoding="utf-8") as f:
                        vsebina = f.read()

                    if f'{STARI_DEL}{mapa}/CrosswordCompilerApp/' in vsebina:
                        # Shrani varnostno kopijo
                        with open(pot + ".bak", "w", encoding="utf-8") as backup:
                            backup.write(vsebina)

                        nova_vsebina = vsebina.replace(
                            f'{STARI_DEL}{mapa}/CrosswordCompilerApp/',
                            NOVA_POT
                        )

                        with open(pot, "w", encoding="utf-8") as f:
                            f.write(nova_vsebina)

                        print(f"✅ Popravljeno: {ime_datoteke}")
                    else:
                        print(f"ℹ️ Brez sprememb: {ime_datoteke}")

if __name__ == "__main__":
    popravi_vse_sudoku_html()
