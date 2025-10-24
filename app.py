# app.py — CLEAN / CONSOLIDATED
from __future__ import annotations

# ===== Imports ================================================================
import os
import re
import glob
import io
import zipfile
import sqlite3
import unicodedata
import tempfile
import shutil
import requests
import ssl
import urllib.request
from pathlib import Path
from functools import wraps
from datetime import datetime, date
from urllib.parse import urlparse, parse_qs

from flask import (
    Flask, jsonify, session, redirect, url_for, request, render_template,
    flash, send_from_directory, send_file
)

# ===== Optionalni moduli (ne podre app-a, če manjka) =========================
try:
    from scripts.krizanka import pridobi_podatke_iz_xml  # type: ignore
except Exception as e:
    print(f"[VUS] OPOZORILO: scripts.krizanka ni na voljo ({e})")
    pridobi_podatke_iz_xml = None

try:
    from Stare_skripte.uvoz_datotek import premakni_krizanke, premakni_sudoku  # type: ignore
except Exception as e:
    print(f"[VUS] OPOZORILO: Stare_skripte.uvoz_datotek ni na voljo ({e})")
    premakni_krizanke = premakni_sudoku = None

try:
    from scripts.arhiviranje_util import arhiviraj_danes  # type: ignore
except Exception as e:
    print(f"[VUS] OPOZORILO: scripts.arhiviranje_util ni na voljo ({e})")
    arhiviraj_danes = None

# ===== Helperji za normalizacijo =============================================
def _strip_diacritics(s: str) -> str:
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s)
    return "".join(ch for ch in s if unicodedata.category(ch) != "Mn")

def _norm_token(s: str) -> str:
    s = (s or "").upper().replace(" ", "").replace("-", "").replace("_", "")
    s = _strip_diacritics(s)
    return s

_FIRST_EQ = {"C": ("C", "Č", "Ć"), "S": ("S", "Š"), "Z": ("Z", "Ž")}

def normalize_ascii(s: str) -> str:
    t = unicodedata.normalize("NFKD", s or "")
    return "".join(ch for ch in t if not unicodedata.combining(ch)).lower()

def norm_geslo_key(s: str) -> str:
    if not s:
        return ""
    t = unicodedata.normalize("NFKD", s)
    t = "".join(ch for ch in t if not unicodedata.combining(ch))
    t = t.upper()
    t = re.sub(r"[ \-_]", "", t)
    return t

def ime_za_sort(opis: str) -> str:
    left, sep, right = (opis or "").rpartition(" - ")
    blok = (right if sep else opis or "").strip()
    i = blok.find("(")
    if i != -1: blok = blok[:i].strip()
    i = blok.find(",")
    if i != -1: blok = blok[:i].strip()
    ime = blok.split()[0] if blok else ""
    return normalize_ascii(ime)

def sort_key_opis(opis: str):
    je_oseba = 0 if (" - " in (opis or "")) else 1
    return (je_oseba, ime_za_sort(opis), normalize_ascii(opis))

def normalize_search(text: str) -> str:
    if not text:
        return ""
    s = unicodedata.normalize('NFD', text)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r'[^a-zA-Z0-9\s]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip().lower()
    return s

def parse_tokens(q: str):
    if not q:
        return [], []
    parts = re.findall(r'"([^"]+)"|(\S+)', q)
    inc, exc = [], []
    for quoted, plain in parts:
        tok = normalize_search(quoted or plain)
        if not tok:
            continue
        if plain and plain.startswith('-'):
            exc.append(normalize_search(plain[1:]))
        else:
            inc.append(tok)
    return inc, exc

# ===== DB pot + migracija + helperji =========================================

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get("DB_PATH", "/var/data/VUS.db").strip() or "/var/data/VUS.db").resolve()
LEGACY_PATH = (BASE_DIR / "VUS.db").resolve()
VUS_DB_URL = (os.environ.get("VUS_DB_URL") or "").strip()
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# Enkratna migracija iz legacy samo, če cilj ne obstaja in legacy izgleda realen (>1 MB)
if (not DB_PATH.exists()) and LEGACY_PATH.exists() and LEGACY_PATH.stat().st_size > 1_000_000:
    try:
        shutil.copy2(LEGACY_PATH, DB_PATH)
        print(f"[VUS] Legacy DB skopirana na {DB_PATH}")
    except Exception as e:
        print(f"[VUS] OPOZORILO: kopiranje legacy baze ni uspelo: {e}")

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False, timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON;")
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn

def assert_baza_ok() -> None:
    if not DB_PATH.exists() or DB_PATH.stat().st_size == 0:
        raise RuntimeError(f"[VUS] Baza ne obstaja ali je prazna: {DB_PATH}")
    with get_conn() as c:
        ok = c.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='slovar'").fetchone()
        if not ok:
            tabele = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")]
            raise RuntimeError(f"[VUS] V bazi {DB_PATH} ni tabele 'slovar'. Najdene: {tabele or '—'}")
    print(f"[VUS] OK baza: {DB_PATH}")

