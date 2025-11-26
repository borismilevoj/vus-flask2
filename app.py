# ===== app.py ================================================================
from __future__ import annotations

# --- Stdlib
import os
import io
import re
import sqlite3
import unicodedata
from datetime import date, datetime, timedelta
from functools import wraps
from pathlib import Path

# --- Flask
from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    flash,
    jsonify,
    send_from_directory,
    abort,
    session,
    current_app,
)

from werkzeug.utils import secure_filename

# --- Imaging
from PIL import Image

# --- Lokalni moduli
from krizanka import pridobi_podatke_iz_xml
from uvoz_cc_csv_vus import run as uvoz_cc_run

# --- .env (ne prepiše ročno nastavljenih env spremenljivk)
try:
    from dotenv import load_dotenv
    load_dotenv(override=False)
except Exception:
    pass



# ===== DB config (Path + opcijski URI) =======================================
VUS_DB_URL = (os.getenv("VUS_DB_URL") or "").strip()

def _resolve_db() -> tuple[Path, str | None]:
    """
    Vrne (DB_PATH kot Path, DB_URI kot 'file:...' ali None) — varno:
    - spoštuje VUS_DB_URL=file:... če datoteka obstaja
    - nato VUS_DB_PATH / DB_PATH, če obstaja
    - sicer prva izbira: ~/Documents/VUS/VUS.db
    - nikoli ne pusti projektne mape '.../vus-flask2/VUS.db' kot privzet
    """
    # 1) URL (file:)
    if VUS_DB_URL.startswith("file:"):
        raw = VUS_DB_URL[5:].split("?", 1)[0]
        p = Path(raw)
        if p.exists():
            return p, VUS_DB_URL
        else:
            print(f"[VUS][WARN] Ignoriram VUS_DB_URL (ne obstaja): {p}")

    # 2) PATH-varianti
    for k in ("VUS_DB_PATH", "DB_PATH"):
        v = (os.getenv(k) or "").strip()
        if v:
            p = Path(v)
            if p.exists():
                return p, None
            else:
                print(f"[VUS][WARN] Ignoriram {k} (ne obstaja): {p}")

    # 3) Fallback: vedno Documents\VUS\VUS.db
    fallback = Path.home() / "Documents" / "VUS" / "VUS.db"

    # 4) Guard: nikoli projektna pot kot default
    proj_dir = Path(__file__).resolve().parent
    proj_vusdb = proj_dir / "VUS.db"
    if proj_vusdb.exists():
        print(f"[VUS][WARN] Ignoriram projektni VUS.db: {proj_vusdb}")

    return fallback, None

DB_PATH, DB_URI = _resolve_db()
print(f"[VUS] DB_PATH = {DB_PATH} (exists={DB_PATH.exists()})")
if DB_URI:
    print(f"[VUS] DB_URI   = {DB_URI}")

def get_conn(readonly: bool = False) -> sqlite3.Connection:
    """Enotna SQLite povezava (RO/RW)."""
    if DB_URI:
        s, is_uri = DB_URI, True
    else:
        if readonly:
            s, is_uri = f"file:{DB_PATH.as_posix()}?mode=ro&cache=shared&immutable=1", True
        else:
            s, is_uri = str(DB_PATH), False
    con = sqlite3.connect(s, uri=is_uri, timeout=10.0, check_same_thread=False, isolation_level=None)
    con.execute("PRAGMA foreign_keys = ON;")
    con.execute("PRAGMA busy_timeout = 5000;")
    return con


# ===== Flask app =============================================================
app = Flask(__name__, static_folder="static", static_url_path="/static")
app.url_map.strict_slashes = False
app.secret_key = "boris-vus-krizanka-1234567890"
# ali katerikoli drug dolg string, samo da NI None/prazen

import re
import unicodedata
from pathlib import Path

ALLOWED_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def naredi_slug_iz_opisa(opis: str, dodatno: str = "") -> str:
    """
    Naredi slug iz besedila (opis + dodatno).
    Enaka logika kot v JS: brez šumnikov, max 15 besed, podčrtaji.
    """
    s = f"{opis or ''} {dodatno or ''}"

    # odstrani šumnike
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")

    # pomišljaje v presledke
    s = re.sub(r"[-–—−]", " ", s)

    # odstrani ločila
    s = re.sub(r"[().,;:!?]", "", s)

    s = s.lower()
    # dovoli samo črke, številke in presledke
    s = re.sub(r"[^a-z0-9\s]", "", s)

    # trim, razbij na besede, vzemi max 15 in poveži s podčrtaji
    parts = s.strip().split()
    parts = parts[:15]
    slug = "_".join(parts) if parts else "slika"

    return slug

