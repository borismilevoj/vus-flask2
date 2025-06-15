import os

MAPA = os.path.join('static', 'Sudoku_easy')
STARI_DEL = "/static/Sudoku_easy/CrosswordCompilerApp/"
NOVA_POT = "/static/CrosswordCompilerApp/"

PREDLOGA_HTML = """<!DOCTYPE html>
<html lang="sl">
<head>
  <meta charset="UTF-8">
  <title>Sudoku - VUS</title>
  <script src="/static/Sudoku_easy/{ime_js}"></script>
  <style>
    body {{ font-family: sans-serif; text-align: center; margin-top: 20px; }}
    #sudoku-container {{ display: grid; grid-template-columns: repeat(9, 40px); width: fit-content; margin: auto; }}
    .cell {{
      width: 40px; height: 40px; border: 1px solid #999;
      font-size: 20px; text-align: center; line-height: 40px;
    }}
  </style>
</head>
<body>
  <h1>Sudoku - {datum}</h1>
  <div id="sudoku-container"></div>

  <script>
    const container = document.getElementById("sudoku-container");
    sudokuData.forEach((row, i) => {{
      row.forEach((val, j) => {{
        const cell = document.createElement("div");
        cell.className = "cell";
        cell.textContent = val === 0 ? "" : val;
        container.appendChild(cell);
      }});
    }});
  </script>
</body>
</html>
"""

def popravi_ali_ustvari():
    if not os.path.exists(MAPA):
        print(f"❌ Mapa ne obstaja: {MAPA}")
        return

    for ime_datoteke in os.listdir(MAPA):
        if ime_datoteke.endswith(".js") and ime_datoteke.startswith("Sudoku_easy_"):
            datum = ime_datoteke.replace("Sudoku_easy_", "").replace(".js", "")
            html_ime = f"Sudoku_easy_{datum}.html"
            pot_html = os.path.join(MAPA, html_ime)

            ustvarjeno = False
            popravljeno = False

            if not os.path.exists(pot_html):
                # Ustvari novo HTML datoteko iz predloge
                with open(pot_html, "w", encoding="utf-8") as f:
                    f.write(PREDLOGA_HTML.format(ime_js=ime_datoteke, datum=datum))
                print(f"🆕 Ustvarjeno: {html_ime}")
                ustvarjeno = True
            else:
                # Preveri obstoječo HTML vsebino
                with open(pot_html, "r", encoding="utf-8") as f:
                    vsebina = f.read()

                if STARI_DEL in vsebina:
                    # Popravi stare poti
                    with open(pot_html + ".bak", "w", encoding="utf-8") as b:
                        b.write(vsebina)
                    vsebina = vsebina.replace(STARI_DEL, NOVA_POT)
                    popravljeno = True

                if "<div id=\"sudoku-container\">" not in vsebina:
                    # Nadomesti z novo vsebino, ker ni prava Sudoku struktura
                    vsebina = PREDLOGA_HTML.format(ime_js=ime_datoteke, datum=datum)
                    popravljeno = True

                if popravljeno:
                    with open(pot_html, "w", encoding="utf-8") as f:
                        f.write(vsebina)
                    print(f"🔧 Popravljeno: {html_ime}")
                else:
                    print(f"✅ V redu: {html_ime}")

if __name__ == "__main__":
    popravi_ali_ustvari()
