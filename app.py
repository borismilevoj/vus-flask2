# ===== app.py ================================================================
from __future__ import annotations

# --- Stdlib
import io
import os
import re
import sqlite3
import threading
import traceback
import unicodedata
from datetime import date, datetime, timedelta
from functools import wraps
from pathlib import Path

# --- Flask / 3rd-party
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
from PIL import Image

# --- Lokalni moduli
from krizanka import pridobi_podatke_iz_xml
"from uvoz_cc_csv_vus import run as uvoz_cc_run"

# --- .env (ne prepiše ročno nastavljenih env spremenljivk)
try:
    from dotenv import load_dotenv
    load_dotenv(override=False)
except Exception:
    pass


# preprost global za status uvoza ALL
UVOZ_CC_ALL_STATUS = {
    "running": False,
    "last_msg": None,
    "last_error": None,
}

def normaliziraj_geslo(s: str) -> str:
    """
    Odstrani šumnike/naglase in posebne znake, da dobimo "čisto" osnovo
    za ime datoteke (npr. 'Müller čŠž' -> 'Muller cSz').
    """
    if not s:
        return ""
    # NFKD razbije črke z naglasi, encode/decode pobriše ne-ASCII
    s_norm = unicodedata.normalize("NFKD", s)
    s_ascii = s_norm.encode("ascii", "ignore").decode("ascii")
    return s_ascii



# ===== DB config (Path + opcijski URI) =======================================
VUS_DB_URL = (os.getenv("VUS_DB_URL") or "").strip()

# ===== DB config (Path + opcijski URI) =======================================
VUS_DB_URL = (os.getenv("VUS_DB_URL") or "").strip()

def _resolve_db() -> tuple[Path, str | None]:
    """
    Vrne (DB_PATH kot Path, DB_URI kot 'file:...' ali None) — varno in deterministično:
    - 1) VUS_DB_URL=file:... če datoteka obstaja
    - 2) VUS_DB_PATH / DB_PATH če obstaja
    - 3) projektna data/VUS.db (če obstaja)  <-- lokalni default za ta projekt
    - 4) projektna var/data/VUS.db (če obstaja)
    - 5) fallback: ~/Documents/VUS/VUS.db
    """

    proj_dir = Path(__file__).resolve().parent

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

    # 3) projektna data/VUS.db
    proj_data_db = proj_dir / "data" / "VUS.db"
    if proj_data_db.exists():
        return proj_data_db, None

    # 4) projektna var/data/VUS.db
    proj_var_db = proj_dir / "var" / "data" / "VUS.db"
    if proj_var_db.exists():
        return proj_var_db, None

    # 5) fallback: Documents\VUS\VUS.db
    fallback = Path.home() / "Documents" / "VUS" / "VUS.db"
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
            s, is_uri = f"file:{DB_PATH.resolve().as_posix()}?mode=ro&cache=shared&immutable=1", True
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

from pathlib import Path

# ... app = Flask(__name__) ...

COUNT_FILE = Path(app.root_path) / "data" / "count.txt"

def read_passwords_count():
    try:
        txt = COUNT_FILE.read_text(encoding="utf-8").strip()
        return int(txt.replace(".", "").replace(" ", ""))
    except Exception as e:
        print("COUNT_FILE problem:", COUNT_FILE, "exists=", COUNT_FILE.exists(), "err=", e)
        return None



ALLOWED_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}

import re
import unicodedata

MAX_IMAGE_WORDS = 30
# isto kot si imel od začetka


from pathlib import Path
import unicodedata, re

MAX_IMAGE_WORDS = 30  # <-- ena številka, enkrat

def naredi_slug_iz_opisa(opis: str, dodatno: str = "", max_words: int = MAX_IMAGE_WORDS) -> str:
    import unicodedata, re
    text = " ".join(part for part in [(opis or "").strip(), (dodatno or "").strip()] if part).strip()
    if not text:
        return "slika"

    words = text.split()[:max_words]
    s = " ".join(words)

    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "slika"

def make_image_filename_from_opis(opis: str, dodatno: str = "", ext: str = ".jpg") -> str:
    slug = naredi_slug_iz_opisa(opis, dodatno, max_words=MAX_IMAGE_WORDS)
    ext = (ext or ".jpg").lower()
    if not ext.startswith("."):
        ext = "." + ext
    return f"{slug}{ext}"



from pathlib import Path

IMAGE_EXTS = [".jpg", ".jpeg", ".png", ".webp"]