def ensure_indexes() -> None:
    with get_conn() as conn:
        conn.execute("CREATE INDEX IF NOT EXISTS idx_slovar_geslo ON slovar(GESLO)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_slovar_opis  ON slovar(OPIS)")
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_slovar_norm_expr
            ON slovar (replace(replace(replace(upper(GESLO),' ',''),'-',''),'_',''))
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_slovar_norm_len
            ON slovar (length(replace(replace(replace(GESLO,' ',''),'-',''),'_','')))
        """)
        print("[VUS] Indeksi OK.")

# --- SYNC DB helperji ---------------------------------------------------------

def _normalize_sync_url(url: str) -> str:
    """
    Popravi znane 'share' linke v direktne prenose.
    Podpira: dropbox.com, dl.dropboxusercontent.com, drive.google.com.
    Ostale vrne nespremenjene.
    """
    if not url:
        return url
    u = urlparse(url)
    host = (u.netloc or "").lower()

    if "dropbox.com" in host or "dropboxusercontent.com" in host:
        q = parse_qs(u.query)
        if q.get("dl", ["0"])[0] != "1":
            sep = "&" if u.query else "?"
            return url + f"{sep}dl=1"
        return url

    if "drive.google.com" in host or host.endswith(".google.com"):
        parts = [p for p in (u.path or "").split("/") if p]
        if "file" in parts and "d" in parts:
            try:
                file_id = parts[parts.index("d") + 1]
                return f"https://drive.google.com/uc?export=download&id={file_id}"
            except Exception:
                pass
    return url

def _is_probably_html(resp, peek: bytes = b"") -> bool:
    ct = (resp.headers.get("content-type") or "").lower()
    if "text/html" in ct:
        return True
    if peek:
        s = peek[:512].lower()
        if b"<html" in s or b"<!doctype html" in s:
            return True
    return False

def _download_and_swap_db(src_url_or_path: str, dst_path: str | Path) -> tuple[bool, str]:
    """
    Prenese .db (ali kopira iz lokalne poti), preveri SQLite header in jo
    varno zamenja (ustvari .bak). Vrne (ok: bool, msg: str).
    """
    try:
        dst = Path(dst_path).resolve()
        dst.parent.mkdir(parents=True, exist_ok=True)
        tmp = Path(tempfile.gettempdir()) / f"{dst.name}.download.tmp"
        bak = dst.with_suffix(".bak")

        if os.path.isfile(src_url_or_path):
            shutil.copy2(src_url_or_path, tmp)
        elif isinstance(src_url_or_path, str) and src_url_or_path.lower().startswith("file://"):
            local = src_url_or_path.replace("file://", "")
            if local.startswith("/"):
                local = local.lstrip("/")
            if not os.path.isfile(local):
                return False, f"Ne najdem lokalne datoteke: {local}"
            shutil.copy2(local, tmp)
        elif isinstance(src_url_or_path, str) and src_url_or_path.lower().startswith(("http://", "https://")):
            url = _normalize_sync_url(src_url_or_path)
            with requests.get(url, stream=True, timeout=(10, 600), headers={"User-Agent": "VUS-Sync/1.1"}) as r:
                try:
                    r.raise_for_status()
                except Exception as e:
                    return False, f"HTTP napaka ({e}); URL: {url}"

                it = r.iter_content(chunk_size=256 * 1024)
                first = next(it, b"")
                if _is_probably_html(r, first):
                    return False, "URL vrača HTML. Potreben je direkten .db prenos."

                with open(tmp, "wb") as f:
                    if first:
                        f.write(first)
                    for chunk in it:
                        if chunk:
                            f.write(chunk)
        else:
            return False, "VUS_DB_URL ni veljaven: uporabi pot, file:// ali http(s) URL."

        with open(tmp, "rb") as f:
            magic = f.read(16)
        if magic != b"SQLite format 3\x00":
            return False, "Prenesena datoteka ni SQLite (manjka 'SQLite format 3\\0' header)."

        if dst.exists():
            shutil.copy2(dst, bak)
        os.replace(tmp, dst)

        try:
            ensure_indexes()
        except Exception as e:
            print(f"[VUS] OPOZORILO: ensure_indexes po syncu: {e}")

        size_mb = round(dst.stat().st_size / (1024 * 1024), 2)
        bak_info = bak.name if bak.exists() else "—"
        return True, f"DB zamenjana na {dst.name} (≈{size_mb} MB). Backup: {bak_info}"

    except Exception as ex:
        try:
            if 'tmp' in locals() and Path(tmp).exists():
                Path(tmp).unlink(missing_ok=True)
        except Exception:
            pass
        return False, f"Napaka pri sinhronizaciji: {ex}"

# ===== Flask app ==============================================================

# Admin geslo (preprosto)
GESLO = "Tifumannam1_vus-flask2.onrender.com"

app = Flask(__name__, static_folder='static', static_url_path='/static')

@app.get("/home")
def home():
    return render_template("home.html")


@app.after_request
def _no_cache_html(resp):
    # HTML naj bo svež (odpravi 502 zaradi starega edge/brskalniškega cache-a)
    # statika ostane keširana kot doslej
    ctype = (resp.headers.get("Content-Type") or "").lower()
    if "text/html" in ctype:
        resp.headers["Cache-Control"] = "no-store"
        resp.headers.pop("ETag", None)  # opcijsko: še bolj prisili svežino
    return resp

from flask import request
@app.after_request
def _no_cache_html(resp):
    # HTML naj bo svež, statika naj se lahko kešira
    if resp.content_type and 'text/html' in resp.content_type:
        resp.headers['Cache-Control'] = 'no-store'
    return resp
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = "Tifumannam1_vus-flask2.onrender.com"
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['PROPAGATE_EXCEPTIONS'] = True
app.url_map.strict_slashes = False
app.config["JSON_AS_ASCII"] = False
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# (opcijsko) mapa za backupe
BACKUP_DIR = os.environ.get("BACKUP_DIR", str(DB_PATH.parent / "backups"))
os.makedirs(BACKUP_DIR, exist_ok=True)

# ===== Dekoratorji / helperji nad rutami =====================================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('prijavljen'):
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function

# ===== DIAG / HEALTH ==========================================================
@app.get("/healthz")
def healthz():
    try:
        con = get_conn(); con.execute("SELECT 1"); con.close()
        return "ok", 200
    except Exception as e:
        return f"db-fail: {e}", 500

@app.get("/diag/ping")
def diag_ping():
    return "pong", 200

@app.get("/_routes")
def show_routes():
    rules = []
    for r in app.url_map.iter_rules():
        methods = ",".join(sorted(m for m in r.methods if m in {"GET","POST"}))
        rules.append({"rule": str(r), "endpoint": r.endpoint, "methods": methods})
    rules.sort(key=lambda x: x["rule"])
    return {"ok": True, "routes": rules}, 200

@app.get("/diag/db_path")
def diag_db_path():
    p = DB_PATH
    return jsonify(ok=True, DB_PATH=str(p), exists=Path(p).exists())

@app.get("/diag/dbinfo")
def diag_dbinfo():
    p = DB_PATH
    info = {"ok": True, "DB_PATH": str(p), "exists": Path(p).exists()}
    if not info["exists"]:
        return jsonify(info)
    con = get_conn(); cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    info["tables"] = [r[0] for r in cur.fetchall()]
    try:
        cur.execute("SELECT COUNT(*) FROM slovar;")
        info["slovar_count"] = cur.fetchone()[0]
    except Exception as e:
        info["slovar_error"] = str(e)
    con.close()
    return jsonify(info)

@app.get("/diag/sync-check")
def diag_sync_check():
    url = (os.environ.get("VUS_DB_URL") or "").strip()
    info = {"ok": False, "VUS_DB_URL_present": bool(url), "url": url or None,
            "why": None, "http_status": None, "final_url": None, "content_length": None}
    if not url:
        info["why"] = "VUS_DB_URL ni nastavljen"; return jsonify(info), 400
    if not (url.startswith("http://") or url.startswith("https://")):
        info["why"] = "VUS_DB_URL mora biti http(s) direct-download link"; return jsonify(info), 400
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, context=ssl.create_default_context(), timeout=20) as resp:
            info["http_status"]=resp.status; info["final_url"]=resp.geturl()
            info["content_length"]=resp.headers.get("Content-Length")
            info["ok"] = 200 <= resp.status < 400
            info["why"] = None if info["ok"] else f"HTTP {resp.status}"
            return jsonify(info), 200 if info["ok"] else 502
    except Exception as e:
        info["why"] = f"{type(e).__name__}: {e}"
        return jsonify(info), 502

# ===== Domača stran ===========================================================
@app.get("/", endpoint="home")
def home():
    return redirect(url_for("prikazi_krizanko"))

# ===== Auth (simple) ==========================================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    napaka = None
    if request.method == 'POST':
        if request.form.get('geslo') == GESLO:
            session['prijavljen'] = True
            next_url = request.args.get('next') or url_for('home')
            return redirect(next_url)
        else:
            napaka = "Napačno geslo."
    return render_template('login.html', napaka=napaka)

@app.get('/logout')
def logout():
    session.pop('prijavljen', None)
    return redirect(url_for('login'))

# ===== Admin view =============================================================
@app.get("/admin", endpoint="admin")
@login_required
def admin():
    print("[VUS] UPORABLJAM BAZO:", DB_PATH)
    try:
        with get_conn() as conn:
            stevec = conn.execute("SELECT COUNT(*) FROM slovar").fetchone()[0]
        return render_template("admin.html", stevec=stevec)
    except Exception as e:
        return render_template("admin.html", napaka=str(e)), 500

# ===== Admin akcije (API) – usklajeno z admin.html ===========================

# ==== VUS API routes (clean) =================================================

# PREVERI (POST + GET ?t=), vrača results + exists + count
# ==== PREVERI (GET/POST, LIKE po GESLO in OPIS) ====
@app.post("/preveri_geslo", endpoint="preveri_geslo_post")
def preveri_geslo_post():
    data = request.get_json(silent=True) or {}
    q = (data.get("geslo") or data.get("t") or "").strip()
    return _preveri_common(q)

@app.get("/preveri_geslo", endpoint="preveri_geslo_get")
def preveri_geslo_get():
    q = (request.args.get("t") or "").strip()
    return _preveri_common(q)

def _preveri_common(q: str):
    if not q:
        return jsonify(ok=True, count=0, results=[], exists=False), 200

    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT id, GESLO AS geslo, OPIS AS opis
            FROM slovar
            WHERE LOWER(TRIM(GESLO)) = LOWER(TRIM(?))
              AND GESLO NOT LIKE '% %'
            ORDER BY id DESC
            LIMIT 200
            """,
            (q,),
        ).fetchall()

    results = [dict(r) for r in rows]
    exists = bool(results)
    return jsonify(ok=True, count=len(results), results=results, exists=exists), 200


