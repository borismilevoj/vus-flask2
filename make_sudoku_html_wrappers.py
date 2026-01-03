from pathlib import Path

LIB_NAMES = {"jquery.js", "raphael.js", "crosswordCompiler.js"}

HTML_TEMPLATE = """<!doctype html>
<html lang="sl">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <style>
    html,body{{height:100%;margin:0;padding:0;}}
    /* CC zna risat v različne kontejnarje – damo več opcij */
    #puzzle,#crossword,#CrosswordPuzzle{{height:100vh;width:100%;}}
  </style>
</head>
<body>
  <div id="puzzle"></div>
  <div id="crossword"></div>
  <div id="CrosswordPuzzle"></div>

  <script src="CrosswordCompilerApp/jquery.js"></script>
  <script src="CrosswordCompilerApp/raphael.js"></script>
  <script src="CrosswordCompilerApp/crosswordCompiler.js"></script>

  <script src="{js_name}"></script>

  <script>
    (function () {{
      function tryInit() {{
        // Najpogostejši CC način
        if (typeof CrosswordPuzzleDataInit === "function") {{
          try {{ CrosswordPuzzleDataInit("puzzle"); return true; }} catch (e1) {{}}
          try {{ CrosswordPuzzleDataInit(); return true; }} catch (e2) {{}}
        }}

        // Fallbacki za druge CC verzije
        if (typeof CreatePuzzle === "function") {{
          try {{ CreatePuzzle("puzzle"); return true; }} catch (e1) {{}}
          try {{ CreatePuzzle(); return true; }} catch (e2) {{}}
        }}
        if (typeof createPuzzle === "function") {{
          try {{ createPuzzle("puzzle"); return true; }} catch (e1) {{}}
          try {{ createPuzzle(); return true; }} catch (e2) {{}}
        }}

        return false;
      }}

      function start() {{
        // sanity check: ali se je sudoku .js sploh naložil
        if (typeof CrosswordPuzzleData === "undefined") {{
          console.error("[CC wrapper] CrosswordPuzzleData ni definiran (sudoku .js se ni naložil?)");
        }}

        var ok = tryInit();
        if (!ok) {{
          console.error("[CC wrapper] Init ni uspel. Preveri console v iframe tabu (open wrapper html v nov tab).");
        }}
      }}

      if (document.readyState === "loading") {{
        document.addEventListener("DOMContentLoaded", start);
      }} else {{
        start();
      }}
    }})();
  </script>
</body>
</html>
"""


def ensure_wrappers(static_subdir: str, force: bool = False) -> int:
    root = Path("static") / static_subdir
    if not root.exists():
        print(f"[SKIP] Ne obstaja: {root}")
        return 0

    changed = 0
    for js in root.rglob("*.js"):
        if js.name in LIB_NAMES:
            continue

        html = js.with_suffix(".html")
        if html.exists() and not force:
            continue

        content = HTML_TEMPLATE.format(title=js.stem, js_name=js.name)
        html.write_text(content, encoding="utf-8")
        changed += 1

    action = "updated/created" if force else "created"
    print(f"[OK] {static_subdir}: {action} {changed} wrapper HTML")
    return changed


def main():
    total = 0
    # force=True prepiše obstoječe wrapperje (ker drugače ne posodobiš init logike)
    for sub in ["Sudoku_very_easy", "Sudoku_easy", "Sudoku_medium", "Sudoku_hard"]:
        total += ensure_wrappers(sub, force=True)
    print(f"\nDONE. Wrapper HTML updated/created total: {total}")


if __name__ == "__main__":
    main()
