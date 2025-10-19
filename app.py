# app.py — CLEAN / CONSOLIDATED (fixed)
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
DB_PATH = Path(os.environ.get("DB_PATH", "/var/data/VUS.db").strip()).resolve()
LEGACY_PATH = (BASE_DIR / "VUS.db").resolve()
VUS_DB_URL = os.environ.get("VUS_DB_URL", "").strip()
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# Enkratna migracija: če ciljna baza ne obstaja, a legacy obstaja → kopiraj
if not DB_PATH.exists() and LEGACY_PATH.exists():
    try:
        shutil.copy2(LEGACY_PATH, DB_PATH)
        print(f"[VUS] Legacy DB skopirana na {DB_PATH}")
    except Exception as e:
        print(f"[VUS] OPOZORILO: kopiranje baze ni uspelo: {e}")

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False, timeout=5.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON;")
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn

def assert_baza_ok() -> None:
    if not DB_PATH.exists() or DB_PATH.stat().st_size == 0:
        raise RuntimeError(f"[VUS] Baza ne obstaja ali je prazna: {DB_PATH}")
    with get_conn() as c:
        cur = c.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='slovar'")
        if not cur.fetchone():
            tabele = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")]
            raise RuntimeError(
                f"[VUS] V bazi {DB_PATH} ni tabele 'slovar'. Najdene: {tabele or '—'}."
            )
    print(f"[VUS] OK baza: {DB_PATH}")

def ensure_indexes() -> None:
    with get_conn() as conn:
        cur = conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='slovar'")
        if not cur.fetchone():
            tabele = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")]
            raise RuntimeError(
                f"[VUS] V bazi {DB_PATH} ni tabele 'slovar'. Najdene: {tabele or '—'}."
            )
        # hitra normalizacija za iskanje po vzorcu (ignorira presledke, vezaje, podčrtaje)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_slovar_norm_expr ON slovar(replace(replace(replace(upper(GESLO),' ',''),'-',''),'_',''))")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_slovar_geslo ON slovar(GESLO)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_slovar_opis  ON slovar(OPIS)")
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

    # Dropbox (obe domeni sta OK; poskrbimo za dl=1)
    if "dropbox.com" in host or "dropboxusercontent.com" in host:
        q = parse_qs(u.query)
        if q.get("dl", ["0"])[0] != "1":
            sep = "&" if u.query else "?"
            return url + f"{sep}dl=1"
        return url

    # Google Drive: /file/d/<ID>/view → uc?export=download&id=<ID>
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

        # 1) Lokalna pot
        if os.path.isfile(src_url_or_path):
            shutil.copy2(src_url_or_path, tmp)

        # 2) file:// URL
        elif isinstance(src_url_or_path, str) and src_url_or_path.lower().startswith("file://"):
            local = src_url_or_path.replace("file://", "")
            if local.startswith("/"):  # npr. /C:/...
                local = local.lstrip("/")
            if not os.path.isfile(local):
                return False, f"Ne najdem lokalne datoteke: {local}"
            shutil.copy2(local, tmp)

        # 3) http(s)
        elif isinstance(src_url_or_path, str) and src_url_or_path.lower().startswith(("http://", "https://")):
            url = _normalize_sync_url(src_url_or_path)
            with requests.get(url, stream=True, timeout=60) as r:
                try:
                    r.raise_for_status()
                except Exception as e:
                    return False, f"HTTP napaka ({e}); URL: {url}"

                it = r.iter_content(chunk_size=4096)
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

        # 4) Preveri SQLite header
        with open(tmp, "rb") as f:
            magic = f.read(16)
        if magic != b"SQLite format 3\x00":
            return False, "Prenesena datoteka ni SQLite (manjka 'SQLite format 3\\0' header)."

        # 5) Backup + atomarna zamenjava
        if dst.exists():
            shutil.copy2(dst, bak)
        os.replace(tmp, dst)

        # 6) (best-effort) ponovno ustvari indekse po zamenjavi
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

# Admin geslo
GESLO = "Tifumannam1_vus-flask2.onrender.com"

app = Flask(__name__, static_folder='static', static_url_path='/static')
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

