import os
import xml.etree.ElementTree as ET

def pretvori_in_ustvari(mapa, tezavnost, omeji_na=None):
    print(f"\n🔁 Obdelujem: {tezavnost}")
    datoteke = [f for f in os.listdir(mapa) if f.endswith(".xml") and f.startswith(f"Sudoku_{tezavnost}_")]
    datoteke.sort()
    if omeji_na:
        datoteke = datoteke[:omeji_na]

    st_uspesnih = 0

    for ime_datoteke in datoteke:
        print(f"🔄 {ime_datoteke}")
        xml_pot = os.path.join(mapa, ime_datoteke)
        js_pot = xml_pot.replace(".xml", ".js")
        datum = ime_datoteke.replace(f"Sudoku_{tezavnost}_", "").replace(".xml", "")
        html_pot = os.path.join(mapa, f"Sudoku_{tezavnost}_{datum}.html")

        try:
            tree = ET.parse(xml_pot)
            root = tree.getroot()
            celice = root.findall('.//{http://crossword.info/xml/rectangular-puzzle}cell')

            max_x = max(int(cell.attrib['x']) for cell in celice)
            max_y = max(int(cell.attrib['y']) for cell in celice)
            mreza = [[0 for _ in range(max_x)] for _ in range(max_y)]

            for cell in celice:
                x = int(cell.attrib['x']) - 1
                y = int(cell.attrib['y']) - 1
                vrednost = int(cell.attrib['solution'])
                mreza[y][x] = vrednost

            with open(js_pot, "w", encoding="utf-8") as f:
                f.write("var sudokuData = [\n")
                for row in mreza:
                    f.write("  [" + ", ".join(str(v) for v in row) + "],\n")
                f.write("];\n")

            with open(html_pot, "w", encoding="utf-8") as f:
                f.write(f"""<!DOCTYPE html>
<html lang="sl">
<head>
  <meta charset="UTF-8">
  <title>Sudoku - {datum}</title>
  <script src="/static/{tezavnost}/CrosswordCompilerApp/Sudoku_{tezavnost}_{datum}.js"></script>
  <style>
    body {{ font-family: sans-serif; text-align: center; margin-top: 20px; }}
    #sudoku-container {{ display: grid; grid-template-columns: repeat({max_x}, 40px); width: fit-content; margin: auto; }}
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
    sudokuData.forEach((row) => {{
      row.forEach((val) => {{
        const cell = document.createElement("div");
        cell.className = "cell";
        cell.textContent = val === 0 ? "" : val;
        container.appendChild(cell);
      }});
    }});
  </script>
</body>
</html>""")

            print(f"✅ OK: {os.path.basename(js_pot)}, {os.path.basename(html_pot)}")
            st_uspesnih += 1

        except Exception as e:
            print(f"❌ Napaka pri {ime_datoteke}: {e}")

    print(f"🎉 Uspešno obdelanih v {tezavnost}: {st_uspesnih}")

# 🔧 Težavnosti
tezavnosti = ["Sudoku_easy", "Sudoku_medium", "Sudoku_hard", "Sudoku_very_easy"]

for tezavnost in tezavnosti:
    mapa = os.path.join("../static", tezavnost, "CrosswordCompilerApp")
    if os.path.exists(mapa):
        pretvori_in_ustvari(mapa, tezavnost, omeji_na=None)
    else:
        print(f"⚠️ Mapa ne obstaja: {mapa}")