# ===== Helpers ===============================================================

def login_required(f):
    @wraps(f)
    def _wrap(*a, **kw):
        # TODO: poveži na tvojo sejo/geslo, če želiš omejitve
        return f(*a, **kw)
    return _wrap


# ===== Home + favicon ========================================================
@app.get("/", endpoint="home")
def home():
    # base.html pričakuje 'home' – preusmeri na admin
    return redirect(url_for("admin"))

@app.route("/favicon.ico")
def favicon():
    # Začasno brez favicon (204)
    return ("", 204)


# ===== Minimalni legacy end-pointi (da predloge ne padijo) ===================
@app.get("/isci-vzorec", endpoint="isci_vzorec")
def _isci_vzorec_redirect():
    return redirect(url_for("admin"))

@app.get("/arhiv-krizanke", endpoint="arhiv_krizanke_legacy_redirect")
def _arhiv_krizanke_legacy_redirect():
    # stari URL samo preusmeri na pravi arhiv
    return redirect(url_for("arhiv_krizank"))



# ===== Diag: pregled vseh poti ===============================================
@app.get("/__routes__")
def __routes__():
    rows = []
    for rule in app.url_map.iter_rules():
        methods = ",".join(sorted(rule.methods - {"HEAD", "OPTIONS"}))
        rows.append(f"{rule.endpoint:35s} {methods:8s} {rule.rule}")
    rows.sort()
    return "<pre>" + "\n".join(rows) + "</pre>"


# ===== API: števec (COUNT slovar) ============================================
@app.get("/api/stevec", endpoint="api_stevec")
def api_stevec():
    try:
        dbp = DB_PATH.as_posix() if hasattr(DB_PATH, "as_posix") else str(DB_PATH)
        con = sqlite3.connect(f"file:{dbp}?mode=ro&cache=shared", uri=True, timeout=5.0, check_same_thread=False)
        n = int(con.execute("SELECT COUNT(*) FROM slovar;").fetchone()[0] or 0)
        con.close()
        return jsonify(ok=True, count=n)
    except Exception as e:
        return jsonify(ok=False, msg=str(e), count=0), 500


# ===== PREVERI GESLO (exact, NOCASE) + API alias =============================
@app.route("/preveri_geslo", methods=["GET", "POST"], endpoint="preveri_geslo")
def preveri_geslo():
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        q = data.get("geslo") or request.form.get("geslo") or ""
    else:
        q = request.args.get("geslo") or request.args.get("q") or ""
    q = (q or "").strip()
    if not q:
        return jsonify(ok=False, error="Manjka 'geslo'."), 400

    try:
        con = get_conn(readonly=True)

        # 1) preštej vse zadetke (case-insensitive)
        row = con.execute(
            "SELECT COUNT(*) FROM slovar WHERE geslo = ? COLLATE NOCASE;",
            (q,),
        ).fetchone()
        count = int(row[0] or 0)

        # 2) opcijsko pobereš še vse natančne zapise (če jih hočeš videt)
        rows = con.execute(
            "SELECT geslo FROM slovar WHERE geslo = ? COLLATE NOCASE;",
            (q,),
        ).fetchall()
        exact = [r[0] for r in rows]

        con.close()

        return jsonify(
            ok=True,
            exists=(count > 0),
            geslo=q,
            exact=exact,
            count=count,
        )
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@app.route("/api/preveri_geslo", methods=["GET", "POST"], endpoint="api_preveri_geslo")
def api_preveri_geslo():
    return preveri_geslo()