# ====== ARHIV helperji (potrebujejo app) ====================================
CC_BASE = Path(app.root_path) / "static" / "CrosswordCompilerApp"
SUDOKU_BASE = Path(app.root_path) / "static" / "SudokuCompilerApp"
DATE_RE_ANY = re.compile(r"^(20\d{2})-(\d{2})-(\d{2})\.(js|xml)$")

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

# ===== Diagnostika / health ===================================================
@app.get("/diag/ping")
def diag_ping():
    return "pong", 200

# === DIAG: plain-text izpis baze =============================================
@app.get("/dbdiag.txt")
def dbdiag_txt():
    from io import StringIO
    buf = StringIO()
    buf.write(f"DB_PATH={DB_PATH}\n")
    try:
        exists = DB_PATH.exists()
    except Exception:
        exists = False
    size = DB_PATH.stat().st_size if exists else 0
    buf.write(f"EXISTS={exists}\n")
    buf.write(f"SIZE={size}\n")
    try:
        with get_conn() as conn:
            cnt = conn.execute("SELECT COUNT(*) FROM slovar").fetchone()[0]
        buf.write(f"COUNT_slovar={cnt}\n")
    except Exception as e:
        buf.write(f"ERROR={e}\n")
    return buf.getvalue(), 200, {"Content-Type": "text/plain; charset=utf-8", "Cache-Control": "no-store"}

# === DIAG: preveri vir (VUS_DB_URL) in ali je direkten .db ===================
@app.get("/diag/sync-check")
def diag_sync_check():
    raw = (os.environ.get("VUS_DB_URL") or globals().get("VUS_DB_URL") or "").strip()
    raw = raw.replace("\r", "").replace("\n", "").replace("\t", "").replace("&amp;", "&")
    info = {"input": raw}
    if not raw:
        return jsonify({"ok": False, "msg": "VUS_DB_URL ni nastavljen"}), 400

    url = _normalize_sync_url(raw)
    info["normalized"] = url

    try:
        # lokalna datoteka
        if os.path.isfile(url):
            with open(url, "rb") as f:
                header = f.read(16).decode("latin1", "replace")
            return jsonify({"ok": True, "mode": "local-file", "header": header}), 200

        # file://
        if url.lower().startswith("file://"):
            p = url.replace("file://", "").lstrip("/")
            exists = os.path.isfile(p)
            header = ""
            if exists:
                with open(p, "rb") as f:
                    header = f.read(16).decode("latin1", "replace")
            return jsonify({"ok": True, "mode": "file-url", "exists": exists, "header": header}), 200

        # http(s)
        if url.lower().startswith(("http://", "https://")):
            import requests
            with requests.get(url, stream=True, allow_redirects=True, timeout=20,
                              headers={"User-Agent": "VUS-Sync/1.0"}) as r:
                first = next(r.iter_content(chunk_size=512), b"")
                return jsonify({
                    "ok": True,
                    "mode": "http",
                    "status": r.status_code,
                    "final_url": r.url,
                    "content_type": r.headers.get("content-type"),
                    "looks_html": ("text/html" in (r.headers.get("content-type") or "").lower())
                                  or (b"<html" in first[:512].lower()),
                    "header": first[:16].decode("latin1", "replace"),
                }), 200

        return jsonify({"ok": True, "mode": "unknown"}), 200

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.get("/_routes")
def show_routes():
    lines = []
    for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.rule):
        methods = sorted(m for m in rule.methods if m not in {"HEAD","OPTIONS"})
        lines.append(f"{methods} {rule.rule}  ->  endpoint='{rule.endpoint}'")
    return "<pre>" + "\n".join(lines) + "</pre>"

@app.get("/routes", endpoint="routes_json")
def routes_json():
    return jsonify(routes=sorted(map(str, app.url_map.iter_rules())))