def _images_dir():
    # pomembno: Images z veliko I
    return Path(app.static_folder) / "Images"

def find_existing_image_filename(opis: str, dodatno: str = "", max_dupes: int = 9) -> str | None:
    """
    Vrne filename, ki dejansko obstaja v static/Images.
    Proba:
      - novo slug (npr. 30 besed)
      - Windows dupes: " (1)", " (2)", ...
      - fallback še na staro 15-besedno varianto (da starih slik ne razbije)
    """
    img_dir = _images_dir()
    if not img_dir.exists():
        return None

    # 1) najprej "nova" varianta (tvoja trenutna)
    base30 = make_image_filename_from_opis(opis, dodatno)  # pri tebi zdaj 30

    # 2) fallback: staro obnašanje 15 besed (če imaš ogromno slik narejeninaredi_slug_iz_opisah po starem)
    #    -> najlažje: začasno naredimo lokalno 15-besedno verzijo kar tukaj
    def base15_local(opis: str, dodatno: str = "") -> str:
        import unicodedata, re
        text = " ".join(part for part in [(opis or "").strip(), (dodatno or "").strip()] if part).strip()
        if not text:
            return "slika"
        words = text.split()[:15]
        s = " ".join(words)
        s = unicodedata.normalize("NFD", s)
        s = "".join(ch for ch in s if not unicodedata.combining(ch))
        s = s.lower()
        s = re.sub(r"[^a-z0-9]+", "_", s)
        s = re.sub(r"_+", "_", s).strip("_")
        return s or "slika"

    base15 = base15_local(opis, dodatno)

    # kandidati v pravem vrstnem redu
    bases = [base30]
    if base15 != base30:
        bases.append(base15)

    for base in bases:
        # a) exact (brez (1))
        for ext in IMAGE_EXTS:
            p = img_dir / f"{base}{ext}"
            if p.exists():
                return p.name

        # b) windows duplicate (1..max_dupes)
        for i in range(1, max_dupes + 1):
            for ext in IMAGE_EXTS:
                p = img_dir / f"{base} ({i}){ext}"
                if p.exists():
                    return p.name

    return None


# ===== Helpers ===============================================================

def login_required(f):
    @wraps(f)
    def _wrap(*a, **kw):
        # TODO: poveži na tvojo sejo/geslo, če želiš omejitve
        return f(*a, **kw)
    return _wrap


# ===== Home + favicon ========================================================
@app.get("/")
def home():
    passwords_count = read_passwords_count()
    return render_template("home.html", passwords_count=passwords_count)



@app.get("/home")
def home_alias():
    return redirect(url_for("home"))


@app.route("/favicon.ico")
def favicon():
    # Začasno brez favicon (204)
    return ("", 204)





# ===== ISKANJE PO VZORCU =====================================================
@app.get("/isci-vzorec", endpoint="isci_vzorec")
def isci_vzorec_page():
    return render_template("isci_vzorec.html")