# PREVERI SLIKA (ostane, samo malenkost čiščenja)

from pathlib import Path
from functools import lru_cache
from difflib import SequenceMatcher
import unicodedata
import os
from flask import jsonify, request, url_for

EXTS = (".png", ".jpg", ".jpeg", ".webp", ".gif")

def _normalize_stem(s: str) -> str:
    """NFKD, odstrani diakritike, poravna posebne narekovaje, spusti na [a-z0-9]."""
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace("’", "'").replace("`", "'").replace("“", '"').replace("”", '"')
    allowed = "abcdefghijklmnopqrstuvwxyz0123456789"
    return "".join(ch for ch in s.lower() if ch in allowed)

def _rel_static(p: Path) -> str:
    """Pot relativno na app.static_folder kot posix (za url_for)."""
    return p.relative_to(app.static_folder).as_posix()

def _score(candidate_norm: str, target_norm: str) -> tuple[int, float]:
    """
    Manjši rank je boljši.
    Rank 0: exact norm
    Rank 1: prefix
    Rank 2: substring
    Rank 3: fuzzy (SequenceMatcher.ratio) — višji ratio je boljši
    """
    if candidate_norm == target_norm:
        return (0, 1.0)
    if candidate_norm.startswith(target_norm):
        return (1, 1.0)
    if target_norm in candidate_norm:
        return (2, 1.0)
    ratio = SequenceMatcher(None, candidate_norm, target_norm).ratio()
    return (3, ratio)

@lru_cache(maxsize=1)
def _scan_index(base_path_str: str, mtime: float):
    """Vrni indeks [(path, stem, norm)] za vse slike. Cache invalidira mtime mape."""
    base = Path(base_path_str)
    items = []
    for p in base.rglob("*"):
        if p.is_file() and p.suffix.lower() in EXTS:
            stem = p.stem
            norm = _normalize_stem(stem)
            items.append((p, stem, norm))
    # determinističen vrstni red za enake score: najprej krajši stem, nato abecedno
    items.sort(key=lambda t: (len(t[1]), t[1].lower()))
    return items