@app.get("/dbdiag")
def dbdiag():
    info = {
        "DB_PATH": str(DB_PATH),
        "DB_EXISTS": DB_PATH.exists(),
        "DB_SIZE_BYTES": DB_PATH.stat().st_size if DB_PATH.exists() else None,
    }
    try:
        with get_conn() as conn:
            info["COUNT_slovar"] = conn.execute("SELECT COUNT(*) FROM slovar;").fetchone()[0]
    except Exception as e:
        info["ERROR"] = repr(e)
    return jsonify(info), 200

# --- ADMIN: light GET test na URL (uporablja isto normalizacijo) ---
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

# Diagnostika vira za sync (ENV VUS_DB_URL ali globalni VUS_DB_URL)


# ===== Domača stran ======================================
@app.get("/", endpoint="home")
def home():
    return redirect(url_for("prikazi_krizanko"))

# ===== Admin =============================================
@app.get("/admin", endpoint="admin")
def admin():
    print("[VUS] UPORABLJAM BAZO:", DB_PATH)
    try:
        with get_conn() as conn:
            stevec = conn.execute("SELECT COUNT(*) FROM slovar").fetchone()[0]
        # prilagodi, če admin.html pričakuje druga imena spremenljivk
        return render_template("admin.html", stevec=stevec)
    except Exception as e:
        # pokaži stran z napako, a vedno nekaj VRNI
        return render_template("admin.html", napaka=str(e)), 500



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

# ===== API / Admin preveri ====================================================
@app.post("/api/admin/preveri")
@app.post("/admin/preveri")  # alias za stare klice
def api_admin_preveri():
    payload = request.get_json(silent=True) or {}
    vnos = (payload.get("vnos")
            or request.form.get("vnos")
            or request.values.get("vnos")
            or "").strip()
    if not vnos:
        return jsonify([]), 200

    key = norm_geslo_key(vnos)
    sql = """
      SELECT geslo, opis
      FROM slovar
      WHERE REPLACE(REPLACE(REPLACE(UPPER(geslo),' ',''),'-',''),'_','') = ?
    """
    with get_conn() as conn:
        rows = conn.execute(sql, (key,)).fetchall()

    pairs = [(r["geslo"], r["opis"]) for r in rows]
    pairs = sorted(pairs, key=lambda r: sort_key_opis(r[1]))
    return jsonify([{"geslo": g, "opis": o} for g, o in pairs]), 200

# ===== API-ji / CRUD ==========================================================
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

@app.post('/dodaj_geslo')
def dodaj_geslo():
    data = request.json or {}
    geslo = (data.get('geslo') or '').strip()
    opis = (data.get('opis') or '').strip()
    if not geslo or not opis:
        return jsonify({"napaka": "Manjka geslo ali opis."}), 400
    with get_conn() as conn:
        opis_norm = normalize_ascii(opis)
        obstojece = conn.execute("SELECT ID, OPIS FROM slovar WHERE UPPER(GESLO) = UPPER(?)", (geslo,)).fetchall()
        for r in obstojece:
            if normalize_ascii(r['OPIS']) == opis_norm:
                return jsonify({"sporocilo": "Ta zapis že obstaja – ni dodano."}), 200
        conn.execute("INSERT INTO slovar (GESLO, OPIS) VALUES (?, ?)", (geslo, opis))
        new_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    return jsonify({"id": new_id, "geslo": geslo, "opis": opis, "sporocilo": "Geslo uspešno dodano!"})

@app.post('/uredi_geslo')
def uredi_geslo():
    data = request.json or {}
    id = data.get('id')
    opis = (data.get('opis') or '').strip()
    if not id:
        return jsonify({'napaka': 'Manjka ID.'}), 400
    with get_conn() as conn:
        conn.execute("UPDATE slovar SET OPIS = ? WHERE ID = ?", (opis, id))
    return jsonify({'sporocilo': 'Opis uspešno spremenjen'})

@app.post('/brisi_geslo')
def brisi_geslo():
    data = request.json or {}
    id = data.get('id')
    if not id:
        return jsonify({'napaka': 'Manjka ID.'}), 400
    with get_conn() as conn:
        conn.execute("DELETE FROM slovar WHERE ID = ?", (id,))
    return jsonify({'sporocilo': 'Geslo izbrisano.'})