@app.get("/api/gesla_admin")
def api_gesla_admin():
    """
    Vrne vse vrstice iz tabele 'slovar' za dano geslo (NOCASE),
    skupaj z opisom/razlago, če ustrezen stolpec obstaja.
    """
    q = (request.args.get("geslo") or "").strip()
    if not q:
        return jsonify(ok=False, msg="Manjka 'geslo'."), 400

    con = get_conn(readonly=True)
    cur = con.cursor()

    # preberi stolpce v tabeli slovar
    cols_raw = list(cur.execute("PRAGMA table_info(slovar);"))
    name_map = { (row[1] or "").lower(): row[1] for row in cols_raw }

    # poskusi najti stolpec za opis/razlago (case-insensitive)
    desc_col = None
    for cand in ("opis", "razlaga", "opis_gesla", "clue"):
        if cand in name_map:
            desc_col = name_map[cand]
            break

    results = []

    if desc_col:
        sql = f"SELECT id, geslo, {desc_col} FROM slovar WHERE geslo = ? COLLATE NOCASE ORDER BY id;"
        rows = cur.execute(sql, (q,)).fetchall()
        for rid, g, desc in rows:
            results.append({
                "id": rid,
                "geslo": g,
                "razlaga": desc or "",
            })
    else:
        # fallback, če v tabeli sploh ni opisnega stolpca
        sql = "SELECT id, geslo FROM slovar WHERE geslo = ? COLLATE NOCASE ORDER BY id;"
        rows = cur.execute(sql, (q,)).fetchall()
        for rid, g in rows:
            results.append({
                "id": rid,
                "geslo": g,
                "razlaga": "",
            })

    con.close()

    return jsonify(ok=True, results=results)


@app.route("/api/preveri", methods=["GET", "POST"], endpoint="api_preveri_legacy")
def api_preveri_legacy():
    """
    Legacy endpoint, da stari frontend /api/preveri še vedno dela.
    Interno samo kliče preveri_geslo().
    """
    return preveri_geslo()


# ===== Admin: render (front kliče /api/stevec) ===============================
@app.get("/admin")
@login_required
def admin():
    return render_template("admin.html", DB_PATH=DB_PATH)

from pathlib import Path
from uvoz_cc_csv_vus import run as uvoz_cc_run

# baza projekta (kjer je app.py)
BASE_DIR = Path(__file__).resolve().parent

# CSV bo v mapi var/data/cc_clues_DISPLAY_UTF8.csv
CC_CSV_PATH = str(BASE_DIR / "var" / "data" / "cc_clues_DISPLAY_UTF8.csv")


# 1) GUMB: samo Citation vsebuje "vpis"
@app.post("/admin/uvoz_cc")
def admin_uvoz_cc():
    try:
        stats = uvoz_cc_run(
            csv_path=CC_CSV_PATH,
            db_path=str(DB_PATH),
            import_all=False,                 # NE ALL
            only_citation_contains="vpis",    # tukaj filtriramo
            verbose=False,
            dry_run=False,
        )
        msg = (
            f"Uvoz iz CC CSV (VPIS): "
            f"dodanih {stats['inserted']}, "
            f"posodobljenih {stats['updated']}, "
            f"preskočenih {stats['skipped']}."
        )
        flash(msg, "success")
    except Exception as e:
        flash(f"Napaka pri uvozu iz CC CSV (VPIS): {e}", "danger")

    return redirect(url_for("admin"))

# 2) GUMB: ALL – ignoriraj Citation, uvozi vse vrstice
@app.post("/admin/uvoz_cc_all")
def admin_uvoz_cc_all():
    try:
        stats = uvoz_cc_run(
            csv_path=CC_CSV_PATH,
            db_path=str(DB_PATH),
            import_all=True,                  # ALL
            only_citation_contains=None,      # zagotovo brez filtra
            verbose=False,
            dry_run=False,
        )
        msg = (
            f"Uvoz iz CC CSV (ALL): "
            f"dodanih {stats['inserted']}, "
            f"posodobljenih {stats['updated']}, "
            f"preskočenih {stats['skipped']}."
        )
        flash(msg, "warning")  # lahko 'success', dal sem 'warning' da veš da je BIG sync
    except Exception as e:
        flash(f"Napaka pri uvozu iz CC CSV (ALL): {e}", "danger")

    return redirect(url_for("admin"))

@app.get("/stevec_gesel")
def stevec_gesel():
    # odpri povezavo na bazo
    con = get_conn()          # uporabi tvojo helper funkcijo
    cur = con.cursor()
    # preštej zapise v glavni tabeli slovar
    cur.execute("SELECT COUNT(*) FROM slovar;")
    n = cur.fetchone()[0] or 0
    con.close()
    # vrni JSON, ki ga bere JS v adminu
    return jsonify({"count": int(n)})



# ===== Križanka po datumu (brez “skoka na danes”) ============================
CC_DIR = Path("static") / "Krizanke" / "CrosswordCompilerApp"