@app.post("/isci_vzorec", endpoint="isci_vzorec_api")
def isci_vzorec_api():
    """
    API za iskanje po vzorcu.
    Pričakuje JSON: { vzorec, dolzina, dodatno }
    Vrne seznam: [{ GESLO: ..., OPIS: ... }, ...]
    Stolpce (GESLO/geslo, OPIS/Opis/razlaga...) zazna dinamično iz PRAGMA.
    """
    import sys, traceback, sqlite3

    try:
        data = request.get_json(silent=True) or {}

        vzorec = (data.get("vzorec") or "").strip().upper()
        try:
            dolzina = int(data.get("dolzina") or 0)
        except (TypeError, ValueError):
            dolzina = 0
        dodatno = (data.get("dodatno") or "").strip()

        # če ni ne vzorca ne dodatnega filtra, nima smisla iskati
        if not vzorec and not dodatno:
            return jsonify([])

        like = vzorec  # '_' je wildcard za en znak v LIKE

        con = get_conn(readonly=True)
        cur = con.cursor()
        table = "slovar_sortiran"

        db_list = cur.execute("PRAGMA database_list;").fetchall()
        print("DB LIST (isci_vzorec):", db_list, file=sys.stderr, flush=True)

        # še en “marker”, da 100% vidiš, da je del kode šel čez
        print("MARK: after PRAGMA database_list", file=sys.stderr, flush=True)

        # PRAGMA: preberi imena stolpcev v 'slovar'
        cols_raw = list(cur.execute(f"PRAGMA table_info({table});"))
        name_map = {(row[1] or "").lower(): row[1] for row in cols_raw}

        # stolpec za geslo (GESLO / geslo / word ...)
        geslo_col = None
        for cand in ("geslo", "word", "beseda"):
            if cand in name_map:
                geslo_col = name_map[cand]
                break
        if not geslo_col and cols_raw:
            # fallback: vzamemo drugi stolpec (po navadi je to GESLO)
            geslo_col = cols_raw[1][1]

        # stolpec za opis
        desc_col = None
        for cand in ("opis", "razlaga", "opis_gesla", "clue"):
            if cand in name_map:
                desc_col = name_map[cand]
                break

        if not geslo_col:
            con.close()
            return jsonify({
                "ok": False,
                "error": f"V tabeli '{table}' ne najdem stolpca za geslo.",
                "results": []
            }), 200

        # izraz, kjer ignoriramo presledke in delamo z UPPER(geslo)
        norm_geslo = f"REPLACE(UPPER({geslo_col}), ' ', '')"

        # Sestavimo SQL
        if desc_col:
            sql = f"""
                SELECT {geslo_col}, {desc_col}
                FROM {table}
                WHERE {norm_geslo} LIKE ?
            """

        else:
            sql = f"""
                SELECT {geslo_col}, ''
                FROM slovar_sortiran

                WHERE {norm_geslo} LIKE ?
            """

        params = [like]

        # filter po dolžini – štejejo samo črke (brez presledkov)
        if dolzina > 0:
            sql += f" AND LENGTH({norm_geslo}) = ?"
            params.append(dolzina)

        # dodatni filter po opisu ali geslu (klasičen LIKE, tu presledkov ne ignoriramo)
        if dodatno:
            if desc_col:
                sql += f" AND {desc_col} LIKE ? COLLATE NOCASE"
            else:
                sql += f" AND {geslo_col} LIKE ? COLLATE NOCASE"
            params.append(f"%{dodatno}%")

        if desc_col:
            has_dash = f"CASE WHEN instr({desc_col}, ' - ') > 0 THEN 0 ELSE 1 END"

            after_dash = f"""
            CASE
              WHEN instr({desc_col}, ' - ') > 0
              THEN substr({desc_col}, instr({desc_col}, ' - ') + 3)
              ELSE {desc_col}
            END
            """

            name_key = f"""
            CASE
              WHEN instr({after_dash}, '(') > 0
              THEN trim(substr({after_dash}, 1, instr({after_dash}, '(') - 1))
              ELSE trim({after_dash})
            END
            """

            sql += f"""
              ORDER BY
                {has_dash},                             -- najprej tisti z ' - '
                {name_key} COLLATE NOCASE,              -- potem po imenu
                {desc_col} COLLATE NOCASE,              -- stabilnost
                {geslo_col} COLLATE NOCASE
              LIMIT 500;
            """
        else:
            sql += f" ORDER BY {geslo_col} COLLATE NOCASE LIMIT 500;"

        # debug: izpiši SQL in parametre
        print("isci_vzorec_api SQL:", sql, "params:", params, file=sys.stderr)

        try:
            rows = cur.execute(sql, params).fetchall()
        except sqlite3.OperationalError as e:
            print("isci_vzorec_api SQL ERROR:", e, file=sys.stderr)
            traceback.print_exc()
            con.close()
            return jsonify({"ok": False, "error": str(e), "results": []}), 200

        con.close()

        results = [{"GESLO": r[0], "OPIS": (r[1] or "")} for r in rows]
        return jsonify(results)

    except Exception as e:
        print("isci_vzorec_api ERROR:", e, file=sys.stderr)
        traceback.print_exc()
        return jsonify({"ok": False, "error": str(e), "results": []}), 200


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


@app.get("/debug_slovar")
def debug_slovar():
    """
    Hiter test na Renderju: ali baza in tabela 'slovar' obstajata.
    """
    import sys, traceback, sqlite3

    try:
        con = get_conn(readonly=True)
        cur = con.cursor()
        cols = list(cur.execute("PRAGMA table_info(slovar);"))
        if not cols:
            con.close()
            return jsonify(ok=False, msg="Tabela 'slovar' ne obstaja ali je prazna PRAGMA."), 200

        try:
            row = cur.execute("SELECT COUNT(*) FROM slovar;").fetchone()
            n = int(row[0] or 0)
        except sqlite3.OperationalError as e:
            con.close()
            return jsonify(ok=False, msg=f"Napaka pri SELECT COUNT(*): {e}"), 200

        con.close()
        return jsonify(ok=True, count=n, msg="Tabela 'slovar' je dosegljiva."), 200

    except Exception as e:
        print("debug_slovar ERROR:", e, file=sys.stderr)
        traceback.print_exc()
        return jsonify(ok=False, msg=str(e)), 200