@app.get("/preveri_slika")
def preveri_slika():
    raw = (request.args.get("opis") or request.args.get("ime") or "").strip()
    if not raw:
        return jsonify(ok=False, error="manjka parameter ?opis ali ?ime"), 400

    base = Path(app.static_folder) / "images"
    if not base.exists():
        return jsonify(ok=False, error=f"manjka mapa {base}"), 500

    # 0) quick exact filename hit (case-insensitive), brez normalizacije
    #    preizkusi več “case” variant in vse podprte končnice
    tried = []
    for s in dict.fromkeys([raw, raw.upper(), raw.lower(), raw.title()]):
        if not s:
            continue
        for ext in EXTS:
            cand = base / f"{s}{ext}"
            tried.append(cand)
            if cand.exists():
                rel = _rel_static(cand)
                return jsonify(ok=True, url=url_for("static", filename=rel),
                               filename=cand.name, rule="filename_exact"), 200

    # 1) indeksiraj slike (cache po mtime mape)
    #    (če dodaš/zbrišeš datoteke, se cache avtomatsko invalidira)
    mtime = base.stat().st_mtime
    items = _scan_index(str(base), mtime)

    target_norm = _normalize_stem(raw)
    if not target_norm:
        # Vse normalizirane znake je “pojedlo” — ne moremo primerjati
        return jsonify(ok=False, error="po normalizaciji ni ostalo nič (dovoli [a-z0-9])"), 400

    # 2) izberi najboljšega kandidata po ranku/ratio
    best = None
    best_key = None
    for p, stem, norm in items:
        key = _score(norm, target_norm)
        if best_key is None or key < best_key or (key == best_key and (len(stem), stem.lower()) < (len(best[1]), best[1].lower())):
            best = (p, stem, norm)
            best_key = key

        # kratki‐stik: če je exact norm, ni treba gledati naprej
        if best_key and best_key[0] == 0:
            break

    if not best:
        return jsonify(ok=True, url=None), 200

    p, stem, norm = best
    rel = _rel_static(p)
    rank, ratio = best_key
    rule = {0: "norm_exact", 1: "norm_prefix", 2: "norm_substring", 3: "fuzzy"}[rank]

    # 3) podpora za ?all=1 → vrni top k kandidatov (npr. 10)
    if request.args.get("all") in ("1", "true", "yes"):
        scored = []
        for p2, stem2, norm2 in items:
            rnk, rat = _score(norm2, target_norm)
            scored.append((rnk, rat, p2, stem2, norm2))
        # sort: rank asc, ratio desc, shorter stem first, then alpha
        scored.sort(key=lambda t: (t[0], -t[1], len(t[3]), t[3].lower()))
        k = int(request.args.get("k") or 10)
        out = []
        for rnk, rat, pp, st, nm in scored[:max(1, min(50, k))]:
            out.append({
                "url": url_for("static", filename=_rel_static(pp)),
                "filename": pp.name,
                "stem": st,
                "rule": {0: "norm_exact", 1: "norm_prefix", 2: "norm_substring", 3: "fuzzy"}[rnk],
                "ratio": round(float(rat), 4),
            })
        return jsonify(ok=True, query=raw, target_norm=target_norm, results=out), 200

    # 4) default: vrni najboljšega + diagnostiko
    return jsonify(
        ok=True,
        url=url_for("static", filename=rel),
        filename=p.name,
        stem=stem,
        rule=rule,
        ratio=round(float(ratio), 4),
        target_norm=target_norm
    ), 200



# DODAJ
@app.post("/dodaj_geslo")
def dodaj_geslo():
    data = request.get_json(silent=True) or {}
    geslo = (data.get("geslo") or "").strip()
    opis = (data.get("opis") or "").strip()
    if not geslo or not opis:
        return jsonify(napaka="Manjka geslo ali opis."), 400

    with get_conn() as conn:
        opis_norm = normalize_ascii(opis)
        obstojece = conn.execute(
            "SELECT ID, OPIS FROM slovar WHERE UPPER(GESLO) = UPPER(?)",
            (geslo,),
        ).fetchall()
        for r in obstojece:
            if normalize_ascii(r["OPIS"]) == opis_norm:
                return jsonify(sporocilo="Ta zapis že obstaja – ni dodano."), 200

        conn.execute("INSERT INTO slovar (GESLO, OPIS) VALUES (?, ?)", (geslo, opis))
        new_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

    return jsonify(id=new_id, geslo=geslo, opis=opis, sporocilo="Geslo uspešno dodano!")


# UREDI
@app.post("/uredi_geslo")
def uredi_geslo():
    data = request.get_json(silent=True) or {}
    id_ = data.get("id")
    opis = (data.get("opis") or "").strip()
    geslo = (data.get("geslo") or "").strip()
    if not id_ or not geslo:
        return jsonify(napaka="Manjka ID ali geslo."), 400
    with get_conn() as conn:
        conn.execute("UPDATE slovar SET GESLO = ?, OPIS = ? WHERE ID = ?", (geslo, opis, id_))
    return jsonify(sporocilo="Zapis uspešno spremenjen")


# BRIŠI
@app.post("/brisi_geslo")
def brisi_geslo():
    data = request.get_json(silent=True) or {}
    id_ = data.get("id")
    if not id_:
        return jsonify(napaka="Manjka ID."), 400
    with get_conn() as conn:
        conn.execute("DELETE FROM slovar WHERE ID = ?", (id_,))
    return jsonify(sporocilo="Geslo izbrisano.")


# ZAMENJAJ v opisu (bulk replace)
@app.post("/zamenjaj")
def zamenjaj():
    data = request.get_json(silent=True) or {}
    find = (data.get("find") or "").strip()
    repl = (data.get("replace") or "").strip()
    if not find:
        return jsonify(ok=False, error="Manjka iskalni izraz"), 400
    with get_conn() as conn:
        conn.execute("UPDATE slovar SET OPIS = REPLACE(OPIS, ?, ?)", (find, repl))
        count = conn.total_changes
    return jsonify(ok=True, count=count)


# SYNC DB (kot si imel)
@app.route("/admin/sync_db", methods=["GET", "POST"])
@login_required
def admin_sync_db():
    app.logger.info("Sync DB triggered. DB_PATH=%s, VUS_DB_URL=%r", DB_PATH, VUS_DB_URL)
    ok, msg = _download_and_swap_db(VUS_DB_URL, DB_PATH)
    app.logger.info("Sync DB result: ok=%s; %s", ok, msg)
    flash(("✔ " if ok else "✖ ") + msg, "success" if ok else "danger")
    return redirect(url_for("admin"))

@app.get("/admin/sync_db/test")
@login_required
def admin_sync_db_test():
    raw = os.environ.get("VUS_DB_URL") or (globals().get("VUS_DB_URL") or "")
    url = _normalize_sync_url(raw)
    if not url:
        return jsonify(ok=False, msg="VUS_DB_URL ni nastavljen"), 400
    try:
        r = requests.get(url, stream=True, allow_redirects=True, timeout=20, headers={"User-Agent": "VUS-Sync/1.0"})
        return jsonify(
            ok=r.ok,
            status=r.status_code,
            requested_url=raw,
            normalized_url=url,
            final_url=r.url,
            content_type=r.headers.get("Content-Type"),
            content_length=r.headers.get("Content-Length"),
            history=[{"code": h.status_code, "location": h.headers.get("Location")} for h in r.history],
        ), 200
    except Exception as e:
        return jsonify(ok=False, error=str(e), requested_url=raw, normalized_url=url), 500