def _cc_paths(d: date) -> tuple[Path, Path]:
    """Vrne dejanske FS poti do .js in .xml za izbran datum (z mesečnimi mapami)."""
    ym = d.strftime("%Y-%m")        # npr. 2025-11
    ds = d.strftime("%Y-%m-%d")     # npr. 2025-11-19
    js_path  = CC_DIR / ym / f"{ds}.js"
    xml_path = CC_DIR / ym / f"{ds}.xml"
    return js_path, xml_path

def _cc_urls(d: date) -> tuple[str, str]:
    """Vrne URL-ja za statične .js in .xml (z mesečnimi mapami)."""
    ym = d.strftime("%Y-%m")
    ds = d.strftime("%Y-%m-%d")
    return (
        url_for("static", filename=f"Krizanke/CrosswordCompilerApp/{ym}/{ds}.js"),
        url_for("static", filename=f"Krizanke/CrosswordCompilerApp/{ym}/{ds}.xml"),
    )


from datetime import date, datetime, timedelta

@app.get("/krizanka")
def krizanka():
    d_str = request.args.get("d")
    if d_str:
        try:
            d = datetime.strptime(d_str, "%Y-%m-%d").date()
        except ValueError:
            abort(400, "Neveljaven datum")
    else:
        d = date.today()

    js_path, xml_path = _cc_paths(d)
    if not js_path.exists() or not xml_path.exists():
        abort(404, f"Za {d:%Y-%m-%d} ni .js/.xml v static\\Krizanke\\CrosswordCompilerApp.")

    js_url, xml_url = _cc_urls(d)

    cc = None
    try:
        cc = pridobi_podatke_iz_xml(xml_path)
    except Exception as e:
        print("[KRIZANKA] napaka pri branju XML:", e)
    print("[KRIZANKA CC]", type(cc), cc)

    # prejšnja / naslednja
    prev_url = url_for("krizanka", d=(d - timedelta(days=1)).strftime("%Y-%m-%d"))
    next_url = url_for("krizanka", d=(d + timedelta(days=1)).strftime("%Y-%m-%d"))
    back_url = url_for("krizanka", d=d.strftime("%Y-%m-%d"))

    session["krizanka_d"] = d.strftime("%Y-%m-%d")

    return render_template(
        "krizanka.html",
        datum=d,
        js_url=js_url,
        xml_url=xml_url,
        cc=cc,
        prev_url=prev_url,
        next_url=next_url,
        back_url=back_url,
    )

@app.get("/krizanka/<datum>")
def krizanka_alias(datum):
    # pričakujemo datum v obliki YYYY-MM-DD
    return redirect(url_for("krizanka", d=datum))


@app.get("/arhiv-krizank", endpoint="arhiv_krizank")
def arhiv_krizank():
    """
    Arhiv križank – bere vse *.js v static/Krizanke/CrosswordCompilerApp/** (tudi v podmapah YYYY-MM)
    in servira templatu arhiv.html (tip='krizanke').
    """
    root = Path(app.static_folder) / "Krizanke" / "CrosswordCompilerApp"

    datumi = []
    if root.exists():
        # rglob => pobere tudi iz podmap (2025-11/2025-11-25.js)
        for p in root.rglob("*.js"):
            stem = p.stem  # pričakujemo YYYY-MM-DD
            try:
                dt = datetime.strptime(stem, "%Y-%m-%d").date()
                datumi.append(dt)
            except ValueError:
                continue

    months_sorted, meseci = razbij_po_mesecih(datumi)

    return render_template(
        "arhiv.html",
        tip="krizanke",
        tezavnost=None,
        months_sorted=months_sorted,
        meseci=meseci,
    )


@app.get("/prikazi-krizanko", endpoint="prikazi_krizanko")
def prikazi_krizanko_route():
    # ponovno uporabi obstoječo logiko v krizanka()
    return krizanka()

def razbij_po_mesecih(datumi):
    """
    datumi: seznam datetime.date
    vrne (months_sorted, meseci),
    kjer je months_sorted npr. ["2025-11", "2025-10", ...],
    meseci pa dict: {"2025-11": ["2025-11-25", "2025-11-24", ...], ...}
    """
    meseci = {}
    for d in datumi:
        ym = d.strftime("%Y-%m")
        meseci.setdefault(ym, []).append(d.strftime("%Y-%m-%d"))

    # znotraj meseca novejši najprej
    for ym, lst in meseci.items():
        lst.sort(reverse=True)

    months_sorted = sorted(meseci.keys(), reverse=True)
    return months_sorted, meseci



