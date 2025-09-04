import os
import re

# ✅ dodan very_hard
seznam_map = ["Sudoku_very_easy", "Sudoku_easy", "Sudoku_medium", "Sudoku_hard", "Sudoku_very_hard"]
static_path = "static"

# ✅ ABSOLUTNE poti do CC knjižnic (brez {mapa}!)
def zgradi_blok_skript(pot_do_js: str) -> str:
    return f"""
<script src="/static/CrosswordCompilerApp/jquery.js"></script>
<script src="/static/CrosswordCompilerApp/raphael.js"></script>
<script src="/static/CrosswordCompilerApp/crosswordCompiler.js"></script>
<script src="/static/{pot_do_js}"></script>
<script>
$(function(){{
  $("#CrosswordCompilerPuz").CrosswordCompiler(
    CrosswordPuzzleData, null,
    {{ SUBMITMETHOD: "POST", SAVE: "", PROGRESS: "" }}
  );
}});
</script>
<div id="CrosswordCompilerPuz"></div>
""".lstrip()

def popravi_html_poti(cesta, mapa, datum):
    """
    cesta = pot do .html
    mapa  = npr. Sudoku_easy
    datum = 'Sudoku_easy_2025-09-04.html' ali '2025-09/Sudoku_easy_2025-09-04.html'
    """
    # izračunamo pot do pripadajočega .js
    if "/" in datum:
        mesec, fname = datum.split("/", 1)
        pot_do_js = f"{mapa}/{mesec}/{fname.replace('.html', '.js')}"
    else:
        pot_do_js = f"{mapa}/{datum.replace('.html', '.js')}"

    with open(cesta, encoding="utf-8", errors="ignore") as f:
        html = f.read()

    # pobriši VSE <script> ... </script> (pustimo čist canvas)
    html = re.sub(r'<script[\s\S]*?</script>', '', html, flags=re.IGNORECASE)

    # pobriši goli jQuery init, če je izven <script> (varnostno)
    html = re.sub(r'\$\(\s*function\s*\([^)]*\)\s*\{[\s\S]*?\}\s*\);', '', html, flags=re.MULTILINE)

    # odstrani “Web page created by … crossword-compiler.com”
    html = re.sub(
        r'<[^>]*>\s*(Web page created by|Software|Page created by)[^<]*crossword-compiler\.com.*?</[^>]+>',
        '', html, flags=re.IGNORECASE)
    html = re.sub(
        r'(Web page created by|Software|Page created by)[^<]*crossword-compiler\.com\.?',
        '', html, flags=re.IGNORECASE)

    # odstrani prazne elemente, ki ostanejo
    html = re.sub(r'<(span|div|footer|p)[^>]*>\s*</\1>', '', html)

    blok = zgradi_blok_skript(pot_do_js)

    # vstavimo naš blok pred obstoječi #CrosswordCompilerPuz ali tik za <body>
    if re.search(r'<div[^>]*id=["\']CrosswordCompilerPuz["\']', html, re.IGNORECASE):
        html = re.sub(r'(<div[^>]*id=["\']CrosswordCompilerPuz["\'])', blok + r'\1',
                      html, count=1, flags=re.IGNORECASE)
    elif re.search(r'<body[^>]*>', html, re.IGNORECASE):
        html = re.sub(r'(<body[^>]*>)', r'\1\n' + blok, html, count=1, flags=re.IGNORECASE)
    else:
        html = blok + html

    with open(cesta, "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ Popravljeno:", cesta)

# ---- glavna zanka po mapah ----
for mapa in seznam_map:
    base = os.path.join(static_path, mapa)
    if not os.path.isdir(base):
        continue

    # datoteke v korenu težavnosti
    for f in os.listdir(base):
        if f.endswith('.html'):
            cesta = os.path.join(base, f)
            popravi_html_poti(cesta, mapa, f)

    # datoteke v mesečnih podmapah YYYY-MM
    for podmapa in os.listdir(base):
        pmapa = os.path.join(base, podmapa)
        if os.path.isdir(pmapa) and re.match(r'^\d{4}-\d{2}$', podmapa):
            for f in os.listdir(pmapa):
                if f.endswith('.html'):
                    cesta = os.path.join(pmapa, f)
                    popravi_html_poti(cesta, mapa, f"{podmapa}/{f}")

print("🎯 Vse Sudoku HTML datoteke so popravljene.")