# DIAG slike
@app.get("/diag/images")
def diag_images():
    base = Path(app.static_folder) / "images"
    if not base.exists():
        return jsonify(ok=False, error=f"Ne najdem mape: {base.as_posix()}"), 500
    q = (request.args.get("q") or "").lower()
    files = []
    for p in base.rglob("*"):
        if p.is_file():
            name = p.name
            if not q or q in name.lower():
                files.append(str(p.relative_to(base).as_posix()))
    return jsonify(ok=True, base=str(base), count=len(files), files=sorted(files))


# ROUTES JSON (ostane)
@app.get("/routes", endpoint="routes_json")
def routes_json():
    return jsonify(routes=sorted(map(str, app.url_map.iter_rules())))


# DB DIAG (JSON + TXT)
@app.get("/dbdiag")
def dbdiag():
    info = {"DB_PATH": str(DB_PATH)}
    try:
        exists = DB_PATH.exists() if hasattr(DB_PATH, "exists") else os.path.exists(DB_PATH)
        size = (DB_PATH.stat().st_size if hasattr(DB_PATH, "stat") else os.path.getsize(DB_PATH)) if exists else 0
        info.update({"DB_EXISTS": exists, "DB_SIZE_BYTES": size})
    except Exception:
        info.update({"DB_EXISTS": False, "DB_SIZE_BYTES": None})
    try:
        with get_conn() as conn:
            info["COUNT_slovar"] = conn.execute("SELECT COUNT(*) FROM slovar;").fetchone()[0]
    except Exception as e:
        info["ERROR"] = repr(e)
    return jsonify(info), 200

@app.get("/dbdiag.txt")
def dbdiag_txt():
    from io import StringIO
    buf = StringIO()
    buf.write(f"DB_PATH={DB_PATH}\n")
    try:
        exists = DB_PATH.exists() if hasattr(DB_PATH, "exists") else os.path.exists(DB_PATH)
        size = (DB_PATH.stat().st_size if hasattr(DB_PATH, "stat") else os.path.getsize(DB_PATH)) if exists else 0
    except Exception:
        exists, size = False, 0
    buf.write(f"EXISTS={exists}\nSIZE={size}\n")
    try:
        with get_conn() as conn:
            cnt = conn.execute("SELECT COUNT(*) FROM slovar").fetchone()[0]
        buf.write(f"COUNT_slovar={cnt}\n")
    except Exception as e:
        buf.write(f"ERROR={e}\n")
    return buf.getvalue(), 200, {"Content-Type": "text/plain; charset=utf-8", "Cache-Control": "no-store"}


# ===== Križanka ===============================================================

@app.get('/krizanka/static/<path:filename>')
def krizanka_static_file(filename):
    pot = os.path.join('static', 'CrosswordCompilerApp')
    return send_from_directory(pot, filename)

@app.route('/krizanka', defaults={'datum': None})
@app.route('/krizanka/<datum>')
def prikazi_krizanko(datum):
    if datum is None:
        datum = datetime.today().strftime('%Y-%m-%d')
    ime_datoteke = f"{datum}.xml"
    osnovna_pot = os.path.dirname(os.path.abspath(__file__))
    mesec = datum[:7]
    pot_arhiv = os.path.join(osnovna_pot, 'static', 'CrosswordCompilerApp', mesec, ime_datoteke)
    pot_glavna = os.path.join(osnovna_pot, 'static', 'CrosswordCompilerApp', ime_datoteke)
    if os.path.exists(pot_arhiv):
        pot_do_datoteke = pot_arhiv
    elif os.path.exists(pot_glavna):
        pot_do_datoteke = pot_glavna
    else:
        return render_template('napaka.html', sporocilo="Križanka za ta datum še ni objavljena.")
    if pridobi_podatke_iz_xml is None:
        return render_template('napaka.html', sporocilo="Modul za branje križank ni na voljo.")
    try:
        podatki = pridobi_podatke_iz_xml(pot_do_datoteke)
    except Exception as e:
        import traceback; traceback.print_exc()
        return render_template('napaka.html', sporocilo=f"Napaka pri branju križanke: {e}")
    return render_template('krizanka.html', podatki=podatki, datum=datum)

# ===== ARHIV KRIŽANK (kanonične in legacy poti) ==============================
CC_BASE = Path(app.root_path) / "static" / "CrosswordCompilerApp"
SUDOKU_BASE = Path(app.root_path) / "static" / "SudokuCompilerApp"
DATE_RE_ANY = re.compile(r"^(20\d{2})-(\d{2})-(\d{2})\.(js|xml)$")

from pathlib import Path
from datetime import date, datetime
from flask import url_for, render_template, request, abort, send_from_directory
import os

CC_BASE = Path(app.root_path) / "static" / "CrosswordCompilerApp"

def _latest_available():
    """Najdi najnovejši datum, za katerega obstajata .js in .xml."""
    best = None
    if not CC_BASE.exists():
        return None
    for ym_dir in CC_BASE.iterdir():                # npr. 2025-11
        if not ym_dir.is_dir():
            continue
        for f in ym_dir.glob("*.js"):
            try:
                d = datetime.strptime(f.stem, "%Y-%m-%d").date()
            except ValueError:
                continue
            if (ym_dir / (f.stem + ".xml")).is_file():
                best = d if (best is None or d > best) else best
    return best

def _cc_urls(d: date | None):
    """Vrne (js_url, xml_url, resolved_date) za dan; če manjka, pade na zadnjega obstoječega."""
    if d:
        ym = d.strftime("%Y-%m")
        stem = CC_BASE / ym / d.strftime("%Y-%m-%d")
        if not (stem.with_suffix(".js").is_file() and stem.with_suffix(".xml").is_file()):
            d = None
    if d is None:
        d = _latest_available()
        if d is None:
            abort(404)
    ym = d.strftime("%Y-%m")
    ymd = d.strftime("%Y-%m-%d")
    stem_rel = f"CrosswordCompilerApp/{ym}/{ymd}"
    return (
        url_for("static", filename=stem_rel + ".js"),
        url_for("static", filename=stem_rel + ".xml"),
        d,
    )

@app.get("/krizanka")
def krizanka():
    # optional: ?d=YYYY-MM-DD
    d_str = request.args.get("d")
    d = None
    if d_str:
        try:
            d = datetime.strptime(d_str, "%Y-%m-%d").date()
        except ValueError:
            d = None
    js_url, xml_url, resolved_date = _cc_urls(d)
    return render_template("krizanka.html", js_url=js_url, xml_url=xml_url, datum=resolved_date)