@app.route("/images/<path:filename>")
def images_static(filename):
    """Servira slike za kartice z namigi iz static/Images/."""
    base = os.path.join(app.static_folder, "Images")
    return send_from_directory(base, filename)

from flask import render_template

@app.get("/preveri_sliko")
def preveri_sliko_page():
    # preusmeri star URL na novega
    return redirect(url_for("preveri_slika"))

def make_image_filename_from_opis(opis: str, dodatno: str = "") -> str:
    """
    Iz opisa + dodatnega niza (npr. 'Sagres') naredi ime slike:
    - vzamemo max 15 besed opisa
    - dodamo dodatno (če ni prazno)
    - odstranimo šumnike/naglas
    - vse nenumerične znake zamenjamo z '_'
    - spustimo v lower
    - dodamo '.jpg'
    """
    opis = (opis or "").strip()
    dodatno = (dodatno or "").strip()

    # 1) max 15 besed opisa
    words = opis.split()
    if len(words) > 15:
        words = words[:15]
    short_opis = " ".join(words)

    # 2) spojimo z dodatnim imenom (npr. Sagres)
    if dodatno:
        base = f"{short_opis} {dodatno}".strip()
    else:
        base = short_opis or dodatno

    if not base:
        base = "slika"

    # 3) odstrani šumnike/naglas (NFKD + izbrišemo 'combining' znake)
    base_norm = unicodedata.normalize("NFKD", base)
    base_norm = "".join(ch for ch in base_norm if not unicodedata.combining(ch))

    # 4) vse, kar ni črka ali cifra, zamenjamo z '_' in malo čistimo
    base_norm = re.sub(r"[^A-Za-z0-9]+", "_", base_norm)
    base_norm = re.sub(r"_+", "_", base_norm).strip("_").lower()

    if not base_norm:
        base_norm = "slika"

    return base_norm + ".jpg"

# --- nekje med routami ---
@app.get("/arhiv-sudoku", endpoint="arhiv_sudoku_pregled")
def arhiv_sudoku_pregled():
    """
    Arhiv sudoku – isti template arhiv.html, tip='sudoku'.
    Privzeta težavnost: 'easy' (lahko).
    Bere tudi iz podmap YYYY-MM.
    """
    tezavnost = "easy"  # če hočeš kaj drugega, zamenjaj

    folder_map = {
        "easy": "Sudoku_easy",
        "medium": "Sudoku_medium",
        "hard": "Sudoku_hard",
    }

    sub = folder_map[tezavnost]
    root = Path(app.static_folder) / sub

    datumi = []
    if root.exists():
        # IMPORTANT: rglob, da pobere tudi 2025-05/2025-05-01.js itd.
        for p in root.rglob("*.js"):
            stem = p.stem  # npr. 2025-05-01
            try:
                dt = datetime.strptime(stem, "%Y-%m-%d").date()
                datumi.append(dt)
            except ValueError:
                # če ni prav formatiran, ga ignoriramo
                continue

    months_sorted, meseci = razbij_po_mesecih(datumi)

    return render_template(
        "arhiv.html",
        tip="sudoku",
        tezavnost=tezavnost,
        months_sorted=months_sorted,
        meseci=meseci,
    )


@app.get("/sudoku/<tezavnost>/<datum>", endpoint="prikazi_sudoku")
def sudoku_page(tezavnost, datum):
    """
    Prikaz konkretnega sudokuja za dano težavnost in datum.
    Datoteke pričakujemo v:
      static/Sudoku_easy/2025-11-25.js
      static/Sudoku_medium/...
      static/Sudoku_hard/...
    """
    folder_map = {
        "easy": "Sudoku_easy",
        "medium": "Sudoku_medium",
        "hard": "Sudoku_hard",
    }

    sub = folder_map.get(tezavnost)
    if not sub:
        abort(404, "Neznana težavnost sudokuja")

    js_path = Path(app.static_folder) / sub / f"{datum}.js"
    if not js_path.exists():
        abort(404, f"Za {datum} ni sudokuja ({tezavnost}).")

    js_url = url_for("static", filename=f"{sub}/{datum}.js")

    return render_template(
        "sudoku.html",   # če imaš drugačno ime template-a, zamenjaj
        tezavnost=tezavnost,
        datum=datum,
        js_url=js_url,
    )

# ...

