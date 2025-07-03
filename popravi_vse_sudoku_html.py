import os
import re

seznam_map = ["Sudoku_very_easy", "Sudoku_easy", "Sudoku_medium", "Sudoku_hard"]
static_path = "static"

skripte = """
<script src="/static/{mapa}/CrosswordCompilerApp/jquery.js"></script>
<script src="/static/{mapa}/CrosswordCompilerApp/raphael.js"></script>
<script src="/static/{mapa}/CrosswordCompilerApp/crosswordCompiler.js"></script>
<script src="/static/{pot_do_js}"></script>
<script>
$(function(){{ $("#CrosswordCompilerPuz").CrosswordCompiler(CrosswordPuzzleData,null,    {{SUBMITMETHOD:"POST",SAVE   :   "",PROGRESS :  "" }} );}});
</script>
<div id="CrosswordCompilerPuz"></div>
"""

def popravi_html_poti(cesta, mapa, datum):
    # Izračunaj pot do .js glede na to, če je v arhivu ali ne
    if "/" in datum:
        parts = datum.split("/")
        mesec = parts[0]
        fname = parts[1]
        pot_do_js = f"{mapa}/{mesec}/{fname.replace('.html', '.js')}"
    else:
        pot_do_js = f"{mapa}/{datum.replace('.html', '.js')}"
    with open(cesta, encoding="utf-8") as f:
        html = f.read()
    # Pobriši VSE <script ...> ... </script>
    html = re.sub(r'<script[\s\S]*?</script>', '', html, flags=re.IGNORECASE)
    # Pobriši VSE golo JS klice $(function(){...}); kjerkoli (tudi izven <script>)
    html = re.sub(r'\$\(\s*function\s*\([^)]*\)\s*\{[\s\S]*?\}\s*\);', '', html, flags=re.MULTILINE)
    # Pobriši vse “Web page created by ...” ali “Software ... crossword-compiler.com” kjerkoli
    html = re.sub(
        r'<[^>]*>\s*(Web page created by|Software|Page created by)[^<]*crossword-compiler\.com.*?</[^>]+>',
        '', html, flags=re.IGNORECASE)
    html = re.sub(
        r'(Web page created by|Software|Page created by)[^<]*crossword-compiler\.com\.?',
        '', html, flags=re.IGNORECASE)
    # Pobriši prazne <span>, <div>, <footer>, <p>
    html = re.sub(r'<(span|div|footer|p)[^>]*>\s*</\1>', '', html)
    # Če obstaja <div id="CrosswordCompilerPuz"> – vstavi skripte pred njo
    if re.search(r'<div[^>]*id=["\']CrosswordCompilerPuz["\']', html, re.IGNORECASE):
        html = re.sub(r'(<div[^>]*id=["\']CrosswordCompilerPuz["\'])', skripte.format(
            mapa=mapa,
            pot_do_js=pot_do_js
        ) + r'\1', html, count=1, flags=re.IGNORECASE)
    elif re.search(r'<body[^>]*>', html, re.IGNORECASE):
        # Če <div id="CrosswordCompilerPuz"> NE obstaja, doda skripte in div takoj za <body>
        html = re.sub(r'(<body[^>]*>)', r'\1\n' + skripte.format(
            mapa=mapa,
            pot_do_js=pot_do_js
        ), html, count=1, flags=re.IGNORECASE)
    else:
        # Če je html popolnoma pokvarjen, dodaj na začetek
        html = skripte.format(mapa=mapa, pot_do_js=pot_do_js) + html

    with open(cesta, "w", encoding="utf-8") as f:
        f.write(html)
    print("Popravljeno:", cesta)

for mapa in seznam_map:
    base = os.path.join(static_path, mapa)
    for f in os.listdir(base):
        if f.endswith('.html'):
            cesta = os.path.join(base, f)
            popravi_html_poti(cesta, mapa, f)
    for podmapa in os.listdir(base):
        pmapa = os.path.join(base, podmapa)
        if os.path.isdir(pmapa) and re.match(r'\d{4}-\d{2}', podmapa):
            for f in os.listdir(pmapa):
                if f.endswith('.html'):
                    cesta = os.path.join(pmapa, f)
                    popravi_html_poti(cesta, mapa, f"{podmapa}/{f}")

print("Vse sudoku HTML datoteke so popravljene!")