def zberi_pretekle(base: Path):
    """Prebere datoteke iz korena in YYYY-MM podmap, filtrira < danes."""
    today = date.today()
    meseci: dict[str, list[str]] = {}

    def add_file(p: Path):
        m = DATE_RE_ANY.match(p.name)
        if not m: return
        y, mth, d = map(int, m.groups()[:3])
        dt = date(y, mth, d)
        if dt >= today: return
        ym = f"{y:04d}-{mth:02d}"
        meseci.setdefault(ym, []).append(f"{y:04d}-{mth:02d}-{d:02d}")

    for p in sorted(base.glob("*.*")):
        if p.is_file(): add_file(p)

    for folder in sorted(base.glob("20??-??")):
        if not folder.is_dir(): continue
        for p in sorted(folder.glob("*.*")):
            if p.is_file(): add_file(p)

    meseci = {ym: sorted(days, reverse=True) for ym, days in meseci.items() if days}
    months_sorted = sorted(meseci.keys(), reverse=True)
    return months_sorted, meseci

@app.get("/arhiv/krizanke", endpoint="arhiv_krizanke")
def arhiv_krizanke():
    months_sorted, meseci = zberi_pretekle(CC_BASE)
    return render_template("arhiv.html", months_sorted=months_sorted, meseci=meseci, tip="krizanke")

@app.route("/krizanka/arhiv", methods=["GET", "HEAD"], endpoint="arhiv_krizanke_legacy_redirect")
def arhiv_krizanke_legacy_redirect():
    return redirect(url_for("arhiv_krizanke"), code=302)

@app.get("/arhiv/krizanke/<mesec>", endpoint="arhiv_krizanke_mesec")
def arhiv_krizanke_mesec(mesec):
    if not re.match(r"^\d{4}-\d{2}$", mesec):
        return render_template("napaka.html", sporocilo="Napačen format meseca."), 400
    _, meseci = zberi_pretekle(CC_BASE)
    datumi = sorted(meseci.get(mesec, []), reverse=True)
    return render_template("arhiv_mesec.html", mesec=mesec, datumi=datumi)

@app.route("/krizanka/arhiv/<mesec>", methods=["GET","HEAD"], endpoint="arhiv_krizanke_mesec_legacy")
def arhiv_krizanke_mesec_legacy(mesec):
    return redirect(url_for("arhiv_krizanke_mesec", mesec=mesec), code=302)

# ===== Sudoku (embedding & arhiv) ============================================
DATE_RE_SUDOKU = re.compile(r"^Sudoku_(?P<code>[a-z_]+)_(?P<y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2})\.html$")

def _deaccent(s: str) -> str:
    if not s: return ""
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))

def _level_candidates(user_level: str) -> list[str]:
    lvl = _deaccent((user_level or "").strip().lower()).replace("-", " ").replace("_", " ")
    if lvl in {"zelo lahki", "zelo lahko", "very easy", "veryeasy"}: return ["very_easy", "easy", "zelo_lahki"]
    if lvl in {"lahki", "lahko", "easy"}:                             return ["easy", "lahki"]
    if lvl in {"srednji", "srednje", "medium"}:                       return ["medium", "srednji"]
    if lvl in {"tezki", "tezko", "težki", "hard"}:                    return ["hard", "tezki"]
    if lvl in {"zelo tezki", "zelo težki", "very hard", "veryhard"}:  return ["very_hard", "hard", "zelo_tezki"]
    return [user_level.replace("-", "_").lower()]

def zberi_pretekle_sudoku(tezavnost: str) -> tuple[list[str], dict[str, list[str]]]:
    code = _level_candidates(tezavnost)[0]
    base = Path(app.static_folder) / f"Sudoku_{code}"
    today = date.today()
    meseci: dict[str, list[str]] = {}
    if not base.exists():
        return [], {}
    def try_add(p: Path):
        m = DATE_RE_SUDOKU.match(p.name)
        if not m: return
        y, mth, d = int(m.group('y')), int(m.group('m')), int(m.group('d'))
        dt = date(y, mth, d)
        if dt >= today: return
        ym = f"{y:04d}-{mth:02d}"
        meseci.setdefault(ym, []).append(f"{y:04d}-{mth:02d}-{d:02d}")
    for p in sorted(base.glob(f"Sudoku_{code}_*.html")):
        if p.is_file(): try_add(p)
    for folder in sorted(base.glob("20??-??")):
        if folder.is_dir():
            for p in sorted(folder.glob(f"Sudoku_{code}_*.html")):
                if p.is_file(): try_add(p)
    for ym in list(meseci.keys()):
        meseci[ym] = sorted(meseci[ym], reverse=True)
        if not meseci[ym]: meseci.pop(ym, None)
    months_sorted = sorted(meseci.keys(), reverse=True)
    return months_sorted, meseci

@app.get('/sudoku')
def osnovni_sudoku():
    return redirect(url_for('prikazi_danasnji_sudoku', tezavnost='lahki'))

def _find_sudoku_relpath(app_obj, code: str, date_str: str) -> str | None:
    static_dir = Path(app_obj.static_folder)
    yymm = date_str[:7]
    candidates = [
        f"Sudoku_{code}/{yymm}/Sudoku_{code}_{date_str}.html",
        f"Sudoku_{code}/Sudoku_{code}_{date_str}.html",
        f"Sudoku_{code}_{date_str}.html",
    ]
    for rel in candidates:
        html_abs = static_dir / rel
        js_abs   = Path(str(html_abs).removesuffix(".html") + ".js")
        if html_abs.exists() and js_abs.exists():
            return rel
    return None

@app.route('/sudoku/<tezavnost>/<datum>')
def prikazi_sudoku(tezavnost, datum):
    m = re.match(r'^(\d{4}-\d{2}-\d{2})', datum)
    if not m:
        return render_template('napaka.html', sporocilo="Napačen datum."), 400
    datum = m.group(1)
    for code in _level_candidates(tezavnost):
        rel = _find_sudoku_relpath(app, code, datum)
        if rel:
            sudoku_url = url_for('static', filename=rel)
            return render_template('sudoku_embed.html', sudoku_url=sudoku_url, tezavnost=tezavnost, datum=datum)
    return render_template('napaka.html', sporocilo="Sudoku za ta datum ali težavnost ni na voljo."), 404