@app.get("/prispevaj", endpoint="prispevaj_geslo")
def prispevaj_geslo():
    # Za zdaj samo placeholder, da ne crkne
    return "Prispevaj geslo je trenutno začasno izklopljeno."
    # ali če hočeš:
    # return redirect(url_for("home"))


# ===== API: PREVERI-SLIKO ====================================================
IMAGE_DIR = Path("static") / "Krizanke" / "Slike"
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_FORMATS = {"JPEG", "PNG", "WEBP"}
MAX_SIZE_BYTES = 1_500_000                  # ~1.5 MB
MIN_W, MIN_H = 200, 200
MAX_W, MAX_H = 3000, 3000

def _open_image_bytes(raw: bytes):
    """Odpri sliko iz bajtov in preveri integriteto."""
    if not raw:
        return None, "Prazna datoteka."
    try:
        bio = io.BytesIO(raw)
        im = Image.open(bio)
        im.verify()          # hitro preverjanje korupcije
        bio.seek(0)
        im = Image.open(bio) # ponovno odpri za branje meta
        im.load()
        return im, None
    except Exception as e:
        return None, f"Slike ne morem prebrati: {e}"

def _check_constraints(im: Image.Image, size_bytes: int):
    w, h = im.size
    fmt = (im.format or "").upper()
    reasons = []
    ok = True

    if fmt not in ALLOWED_FORMATS:
        ok = False; reasons.append(f"Nedovoljen format: {fmt or 'neznan'} (dovoljeno: JPEG, PNG, WEBP).")
    if size_bytes > MAX_SIZE_BYTES:
        ok = False; reasons.append(f"Datoteka je prevelika: {size_bytes//1024} kB (max {MAX_SIZE_BYTES//1024} kB).")
    if w < MIN_W or h < MIN_H:
        ok = False; reasons.append(f"Slika je premajhna: {w}×{h}px (min {MIN_W}×{MIN_H}).")
    if w > MAX_W or h > MAX_H:
        reasons.append(f"Slika je zelo velika: {w}×{h}px (priporočilo max {MAX_W}×{MAX_H}).")

    return ok, reasons, fmt, w, h

def preveri_sliko(raw: bytes):
    """Glavna preverba – vrne (ok, reasons, meta)."""
    im, err = _open_image_bytes(raw)
    if err:
        return False, [err], {"format": None, "width": 0, "height": 0, "size_kb": len(raw)//1024}
    ok, reasons, fmt, w, h = _check_constraints(im, len(raw))
    meta = {"format": fmt, "width": w, "height": h, "size_kb": len(raw)//1024}
    return ok, reasons, meta

def _save_as_webp(im: Image.Image, basename: str) -> tuple[Path, str]:
    """Shrani WEBP (quality 85) v static/Krizanke/Slike/ in vrne (pot, static_url)."""
    basename = secure_filename(basename or "slika")
    out_path = IMAGE_DIR / f"{basename}.webp"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    im.save(out_path, format="WEBP", quality=85, method=6)
    static_rel = out_path.relative_to(Path("static")).as_posix()
    return out_path, url_for("static", filename=static_rel)

import unicodedata
import re
from werkzeug.utils import secure_filename

import unicodedata
import re
from werkzeug.utils import secure_filename

def make_image_basename_from_opis(opis: str, dodatno: str = "") -> str:
    """
    Generira osnovo imena slike na enak način kot JS v križanki:

    - opis (+ dodatno besedilo) -> tekst
    - vzamemo max 15 "besed"
    - odstranimo šumnike/naglas
    - vse v lower()
    - VSE, kar ni [a-z0-9], zamenjamo z '_'
    - stisnemo več '_' v enega, odrežemo z začetka/konca
    """

    import unicodedata
    import re

    # spojimo opis + dodatno (če je)
    text = " ".join(part for part in [(opis or "").strip(), (dodatno or "").strip()] if part).strip()
    if not text:
        return "slika"

    # max 15 "besed"
    words = text.split()
    words = words[:15]
    s = " ".join(words)

    # odstrani šumnike/naglas
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))

    # lower
    s = s.lower()

    # VSE, kar ni črka ali cifra -> '_'
    s = re.sub(r"[^a-z0-9]+", "_", s)

    # stisni več '_' v enega in odreži robove
    s = re.sub(r"_+", "_", s).strip("_")

    if not s:
        s = "slika"

    return s