# ===== API: števec (COUNT slovar) ============================================
from pathlib import Path
import os

def _resolve_cc_clues_file() -> Path:
    # 1) Render override (najbolj ziher)
    envp = (os.getenv("CC_CLUES_PATH") or "").strip()
    if envp:
        return Path(envp)

    # 2) lokalno: projekt/out/cc_clues_UTF8.csv
    return Path(__file__).resolve().parent / "out" / "cc_clues_UTF8.csv"

def _count_nonempty_lines(p: Path) -> int:
    n = 0
    with p.open("rb") as f:
        for line in f:
            if line.strip():
                n += 1
    return n

@app.get("/api/stevec", endpoint="api_stevec")
def api_stevec():
    try:
        import os

        cc_path = (os.getenv("CC_CLUES_PATH") or "").strip()

        if not cc_path or not os.path.exists(cc_path):
            return jsonify(ok=False, msg="CC_CLUES_PATH ne obstaja", count=0), 500

        with open(cc_path, "r", encoding="utf-8", errors="ignore") as f:
            # -1 če ima CSV header
            n = sum(1 for _ in f) - 1

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

    # normalizacija: NBSP -> space, collapse spaces, in key brez presledkov
    q_norm = q.replace("\u00A0", " ")
    q_norm = " ".join(q_norm.split())
    q_compact = q_norm.replace(" ", "")

    try:
        con = get_conn(readonly=True)

        # 1) preštej vse zadetke (case-insensitive, ignorira presledke)
        row = con.execute(
            "SELECT COUNT(*) FROM slovar "
            "WHERE replace(geslo, ' ', '') = ?;",
            (q_compact,),
        ).fetchone()

        count = int(row[0] or 0)

        # 2) pobereš še vse zadetke (dejanski zapis gesla v bazi)
        rows = con.execute(
            "SELECT geslo FROM slovar "
            "WHERE replace(geslo, ' ', '') = ?;",
            (q_compact,),
        ).fetchall()

        exact = [r[0] for r in rows]

        con.close()

        return jsonify(
            ok=True,
            exists=(count > 0),
            geslo=q_norm,
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
    q = (request.args.get("geslo") or "").strip()
    if not q:
        return jsonify(ok=False, msg="Manjka 'geslo'."), 400

    # normalizacija: NBSP -> space, collapse spaces
    q_norm = q.replace("\u00A0", " ")
    q_norm = " ".join(q_norm.split())

    # kompakt brez presledkov (ZA SQL primerjavo brez lower())
    q_compact = q_norm.replace(" ", "")

    con = get_conn(readonly=True)
    cur = con.cursor()

    cols_raw = list(cur.execute("PRAGMA table_info(slovar);"))
    name_map = {(row[1] or "").lower(): row[1] for row in cols_raw}

    desc_col = None
    for cand in ("opis", "razlaga", "opis_gesla", "clue"):
        if cand in name_map:
            desc_col = name_map[cand]
            break

    results = []

    if desc_col:
        sql = f"""
            SELECT id, geslo, {desc_col}
            FROM slovar
            WHERE replace(geslo, ' ', '') = ?
            ORDER BY id;
        """
        rows = cur.execute(sql, (q_compact,)).fetchall()
        for rid, g, desc in rows:
            results.append({"id": rid, "geslo": g, "razlaga": desc or ""})
    else:
        sql = """
            SELECT id, geslo
            FROM slovar
            WHERE replace(geslo, ' ', '') = ?
            ORDER BY id;
        """
        rows = cur.execute(sql, (q_compact,)).fetchall()
        for rid, g in rows:
            results.append({"id": rid, "geslo": g, "razlaga": ""})

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
"from uvoz_cc_csv_vus import run as uvoz_cc_run"

BASE_DIR = Path(__file__).resolve().parent

# CSV je zdaj v root/data/cc_clues_DISPLAY_UTF8.csv
CC_CSV_PATH = str(BASE_DIR / "data" / "cc_clues_DISPLAY_UTF8.csv")


# # 1) GUMB: samo Citation vsebuje "vpis"
# @app.post("/admin/uvoz_cc")
# def admin_uvoz_cc():
#     try:
#         stats = uvoz_cc_run(
#             csv_path=CC_CSV_PATH,
#             db_path=str(DB_PATH),
#             import_all=False,                 # NE ALL
#             only_citation_contains="vpis",    # tukaj filtriramo
#             verbose=False,
#             dry_run=False,
#         )
#         msg = (
#             f"Uvoz iz CC CSV (VPIS): "
#             f"dodanih {stats['inserted']}, "
#             f"posodobljenih {stats['updated']}, "
#             f"preskočenih {stats['skipped']}."
#         )
#         flash(msg, "success")
#     except Exception as e:
#         flash(f"Napaka pri uvozu iz CC CSV (VPIS): {e}", "danger")

#     return redirect(url_for("admin"))


# def _run_uvoz_cc_all_bg():
#     """Teče v ozadju (thread) – uvoz ALL iz CC_CSV_PATH."""
#     global UVOZ_CC_ALL_STATUS
#     UVOZ_CC_ALL_STATUS["running"] = True
#     UVOZ_CC_ALL_STATUS["last_error"] = None
#     UVOZ_CC_ALL_STATUS["last_msg"] = None

#     try:
#         stats = uvoz_cc_run(
#             csv_path=CC_CSV_PATH,
#             db_path=str(DB_PATH),
#             import_all=True,                  # ALL
#             only_citation_contains=None,      # brez filtra
#             verbose=False,
#             dry_run=False,
#         )
#         msg = (
#             f"Uvoz iz CC CSV (ALL) KONČAN: "
#             f"dodanih {stats['inserted']}, "
#             f"posodobljenih {stats['updated']}, "
#             f"preskočenih {stats['skipped']}."
#         )
#         print(msg)
#         UVOZ_CC_ALL_STATUS["last_msg"] = msg

#     except Exception as e:
#         err = f"Napaka pri uvozu iz CC CSV (ALL): {e}"
#         print(err)
#         traceback.print_exc()
#         UVOZ_CC_ALL_STATUS["last_error"] = err

#     finally:
#         UVOZ_CC_ALL_STATUS["running"] = False



#


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
    # --- BULLETPROOF SLIKE: backend vrne točen URL ---
    # potrebuješ funkcijo image_url_for_clue(opis, dodatno) (kot sem ti jo poslal)
    if isinstance(cc, dict):
        lst = cc.get("gesla_opisi") or cc.get("geslaOpisi") or []

        def pick_str(d: dict, *keys: str) -> str:
            for k in keys:
                v = d.get(k)
                if v is not None:
                    s = str(v).strip()
                    if s:
                        return s
            return ""

        def getattr_str(obj, *attrs: str) -> str:
            for a in attrs:
                v = getattr(obj, a, None)
                if v is not None:
                    s = str(v).strip()
                    if s:
                        return s
            return ""

        for g in lst:
            # 1) dict varianta
            if isinstance(g, dict):
                opis = pick_str(g, "opis", "clue", "definition", "definicija", "text")
                dodatno = pick_str(g, "geslo", "resitev", "solution", "answer")

                # če je slika že podana, jo pusti
                cur = pick_str(g, "slika", "slika_url", "image")
                if not cur:
                    g["slika"] = image_url_for_clue(opis, dodatno)

            # 2) objekt varianta
            else:
                opis = getattr_str(g, "opis", "clue", "definition", "definicija", "text")
                dodatno = getattr_str(g, "geslo", "resitev", "solution", "answer")

                cur = getattr_str(g, "slika", "slika_url", "image")
                if not cur:
                    setattr(g, "slika", image_url_for_clue(opis, dodatno))

    # --- konec BULLETPROOF ---

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


# --- Sudoku: arhiv + prikaz --------------------------------------------------

from pathlib import Path
from datetime import datetime, date
from flask import abort, render_template, url_for, redirect

# ------------------ ARHIV ------------------

@app.get("/arhiv-sudoku/<tezavnost>", endpoint="arhiv_sudoku_pregled")
def arhiv_sudoku_pregled(tezavnost):
    """
    Arhiv sudoku po težavnosti.
    Pričakovana struktura:
      static/Sudoku_medium/2026-01/2026-01-03.js
    (tj. JS je poimenovan kot datum)
    """
    folder_map = {
        "very_easy": "Sudoku_very_easy",
        "easy": "Sudoku_easy",
        "medium": "Sudoku_medium",
        "hard": "Sudoku_hard",
    }

    tez = (tezavnost or "").strip().lower()
    sub = folder_map.get(tez)
    if not sub:
        abort(404, "Neznana težavnost sudokuja")

    root = Path(app.static_folder) / sub

    datumi = []
    if root.exists():
        for p in root.rglob("*.js"):
            stem = p.stem  # pričakujemo "YYYY-MM-DD"
            try:
                dt = datetime.strptime(stem, "%Y-%m-%d").date()
                datumi.append(dt)
            except ValueError:
                # ignoriraj vse "Sudoku_*_YYYY-MM-DD" ipd. če so se kdaj pojavili
                continue

    today = date.today()
    datumi = [d for d in datumi if d <= today]

    months_sorted, meseci = razbij_po_mesecih(datumi)

    return render_template(
        "arhiv.html",
        tip="sudoku",
        tezavnost=tez,
        months_sorted=months_sorted,
        meseci=meseci,
    )


# ------------------ PRIKAZ SUDOKUJA ------------------

@app.get("/sudoku/<tezavnost>/<datum>", endpoint="prikazi_sudoku")
def sudoku_page(tezavnost, datum):
    print("DEBUG TEZAVNOST:", tezavnost)
    print("=== SUDOKU_PAGE: STABLE VERSION LOADED ===")

    tez = (tezavnost or "").strip().lower()

    folder_map = {
        # EN
        "very_easy": "Sudoku_very_easy",
        "easy": "Sudoku_easy",
        "medium": "Sudoku_medium",
        "hard": "Sudoku_hard",

        # SI aliasi (če UI kdaj pošlje slovensko)
        "zelo-lahka": "Sudoku_very_easy",
        "zelo_lahka": "Sudoku_very_easy",
        "zelolahka": "Sudoku_very_easy",
        "lahka": "Sudoku_easy",
        "srednja": "Sudoku_medium",
        "tezka": "Sudoku_hard",
        "težka": "Sudoku_hard",
    }

    sub = folder_map.get(tez)
    if not sub:
        abort(404, f"Neznana težavnost sudokuja: {tezavnost}")

    # Validacija datuma (da ne sestavljaš čudnih poti)
    try:
        dt = datetime.strptime(datum, "%Y-%m-%d").date()
    except ValueError:
        abort(404, f"Neveljaven datum: {datum}")

    month = dt.strftime("%Y-%m")
    root = Path(app.static_folder) / sub / month

    # Tvoj standard: datum.html
    target_html = root / f"{datum}.html"
    if not target_html.exists():
        abort(404, f"Za {datum} ni sudokuja ({tez}).")

    sudoku_rel = target_html.relative_to(Path(app.static_folder)).as_posix()
    sudoku_url = url_for("static", filename=sudoku_rel)

    print("DEBUG sudoku_url:", sudoku_url)

    return render_template(
        "sudoku_igra.html",
        tezavnost=tez,
        datum=datum,
        sudoku_url=sudoku_url,
    )


# ------------------ LEGACY ------------------

@app.get("/sudoku-danes/<tezavnost>", endpoint="osnovni_sudoku")
def sudoku_danes(tezavnost):
    folder_map = {"very_easy", "easy", "medium", "hard"}
    tez = (tezavnost or "").strip().lower()
    if tez not in folder_map:
        abort(404, "Neznana težavnost sudokuja")

    today = date.today().strftime("%Y-%m-%d")
    return redirect(url_for("prikazi_sudoku", tezavnost=tez, datum=today))


@app.get("/sudoku-danes", endpoint="osnovni_sudoku_default")
def sudoku_danes_default():
    return redirect(url_for("osnovni_sudoku", tezavnost="easy"))


# TOLE ti je prej rušilo arhiv, ker ni podalo tezavnost parametra:
@app.get("/arhiv-sudoku-legacy", endpoint="arhiv_sudoku")
def arhiv_sudoku_legacy():
    return redirect(url_for("arhiv_sudoku_pregled", tezavnost="easy"))



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
    - vzamemo max 30 "besed"
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

    # max 30 "besed"
    words = text.split()
    words = words[:30]
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

from pathlib import Path

from pathlib import Path

def image_url_for_clue(opis: str, dodatno: str = "", prefer_ext: str = ".jpg") -> str:
    """
    Bulletproof:
    - proba slug po novem (npr. 30 besed)
    - fallback na legacy slug (15 besed)
    - proba več končnic
    - najde tudi duplikate z ' (1)', ' (2)'...
    - vrne točen URL /static/Images/<filename.ext> ali "" če nič ne najde
    """
    images_dir = Path(app.static_folder) / "Images"  # Images z velikim I
    if not images_dir.exists():
        return ""

    opis = (opis or "").strip()
    dodatno = (dodatno or "").strip()

    # 1) kandidati slugov: novi + legacy (15)
    slugs = []

    # novi slug (tvoja make_image_filename_from_opis že ima MAX_IMAGE_WORDS=30)
    s30 = make_image_filename_from_opis(opis, dodatno)
    if s30:
        slugs.append(s30)

    # legacy slug (15 besed) – isto pravilo, samo “odrežemo”
    def make_slug_legacy_15(opis_: str, dodatno_: str = "") -> str:
        import unicodedata, re
        text = " ".join(part for part in [(opis_ or "").strip(), (dodatno_ or "").strip()] if part).strip()
        if not text:
            return "slika"
        words = text.split()[:15]
        s = " ".join(words)
        s = unicodedata.normalize("NFD", s)
        s = "".join(ch for ch in s if not unicodedata.combining(ch))
        s = s.lower()
        s = re.sub(r"[^a-z0-9]+", "_", s)
        s = re.sub(r"_+", "_", s).strip("_")
        return s or "slika"

    s15 = make_slug_legacy_15(opis, dodatno)
    if s15 and s15 not in slugs:
        slugs.append(s15)

    if not slugs:
        return ""

    # 2) končnice (unikatno + v smiselnem vrstnem redu)
    exts = [prefer_ext, ".jpg", ".jpeg", ".png", ".webp"]
    seen_ext = []
    for e in exts:
        e = (e or "").strip().lower()
        if not e.startswith("."):
            e = "." + e
        if e not in seen_ext:
            seen_ext.append(e)

    # 3) proba: normal + " (1)" duplikati
    #    (Windows style: "ime (1).jpg")
    dup_suffixes = [""] + [f" ({i})" for i in range(1, 6)]

    for slug in slugs:
        for ext in seen_ext:
            for suf in dup_suffixes:
                fname = f"{slug}{suf}{ext}"
                if (images_dir / fname).exists():
                    return f"/static/Images/{fname}"

    return ""



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

@app.get("/prispevaj", endpoint="prispevaj_geslo")
def prispevaj_geslo():
    return "Prispevaj geslo je trenutno začasno izklopljeno."


@app.get("/preveri_slika")
def preveri_slika():
    return render_template("preveri_sliko.html")

@app.post("/api/preveri_sliko")
def api_preveri_sliko():
    """
    Bulletproof:
    - generira slug iz (opis + dodatno)
    - poišče realen filename v static/Images (tudi (1), (2) …)
    - fallback: če dodatno ne najde, proba še samo opis
    - vrne URL direkt na /static/Images/<filename> (brez /images route)
    """
    import os, sys, pprint

    data = request.get_json(silent=True) or {}
    print("api_preveri_sliko data =", pprint.pformat(data), file=sys.stderr)

    opis    = (data.get("opis") or "").strip()
    dodatno = (data.get("dodatno_ime") or data.get("dodatno") or "").strip()

    # 1) generiraj "osnovo" (slug) iz tvoje funkcije
    # make_image_filename_from_opis vrne npr. "nekaj.jpg" -> mi rabimo slug brez končnice
    fname_full = make_image_filename_from_opis(opis, dodatno)
    fname_base = make_image_filename_from_opis(opis, "")

    slug_full = os.path.splitext(fname_full)[0] if fname_full else ""
    slug_base = os.path.splitext(fname_base)[0] if fname_base else ""

    # ✅ debug šele zdaj, ko spremenljivke obstajajo
    try:
        print("DEBUG MAX_IMAGE_WORDS =", MAX_IMAGE_WORDS, file=sys.stderr)
    except Exception:
        print("DEBUG MAX_IMAGE_WORDS = (ni definiran?)", file=sys.stderr)

    print("DEBUG fname_full =", fname_full, file=sys.stderr)
    print("DEBUG fname_base =", fname_base, file=sys.stderr)
    print("DEBUG slug_full  =", slug_full, file=sys.stderr)
    print("DEBUG slug_base  =", slug_base, file=sys.stderr)

    images_dir = os.path.join(app.static_folder, "Images")  # velik I
    exts = [".jpg", ".jpeg", ".png", ".webp"]

    def find_existing_for_slug(slug: str):
        """Vrne found_filename ali None. Podpira tudi ' (1)' duplikate."""
        if not slug:
            return None

        # 1) direkt: slug + ext
        for ext in exts:
            cand = slug + ext
            if os.path.exists(os.path.join(images_dir, cand)):
                return cand

        # 2) duplikati: slug (1).ext ... slug (20).ext
        for i in range(1, 21):
            for ext in exts:
                cand = f"{slug} ({i}){ext}"
                if os.path.exists(os.path.join(images_dir, cand)):
                    return cand

        return None

    found = None

    # 2) najprej poskusi (opis + dodatno) če dodatno obstaja
    if dodatno:
        found = find_existing_for_slug(slug_full)

    # 3) fallback: samo opis
    if not found:
        found = find_existing_for_slug(slug_base)

    exists = bool(found)

    # predogled URL – direkt v static/Images
    url = f"/static/Images/{found}" if exists else None

    # predlagano ime (za UI) – vedno NEW (30 besed)
    suggested_slug = slug_full if dodatno else slug_base
    suggested_filename = (suggested_slug + ".jpg") if suggested_slug else ""

    return jsonify({
        "ok": True,
        "exists": exists,

        # ✅ predogled naj uporablja NAJDENO sliko (kar dejansko obstaja)
        "url": url,
        "found_filename": found,

        # ✅ UI/input naj vedno kaže 30-besedno predlagano ime
        "suggested_filename": suggested_filename,

        # ✅ NAJ POMEMBNEJŠE: front-end uporablja data.filename za input
        # zato mora biti suggested, ne found
        "filename": suggested_filename,

        "slug": suggested_slug,
    })


@app.post("/api/upload_sliko")
def api_upload_sliko():
    import os
    from flask import request, jsonify

    file = request.files.get("file")
    filename = (request.form.get("filename") or "").strip()

    if not file:
        return jsonify({"ok": False, "error": "Ni datoteke."})
    if not filename:
        return jsonify({"ok": False, "error": "Manjka ime datoteke."})

    # če ni končnice, jo dodamo iz originalnega imena datoteke
    if "." not in filename:
        ext = os.path.splitext(file.filename)[1].lower()
        if ext:
            filename = filename + ext

    # 1) shrani v static/Images  (folder z veliko I – tako kot imaš na disku)
    save_dir = os.path.join(app.static_folder, "Images")
    os.makedirs(save_dir, exist_ok=True)

    save_path = os.path.join(save_dir, filename)
    file.save(save_path)

    # 2) URL, ki ga front-end uporablja za <img src="...">
    url = f"/static/Images/{filename}"


    return jsonify({
        "ok": True,
        "filename": filename,
        "url": url
    })


# ===== Run ====================================================================
import os
from flask import request, jsonify, abort, render_template_string
from pathlib import Path

from flask import render_template_string

@app.get("/admin/upload-cc")
def admin_upload_cc_form():
    key = request.args.get("key")
    if key != (os.environ.get("ADMIN_KEY") or "").strip():
        abort(403)

    return render_template_string("""
    <h2>Upload CC CSV</h2>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="file" />
      <button type="submit">Upload</button>
    </form>
    """)



import os
from pathlib import Path
from flask import request, jsonify, abort

@app.post("/admin/upload-cc")
def admin_upload_cc():
    key = request.args.get("key")
    if key != (os.environ.get("ADMIN_KEY") or "").strip():
        abort(403)

    f = request.files.get("file")
    if not f or not f.filename:
        return jsonify(ok=False, msg="Manjka file"), 400

    # pomembno: .strip() pobere \n in presledke iz env var
    out_path = Path((os.getenv("CC_CLUES_PATH") or "/var/data/cc_clues_DISPLAY_UTF8.csv").strip())
    out_path.parent.mkdir(parents=True, exist_ok=True)

    f.save(str(out_path))
    return jsonify(ok=True, saved=str(out_path))


@app.get("/api/stevec-debug")
def api_stevec_debug():
    import os
    from pathlib import Path

    p = (os.getenv("CC_CLUES_PATH") or "").strip()
    exists = os.path.exists(p) if p else False

    files = []
    try:
        files = sorted([x.name for x in Path("/var/data").glob("*")])
    except Exception as e:
        files = [f"ERR: {e}"]

    return jsonify(ok=True, cc_clues_path=p, exists=exists, var_data=files)

@app.get("/debug_count")
def debug_count():
    return {
        "count_file": str(COUNT_FILE),
        "exists": COUNT_FILE.exists(),
        "value": read_passwords_count(),
    }


if __name__ == "__main__":
    # Na Windows/PyCharm včasih pomaga izklop reloaderja
    os.environ.pop("WERKZEUG_SERVER_FD", None)
    os.environ.pop("WERKZEUG_RUN_MAIN", None)
    app.run(host="127.0.0.1", port=5050, debug=False, use_reloader=False)