@app.get('/sudoku/<tezavnost>')
def prikazi_danasnji_sudoku(tezavnost):
    danes = datetime.today().strftime('%Y-%m-%d')
    return redirect(url_for('prikazi_sudoku', tezavnost=tezavnost, datum=danes))

@app.get('/sudoku/meni')
def sudoku_meni():
    return render_template('sudoku_meni.html')

@app.get('/sudoku/arhiv/<tezavnost>/<mesec>')
def arhiv_sudoku_mesec(tezavnost, mesec):
    codes = _level_candidates(tezavnost)
    code = codes[0]
    mapa = Path(app.static_folder) / f'Sudoku_{code}' / mesec
    datumi = []
    if mapa.exists():
        for p in mapa.iterdir():
            if p.is_file() and p.name.endswith('.html'):
                try:
                    datum = p.name.replace(f'Sudoku_{code}_', '').replace('.html', '')
                    datetime.strptime(datum, "%Y-%m-%d")
                    datumi.append(datum)
                except ValueError:
                    pass
    datumi.sort(reverse=True)
    return render_template('sudoku_arhiv_mesec.html', tezavnost=tezavnost, mesec=mesec, datumi=datumi)

@app.get('/sudoku/arhiv')
def arhiv_sudoku_pregled():
    return render_template('sudoku_arhiv_glavni.html')

@app.get("/sudoku/arhiv/<tezavnost>", endpoint="arhiv_sudoku")
def arhiv_sudoku_v2(tezavnost):
    months_sorted, meseci = zberi_pretekle_sudoku(tezavnost)
    return render_template("arhiv.html", months_sorted=months_sorted, meseci=meseci, tip="sudoku", tezavnost=tezavnost)

# ===== Uvoz / utility =========================================================
def generiraj_ime_slike(opis, resitev):
    def norm(txt):
        txt = unicodedata.normalize('NFD', txt)
        txt = re.sub(r'[\u0300-\u036f]', '', txt)
        txt = txt.lower()
        txt = re.sub(r'[^a-z0-9 ]', '', txt)
        txt = '_'.join(txt.strip().split())
        return txt
    return f"{norm(opis)}_{norm(resitev)}"

def odstrani_cc_vrstico_iz_html(mapa):
    for datoteka in glob.glob(os.path.join(mapa, "*.html")):
        with open(datoteka, 'r', encoding='utf-8', errors='ignore') as f:
            vrstice = f.readlines()
        nove = [vr for vr in vrstice if "crossword-compiler.com" not in vr]
        if len(nove) < len(vrstice):
            with open(datoteka, 'w', encoding='utf-8') as f:
                f.writelines(nove)
            print(f"[VUS] Očiščeno: {datoteka}")

@app.route('/uvoz', methods=['GET', 'POST'])
@login_required
def uvoz_datotek():
    if request.method == 'POST':
        tip = request.form.get('tip')
        if tip == 'krizanka' and premakni_krizanke is not None:
            premakni_krizanke()
            flash("Križanke so bile uspešno uvožene.", "success")
        elif tip == 'sudoku' and premakni_sudoku is not None:
            tezavnost = request.form.get('tezavnost')
            premakni_sudoku(tezavnost)
            mapa = os.path.join("static", f"Sudoku_{tezavnost}")
            odstrani_cc_vrstico_iz_html(mapa)
            flash(f"Sudoku ({tezavnost}) je bil uspešno uvožen in očiščen.", "success")
        else:
            flash("Neznan tip uvoza ali manjka modul.", "danger")
        return redirect(url_for('uvoz_datotek'))
    return render_template('uvoz.html')

@app.get('/prenesi_slike_zip')
@login_required
def prenesi_slike_zip():
    pot_mape = os.path.join('static', 'Images')
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for koren, _, datoteke in os.walk(pot_mape):
            for ime_datoteke in datoteke:
                polna_pot = os.path.join(koren, ime_datoteke)
                rel_pot = os.path.relpath(polna_pot, pot_mape)
                zipf.write(polna_pot, rel_pot)
    zip_buffer.seek(0)
    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name='slike_static_Images.zip'
    )

# ===== Iskanje ================================================================
@app.post('/preveri')
def preveri():
    payload = request.get_json(silent=True) or {}
    if not payload and request.form:
        payload = request.form
    geslo = (payload.get('geslo') or '').strip()
    if not geslo:
        return jsonify({'obstaja': False, 'gesla': []})
    iskalno_norm = _norm_token(geslo)
    with get_conn() as conn:
        first = geslo[:1].upper()
        equiv = _FIRST_EQ.get(first, (first,))
        q_marks = ",".join("?" for _ in equiv)
        cand = conn.execute(
            f"""
            SELECT ID AS id, GESLO AS geslo, OPIS AS opis
            FROM slovar
            WHERE substr(upper(GESLO),1,1) IN ({q_marks})
            """,
            tuple(equiv)
        ).fetchall()
        rezultati = [r for r in cand if _norm_token(r['geslo']) == iskalno_norm]
        if not rezultati:
            iskalno_simple = geslo.upper().replace(' ', '').replace('-', '').replace('_', '')
            rezultati = conn.execute(
                """
                SELECT ID AS id, GESLO AS geslo, OPIS AS opis
                FROM slovar
                WHERE replace(replace(replace(upper(GESLO),' ',''),'-',''),'_','') = ?
                """,
                (iskalno_simple,)
            ).fetchall()
    rezultati = sorted(rezultati, key=lambda r: sort_key_opis(r['opis']))
    return jsonify({
        'obstaja': len(rezultati) > 0,
        'gesla': [{'id': r['id'], 'geslo': r['geslo'], 'opis': r['opis']} for r in rezultati]
    })