@app.post("/api/brisi_geslo")
def api_brisi_geslo():
    """
    Briše geslo iz tabele 'slovar' po ID-ju.
    Pričakuje JSON ali form-data:
      - id  (ali pk, ali geslo_id)
    """
    data = request.get_json(silent=True) or request.form

    raw_id = data.get("id") or data.get("pk") or data.get("geslo_id")
    if not raw_id:
        return jsonify(ok=False, msg="Manjka 'id'."), 400

    try:
        geslo_id = int(raw_id)
    except ValueError:
        return jsonify(ok=False, msg="Neveljaven 'id' (ni številka)."), 400

    try:
        con = get_conn(readonly=False)
        cur = con.cursor()
        cur.execute("DELETE FROM slovar WHERE id = ?;", (geslo_id,))
        n = cur.rowcount
        con.commit()
        con.close()

        if n == 0:
            return jsonify(ok=False, msg=f"Geslo z id={geslo_id} ne obstaja."), 404
        return jsonify(ok=True, msg=f"Geslo z id={geslo_id} izbrisano.")
    except Exception as e:
        return jsonify(ok=False, msg=str(e)), 500

@app.post("/api/uredi_geslo")
def api_uredi_geslo():
    """
    Uredi geslo v tabeli 'slovar' po ID-ju.

    Pričakuje JSON ali form-data:
      - id
      - geslo      (novo geslo)
      - razlaga    (opis/razlaga; ime stolpca v bazi autodetekcija)
    """
    data = request.get_json(silent=True) or request.form

    raw_id = data.get("id") or data.get("pk") or data.get("geslo_id")
    novo_geslo = (data.get("geslo") or "").strip()
    nova_razlaga = (data.get("razlaga") or data.get("opis") or "").strip()

    if not raw_id:
        return jsonify(ok=False, msg="Manjka 'id'."), 400
    if not novo_geslo:
        return jsonify(ok=False, msg="Manjka novo geslo."), 400

    try:
        geslo_id = int(raw_id)
    except ValueError:
        return jsonify(ok=False, msg="Neveljaven id (ni številka)."), 400

    try:
        con = get_conn(readonly=False)
        cur = con.cursor()

        # preberi dejanske stolpce v tabeli slovar
        cols_raw = list(cur.execute("PRAGMA table_info(slovar);"))
        # npr. [(0, 'id', ...), (1, 'GESLO', ...), (2, 'OPIS', ...)]
        name_map = { (row[1] or "").lower(): row[1] for row in cols_raw }

        # poskusi najti stolpec za opis/razlago (case-insensitive)
        desc_col = None
        for cand in ("opis", "razlaga", "opis_gesla", "clue"):
            if cand in name_map:
                desc_col = name_map[cand]
                break

        if desc_col:
            # imamo stolpec za opis → posodobimo oba
            cur.execute(
                f"UPDATE slovar SET geslo = ?, {desc_col} = ? WHERE id = ?;",
                (novo_geslo, nova_razlaga, geslo_id),
            )
        else:
            # nimamo stolpca za opis → posodobimo samo geslo
            cur.execute(
                "UPDATE slovar SET geslo = ? WHERE id = ?;",
                (novo_geslo, geslo_id),
            )

        n = cur.rowcount
        con.commit()
        con.close()

        if n == 0:
            return jsonify(ok=False, msg=f"Geslo z id={geslo_id} ne obstaja."), 404

        return jsonify(
            ok=True,
            msg="Geslo posodobljeno.",
            geslo=novo_geslo,
            razlaga=nova_razlaga,
        )
    except Exception as e:
        return jsonify(ok=False, msg=str(e)), 500