# ===== Iskanje ================================================================
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

        # varno: pobegnemo %, _ in \, da LIKE ne podivja
        needle = (opis or "").replace("\\", "\\\\").replace("%", r"\%").replace("_", r"\_")
        pattern = f"%{needle}%"

        with get_conn() as conn:
            rezultat = conn.execute(
                "SELECT GESLO, OPIS FROM slovar WHERE OPIS LIKE ? ESCAPE '\\' LIMIT 100",
                (pattern,)
            ).fetchall()

        rezultat = sorted(rezultat, key=lambda r: sort_key_opis(r['OPIS']))
        return jsonify([{'GESLO': r['GESLO'], 'OPIS': r['OPIS']} for r in rezultat])

    # GET
    return render_template('isci_opis.html')

# ===== Prispevaj / števci ====================================================
@app.get('/prispevaj_geslo')
def prispevaj_geslo():
    return render_template('prispevaj.html')

@app.get('/stevec_gesel.txt')
def stevec_gesel_txt():
    try:
        with get_conn() as conn:
            has_tbl = conn.execute(
                "SELECT 1 FROM sqlite_master WHERE type='table' AND name='slovar'"
            ).fetchone() is not None
            if not has_tbl:
                return ("0\n", 200, {"Content-Type": "text/plain; charset=utf-8", "Cache-Control": "no-store"})
            st = conn.execute("SELECT COUNT(*) FROM slovar").fetchone()[0]
            return (str(st), 200, {"Content-Type": "text/plain; charset=utf-8", "Cache-Control": "no-store"})
    except Exception:
        return ("0\n", 200, {"Content-Type": "text/plain; charset=utf-8", "Cache-Control": "no-store"})

@app.get('/stevec_gesel', endpoint='stevec_gesel_json')
def stevec_gesel_json():
    try:
        with get_conn() as conn:
            st = conn.execute("SELECT COUNT(*) FROM slovar").fetchone()[0]
        resp = jsonify({"stevilo_gesel": st})
        resp.headers["Cache-Control"] = "no-store"
        return resp, 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

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
@app.get('/sudoku')
def osnovni_sudoku():
    return redirect(url_for('prikazi_danasnji_sudoku', tezavnost='lahki'))

def _find_sudoku_relpath(app, code: str, date_str: str) -> str | None:
    static_dir = Path(app.static_folder)
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

@app.post('/zamenjaj')
@login_required
def zamenjaj():
    data = request.json or {}
    original = (data.get('original') or '').strip()
    zamenjava = (data.get('zamenjava') or '').strip()
    with get_conn() as conn:
        cur = conn.execute("SELECT COUNT(*) FROM slovar WHERE OPIS LIKE ?", (f"%{original}%",))
        stevilo_zadetkov = cur.fetchone()[0]
        if stevilo_zadetkov > 0:
            conn.execute(
                "UPDATE slovar SET OPIS = REPLACE(OPIS, ?, ?) WHERE OPIS LIKE ?",
                (original, zamenjava, f"%{original}%")
            )
    return jsonify({"spremembe": stevilo_zadetkov})

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

# ===== Admin: DB sync / arhiviraj ============================================
@app.route('/admin/sync_db', methods=['GET','POST'])
@login_required
def admin_sync_db():
    app.logger.info("Sync DB triggered. DB_PATH=%s, VUS_DB_URL=%r", DB_PATH, VUS_DB_URL)
    ok, msg = _download_and_swap_db(VUS_DB_URL, DB_PATH)
    app.logger.info("Sync DB result: ok=%s; %s", ok, msg)
    flash(("✔ " if ok else "✖ ") + msg, "success" if ok else "danger")
    return redirect(url_for('admin'))

@app.post('/admin/arhiviraj')
@login_required
def sprozi_arhiviranje():
    if arhiviraj_danes is None:
        flash("Arhiviranje ni na voljo (manjka modul)", "warning")
        return redirect(url_for('admin'))
    premaknjeni = arhiviraj_danes()
    flash(f"Premaknjenih {len(premaknjeni)} datotek.", "success")
    return redirect(url_for('admin'))

# ===== Diag sync-check ========================================================

# ===== Zagon =================================================================
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