@app.route('/isci_vzorec', methods=['GET', 'POST'])
def isci_vzorec():
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form or {}
        vzorec  = (data.get('vzorec') or '').upper().replace(' ', '')
        dodatno = data.get('dodatno', '')
        try:
            dolzina_vzorca = int(data.get('dolzina') or data.get('stevilo') or 0)
        except Exception:
            dolzina_vzorca = 0
        if dolzina_vzorca <= 0:
            dolzina_vzorca = len(vzorec)
        if len(vzorec) < dolzina_vzorca:
            vzorec = vzorec + '_' * (dolzina_vzorca - len(vzorec))
        elif len(vzorec) > dolzina_vzorca:
            vzorec = vzorec[:dolzina_vzorca]
        with get_conn() as conn:
            query = (
                "SELECT ID, GESLO, OPIS FROM slovar\n"
                "WHERE LENGTH(REPLACE(REPLACE(REPLACE(GESLO, ' ', ''), '-', ''), '_', '')) = ?\n"
                "  AND OPIS IS NOT NULL"
            )
            params = [dolzina_vzorca]
            for i, crka in enumerate(vzorec):
                if crka != '_':
                    query += (
                        f" AND SUBSTR(REPLACE(REPLACE(REPLACE(GESLO, ' ', ''), '-', ''), '_', ''), {i+1}, 1) = ?"
                    )
                    params.append(crka)
            results = conn.execute(query, params).fetchall()
        inc, exc = parse_tokens(dodatno)
        def match_row(row):
            if not inc and not exc: return True
            norm = normalize_search(row["OPIS"])
            return all(t in norm for t in inc) and all(t not in norm for t in exc)
        results = [row for row in results if match_row(row)]
        results = sorted(results, key=lambda row: sort_key_opis(row["OPIS"]))
        payload = [{
            "id": row["ID"],
            "GESLO": row["GESLO"].strip(),
            "OPIS": row["OPIS"],
            "ime": ime_za_sort(row["OPIS"]),
        } for row in results]
        resp = jsonify(payload)
        resp.headers['Cache-Control'] = 'no-store'
        return resp
    return render_template('isci_vzorec.html')

@app.get('/test_iscenje')
def test_iscenje():
    return render_template('isci_vzorec_test.html')

@app.route('/isci_opis', methods=['GET', 'POST'])
def isci_opis():
    if request.method == 'POST':
        podatki = request.get_json(silent=True) or {}
        opis = podatki.get('opis', '')
        needle = (opis or "").replace("\\", "\\\\").replace("%", r"\%").replace("_", r"\_")
        pattern = f"%{needle}%"
        with get_conn() as conn:
            rezultat = conn.execute(
                "SELECT GESLO, OPIS FROM slovar WHERE OPIS LIKE ? ESCAPE '\\' LIMIT 100",
                (pattern,)
            ).fetchall()
        rezultat = sorted(rezultat, key=lambda r: sort_key_opis(r['OPIS']))
        return jsonify([{'GESLO': r['GESLO'], 'OPIS': r['OPIS']} for r in rezultat])
    return render_template('isci_opis.html')

# ===== Prispevaj / števci ====================================================
# ==== PRISPEVAJ (view) =======================================================

from flask import render_template  # (na vrhu datoteke naj bo ta import)

@app.get("/prispevaj", endpoint="prispevaj_view")
def prispevaj_view():
    return render_template("prispevaj.html")

# alias (če imaš kje hardcodano .html)
@app.get("/prispevaj.html", endpoint="prispevaj_html")
def prispevaj_html():
    return render_template("prispevaj.html")

# ==== PRISPEVAJ (alias + submit) =============================================
from flask import render_template, request, redirect, url_for, flash, jsonify  # poskrbi da so ti importi zgoraj

@app.route("/prispevaj_geslo", methods=["GET", "POST"], endpoint="prispevaj_geslo")
def prispevaj_geslo():
    """
    Alias za stare templejte, ki kličejo url_for('prispevaj_geslo').
    GET -> render 'prispevaj.html'
    POST -> sprejme polja 'geslo' in 'opis', doda v slovar in se vrne na stran.
    """
    if request.method == "GET":
        return render_template("prispevaj.html")

    # POST
    geslo = (request.form.get("geslo") or "").strip()
    opis  = (request.form.get("opis")  or "").strip()
    if not geslo or not opis:
        flash("Manjka geslo ali opis.", "danger")
        return redirect(url_for("prispevaj_geslo"))

    # opcijski anti-dup (isti kot pri /dodaj_geslo)
    try:
        with get_conn() as conn:
            opis_norm = normalize_ascii(opis) if "normalize_ascii" in globals() else opis
            obstojece = conn.execute(
                "SELECT ID, OPIS FROM slovar WHERE UPPER(GESLO) = UPPER(?)",
                (geslo,),
            ).fetchall()
            for r in obstojece:
                r_opis = r["OPIS"] if isinstance(r, dict) else r[1]
                if (normalize_ascii(r_opis) if "normalize_ascii" in globals() else r_opis) == opis_norm:
                    flash("Ta zapis že obstaja – ni dodano.", "info")
                    return redirect(url_for("prispevaj_geslo"))

            conn.execute("INSERT INTO slovar (GESLO, OPIS) VALUES (?, ?)", (geslo, opis))
        flash("Geslo uspešno dodano!", "success")
    except Exception as e:
        app.logger.exception("prispevaj_geslo POST failed: %s", e)
        flash(f"Napaka pri dodajanju: {e}", "danger")

    return redirect(url_for("prispevaj_geslo"))


# ==== ŠTEVEC: unikaten endpoint + ime funkcije (duplikat-proof) ===============

import os, sqlite3, logging
# ... (ostalo)

def _count_slovar() -> int:
    try:
        conn = get_conn()
        try:
            row = conn.execute("SELECT COUNT(1) FROM slovar").fetchone()
            return int(row[0]) if row and row[0] is not None else 0
        finally:
            conn.close()
    except sqlite3.Error as e:
        app.logger.warning(
            "Tabela 'slovar' manjka ali baza ni inicializirana (DB_PATH=%s) – %s",
            app.config.get("DB_PATH", "?"),
            e,
        )
        return 0



@app.get("/stevec_gesel.txt", endpoint="stevec_count_txt")
def stevec_count_txt():
    n = _count_slovar()
    return (str(n) + "\n", 200, {
        "Content-Type": "text/plain; charset=utf-8",
        "Cache-Control": "no-store",
    })

@app.get("/stevec_gesel", endpoint="stevec_count_json")
def stevec_count_json():
    n = _count_slovar()
    return jsonify(count=n)


# ===== MAIN ===================================================================
if __name__ == "__main__":
    print(f"[VUS] DB_PATH = {DB_PATH}")
    try:
        assert_baza_ok()
        ensure_indexes()
        print("[VUS] DB OK in indeksi pripravljeni.")
    except Exception as e:
        print(f"[VUS] DB init FAILED: {e}")

    # Windows fix za reloader fd
    os.environ.pop("WERKZEUG_SERVER_FD", None)
    os.environ.pop("WERKZEUG_RUN_MAIN", None)

    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