@app.post("/api/dodaj_geslo")
def api_dodaj_geslo():
    data = request.get_json(silent=True) or request.form

    geslo = (data.get("geslo") or "").strip()
    if not geslo:
        return jsonify(ok=False, msg="Manjka 'geslo'."), 400

    opis  = (data.get("opis") or data.get("razlaga") or "").strip()
    vrsta = (data.get("vrsta") or "").strip()
    izvor = (data.get("izvor") or "").strip()
    tags  = (data.get("tags")  or "").strip()

    try:
        con = get_conn(readonly=False)
        cur = con.cursor()

        cols_raw = list(cur.execute("PRAGMA table_info(slovar);"))
        colnames = [row[1] for row in cols_raw]

        insert_cols = ["geslo"]
        params = [geslo]

        if "opis" in colnames:
            insert_cols.append("opis")
            params.append(opis)
        elif "razlaga" in colnames:
            insert_cols.append("razlaga")
            params.append(opis)

        if "vrsta" in colnames:
            insert_cols.append("vrsta")
            params.append(vrsta)

        if "izvor" in colnames:
            insert_cols.append("izvor")
            params.append(izvor)

        if "tags" in colnames:
            insert_cols.append("tags")
            params.append(tags)

        placeholders = ", ".join("?" for _ in insert_cols)
        sql = f"INSERT INTO slovar ({', '.join(insert_cols)}) VALUES ({placeholders});"
        cur.execute(sql, params)
        new_id = cur.lastrowid
        con.commit()
        con.close()

        return jsonify(ok=True, id=new_id, msg=f"Geslo '{geslo}' dodano.")
    except sqlite3.IntegrityError as e:
        return jsonify(ok=False, msg=f"Napaka (UNIQUE?): {e}"), 409
    except Exception as e:
        return jsonify(ok=False, msg=str(e)), 500



@app.get("/preveri_slika")
def preveri_slika():
    return render_template("preveri_sliko.html")

@app.post("/api/preveri_sliko")
def api_preveri_sliko():
    """
    Sprejme opis + dodatno ime (Sagres...), vrne:
    - predlagano ime datoteke (vključno s končnico)
    - ali slika obstaja
    - URL slike (če obstaja)
    Preveri več končnic: .jpg, .jpeg, .png, .webp
    """
    data = request.get_json() or request.form
    opis = (data.get("opis") or "").strip()
    dodatno = (data.get("dodatno") or "").strip()

    base_name = make_image_basename_from_opis(opis, dodatno)

    images_dir = os.path.join(app.static_folder, "Images")
    os.makedirs(images_dir, exist_ok=True)

    # katere končnice preverjamo
    exts = [".jpg", ".jpeg", ".png", ".webp"]

    found_filename = None
    found_url = None

    for ext in exts:
        candidate = base_name + ext
        full_path = os.path.join(images_dir, candidate)
        if os.path.exists(full_path):
            found_filename = candidate
            found_url = url_for("images_static", filename=candidate)
            break

    # če nismo našli nobene, predlagamo privzeto .jpg
    if found_filename is None:
        found_filename = base_name + ".jpg"

    exists = found_url is not None

    return jsonify({
        "filename": found_filename,  # to vključuje končnico
        "exists": exists,
        "url": found_url,
    })

@app.post("/api/upload_sliko")
def api_upload_sliko():
    """
    Upload slike v static/Images z izbranim imenom.

    Pričakuje:
    - form field 'file' (slika)
    - form field 'filename' (osnova ali ime, lahko z ali brez končnice)
    Končnico vzamemo iz uploadane datoteke, če je le-ta prisotna.
    """
    if "file" not in request.files:
        return jsonify({"ok": False, "error": "Manjka 'file'."}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"ok": False, "error": "Ni izbrane datoteke."}), 400

    requested = (request.form.get("filename") or "").strip()
    # razbij requested na osnovo + ext (če je)
    base_from_form, ext_from_form = os.path.splitext(requested)

    # ext iz dejanske datoteke (lahko .jpg/.png/...)
    _, ext_from_file = os.path.splitext(file.filename)

    # izberi končnico:
    # 1) če jo ima uploadana datoteka, vzamemo to
    # 2) sicer, če je bila v formi, vzamemo to
    # 3) fallback: .jpg
    if ext_from_file:
        final_ext = ext_from_file.lower()
    elif ext_from_form:
        final_ext = ext_from_form.lower()
    else:
        final_ext = ".jpg"

    # osnova imena: če je v formi prazna, naredimo generično
    if base_from_form:
        base = base_from_form
    else:
        base = "slika"

    base = secure_filename(base)
    if not base:
        base = "slika"

    filename = base + final_ext

    images_dir = os.path.join(app.static_folder, "Images")
    os.makedirs(images_dir, exist_ok=True)

    full_path = os.path.join(images_dir, filename)
    file.save(full_path)

    url = url_for("images_static", filename=filename)
    return jsonify({"ok": True, "filename": filename, "url": url})


# ===== Run ====================================================================
if __name__ == "__main__":
    # Na Windows/PyCharm včasih pomaga izklop reloaderja
    os.environ.pop("WERKZEUG_SERVER_FD", None)
    os.environ.pop("WERKZEUG_RUN_MAIN", None)
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
