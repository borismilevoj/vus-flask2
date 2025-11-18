# app_safe.py  — VUS SAFE MODE (lokalno, brez DB, brez admina)
from __future__ import annotations
from flask import Flask, render_template, request
from pathlib import Path
from datetime import datetime, date
import os

app = Flask(__name__)

BASE_DIR  = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
CC_DIR    = STATIC_DIR / "Krizanke" / "CrosswordCompilerApp"
SUDOKU_ROOT = STATIC_DIR / "Sudoku"  # npr. Sudoku_easy

def _as_date(d_str: str | None) -> date:
    if not d_str:
        return date.today()
    for fmt in ("%Y-%m-%d", "%Y.%m.%d", "%d.%m.%Y"):
        try:
            return datetime.strptime(d_str, fmt).date()
        except ValueError:
            pass
    return date.today()

def _find_first(root: Path, patterns: list[str]) -> Path | None:
    for pat in patterns:
        hits = list(root.rglob(pat))
        if hits:
            return hits[0]
    return None

def _cc_find_assets(d: date) -> tuple[str | None, str | None]:
    if not CC_DIR.exists():
        return None, None
    ymd_dash   = d.strftime("%Y-%m-%d")
    ymd_nodash = d.strftime("%Y%m%d")
    js_patterns  = [f"*{ymd_dash}*.js",  f"*{ymd_nodash}*.js",  "*.js"]
    xml_patterns = [f"*{ymd_dash}*.xml", f"*{ymd_nodash}*.xml", "*.xml"]
    js_path  = _find_first(CC_DIR, js_patterns)
    xml_path = _find_first(CC_DIR, xml_patterns)

    def to_static_url(p: Path | None) -> str | None:
        if not p: return None
        rel = p.relative_to(STATIC_DIR).as_posix()
        return f"/static/{rel}"

    return to_static_url(js_path), to_static_url(xml_path)

@app.get("/")
def home():
    return (
        "<!doctype html><meta charset='utf-8'>"
        "<style>body{font-family:system-ui,Segoe UI,Arial;margin:2rem;line-height:1.5}</style>"
        "<h1>VUS – SAFE MODE (lokalno)</h1>"
        "<ul>"
        "<li><a href='/krizanka'>Današnja križanka</a> (lahko dodaš <code>?d=YYYY-MM-DD</code>)</li>"
        "<li><a href='/_routes'>/_routes</a></li>"
        "<li><a href='/healthz'>/healthz</a></li>"
        "</ul>"
    )

@app.get("/krizanka")
def krizanka():
    d = _as_date(request.args.get("d"))
    js_url, xml_url = _cc_find_assets(d)
    resolved = d.strftime("%Y-%m-%d")
    if js_url is None and xml_url is None:
        return (f"Ni najdenih .js/.xml za {resolved} v {CC_DIR.as_posix()}.", 404)
    try:
        return render_template("krizanka.html", js_url=js_url, xml_url=xml_url, datum=resolved, safe_mode=True)
    except Exception:
        parts = [
            "<!doctype html><meta charset='utf-8'>",
            f"<h1>Križanka – {resolved}</h1>"
        ]
        if js_url:
            parts += [f"<p>JS: <code>{js_url}</code></p>", f"<script src='{js_url}'></script>"]
        else:
            parts.append("<p><b>Manjka .js</b></p>")
        if xml_url:
            parts.append(f"<p>XML: <code>{xml_url}</code></p>")
        else:
            parts.append("<p><b>Manjka .xml</b></p>")
        parts.append("<p><a href='/'>← Domov</a></p>")
        return "\n".join(parts)

# --- minimalna /images (nikoli 500) ---
from pathlib import Path
from flask import send_file, Response

IMAGES_DIR = Path(app.root_path) / "static" / "images"   # skladno z ostalimi
ALLOWED_EXTS = {".jpg", ".jpeg", ".png", ".webp"}

@app.get("/images/<path:filename>", endpoint="images_serve")
def images_serve(filename: str):
    try:
        base = Path(filename)
        # 0) normaliziraj in prepreči ../
        target = (IMAGES_DIR / base).resolve()
        if not str(target).startswith(str(IMAGES_DIR.resolve())):
            return Response("", status=404)

        # 1) točno ime
        if target.is_file():
            return send_file(str(target), conditional=True)

        # 2) če ni končnice ali ne obstaja: prefix match (case-insensitive)
        stem = base.stem.lower()
        for p in IMAGES_DIR.rglob("*"):
            if not p.is_file():
                continue
            if p.suffix.lower() not in ALLOWED_EXTS:
                continue
            if p.stem.lower().startswith(stem):
                return send_file(str(p), conditional=True)

        # nič najdeno → tih 404
        return Response("", status=404)

    except Exception as e:
        print("[/images] ERROR:", e)
        return Response("", status=404)

from flask import render_template

@app.get("/preveri-sliko")
def preveri_sliko():
    return render_template("preveri_sliko.html")


@app.get("/sudoku/<tezavnost>/<datum>")
def sudoku(tezavnost: str, datum: str):
    dir_name = f"Sudoku_{tezavnost}".replace("-", "_")
    sud_dir = SUDOKU_ROOT.with_name(dir_name)

    try_dates = []
    try:
        d = _as_date(datum)
        try_dates = [d.strftime("%Y-%m-%d"), d.strftime("%Y%m%d")]
    except Exception:
        try_dates = [datum]

    for stem in try_dates:
        cand = sud_dir / f"{stem}.html"
        if cand.exists():
            rel = cand.relative_to(STATIC_DIR).as_posix()
            return (
                "<!doctype html><meta charset='utf-8'>"
                "<style>body,html{height:100%}body{margin:0;font-family:system-ui,Segoe UI,Arial}</style>"
                f"<iframe src='/static/{rel}' style='border:0;width:100%;height:100%'></iframe>"
            )

    return (f"Sudoku ni najden: {dir_name}/{datum}.html", 404)

@app.get("/healthz")
def healthz():
    return "ok-safe-local", 200

@app.get("/_routes")
def _routes():
    lines = []
    for r in app.url_map.iter_rules():
        methods = ",".join(sorted(m for m in r.methods if m in ("GET","POST","PUT","DELETE")))
        lines.append(f"[{methods or 'GET'}] {r.rule} -> '{r.endpoint}'")
    return "<pre>" + "\n".join(sorted(lines)) + "</pre>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="127.0.0.1", port=port, debug=False)
