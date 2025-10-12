# app.py — FIXED (UTF-8, stabilna DB, rute ohranjene)
# - DB na /var/data/VUS.db (z enkratno migracijo iz lokalne VUS.db)
# - get_conn() z Row row_factory
# - assert_baza_ok() + ensure_indexes()
# - /healthz za hiter check
# - helperji/dekoratorji nad rutami
# - arhiviranje in prikaz: samo PRETEKLI datumi
from __future__ import annotations

# ===== Imports ================================================================
from pathlib import Path
from functools import wraps
from datetime import datetime, date
import os
import io
import re
import glob
import zipfile
import shutil
import sqlite3
import unicodedata
import requests
import tempfile

from flask import (
    Flask, jsonify, session, redirect, url_for, request, render_template,
    flash, send_from_directory, send_file
)

# Poskusi uvoziti tvoje module — ne zruši app-a, če manjka (le opozori)
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


# ===== DB pot + migracija + helperji =========================================
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get("DB_PATH", "/var/data/VUS.db")).resolve()
LEGACY_PATH = (BASE_DIR / "VUS.db").resolve()
VUS_DB_URL = os.environ.get("VUS_DB_URL", "")

DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# Enkratna migracija: če ciljna baza ne obstaja, a legacy obstaja → kopiraj
if not DB_PATH.exists() and LEGACY_PATH.exists():
    try:
        shutil.copy2(LEGACY_PATH, DB_PATH)
        print(f"[VUS] Legacy DB skopirana na {DB_PATH}")
    except Exception as e:
        print(f"[VUS] OPOZORILO: kopiranje baze ni uspelo: {e}")


def get_conn() -> sqlite3.Connection:
    """Vrni SQLite povezavo na DB_PATH (WAL + NORMAL), z Row row_factory."""
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn


def assert_baza_ok() -> None:
    """Preveri, da baza obstaja in ima tabelo 'slovar'."""
    if not DB_PATH.exists() or DB_PATH.stat().st_size == 0:
        raise RuntimeError(f"[VUS] Baza ne obstaja ali je prazna: {DB_PATH}")
    with get_conn() as c:
        cur = c.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='slovar'")
        if not cur.fetchone():
            tabele = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")]
            raise RuntimeError(
                f"[VUS] V bazi {DB_PATH} ni tabele 'slovar'. Najdene: {tabele or '—'}. "
                f"Napačna/prazna .db → nastavi DB_PATH ali uvozi pravo bazo."
            )
    print(f"[VUS] OK baza: {DB_PATH}")


def ensure_indexes() -> None:
    """Ustvari potrebne indekse."""
    with get_conn() as conn:
        cur = conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='slovar'")
        if not cur.fetchone():
            tabele = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")]
            raise RuntimeError(
                f"[VUS] V bazi {DB_PATH} ni tabele 'slovar'. Najdene: {tabele or '—'}. "
                f"Napačna/prazna .db → nastavi DB_PATH."
            )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_slovar_norm_expr ON slovar(replace(replace(replace(upper(GESLO),' ',''),'-',''),'_',''))")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_slovar_geslo ON slovar(GESLO)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_slovar_opis  ON slovar(OPIS)")
        print("[VUS] Indeksi OK.")


def _download_and_swap_db(src_url: str, dst_path: Path) -> tuple[bool, str]:
    """
    Prenese SQLite DB v temp, preveri in atomsko zamenja.
    """
    if not src_url:
        return False, "VUS_DB_URL ni nastavljen."

    try:
        dst_path.parent.mkdir(parents=True, exist_ok=True)

        with requests.get(src_url, stream=True, timeout=90) as r:
            r.raise_for_status()
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        tmp.write(chunk)
                tmp_path = Path(tmp.name)

        # sanity check
        try:
            con = sqlite3.connect(str(tmp_path))
            con.execute("SELECT name FROM sqlite_master LIMIT 1;").fetchone()
            con.close()
        except Exception as e:
            tmp_path.unlink(missing_ok=True)
            return False, f"Datoteka ne izgleda kot veljavna SQLite baza: {e}"

        shutil.move(str(tmp_path), str(dst_path))
        try:
            ensure_indexes()
        except Exception as e:
            print(f"[VUS] OPOZORILO: ensure_indexes po syncu: {e}")

        return True, "Baza uspešno posodobljena."
    except Exception as e:
        return False, f"Napaka pri prenosu/zamenjavi: {e}"


# (opcijsko) mapa za backupe
BACKUP_DIR = os.environ.get("BACKUP_DIR", str(DB_PATH.parent / "backups"))
os.makedirs(BACKUP_DIR, exist_ok=True)

# Admin geslo
GESLO = "Tifumannam1_vus-flask2.onrender.com"

# ===== Flask app ==============================================================
app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = "Tifumannam1_vus-flask2.onrender.com"
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['PROPAGATE_EXCEPTIONS'] = True

# ---- Helperji in dekoratorji (morajo biti nad rutami) -----------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('prijavljen'):
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function

def normalize_search(text: str) -> str:
    if not text:
        return ""
    s = unicodedata.normalize('NFD', text)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r'[^a-zA-Z0-9\s]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip().lower()
    return s

def parse_tokens(q: str):
    """Vrne (include_tokens, exclude_tokens). Fraze v "..." so en token. -token izključi."""
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

def normalize_ascii(text: str) -> str:
    if not text:
        return ""
    s = unicodedata.normalize('NFD', text)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return ' '.join(s.lower().split())

def ime_za_sort(opis: str) -> str:
    if not opis or ' - ' not in opis:
        return ""
    blok = opis.split(' - ', 1)[1].strip()
    if '(' in blok:
        blok = blok.split('(', 1)[0].strip()
    if ',' in blok:
        blok = blok.split(',', 1)[1].strip()
    ime = blok.split()[0] if blok else ""
    return normalize_ascii(ime)

def sort_key_opis(opis: str):
    je_oseba = 0 if ' - ' in (opis or '') else 1
    return (je_oseba, ime_za_sort(opis), normalize_ascii(opis))
# -----------------------------------------------------------------------------

# ======= ARHIV: helperji in rute (v2) ========================================
CC_BASE = Path(app.root_path) / "static" / "CrosswordCompilerApp"
SUDOKU_BASE = Path(app.root_path) / "static" / "SudokuCompilerApp"
DATE_RE_ANY = re.compile(r"^(20\d{2})-(\d{2})-(\d{2})\.(js|xml)$")

def zberi_pretekle(base: Path):
    """
    Prebere datoteke iz korena in YYYY-MM podmap, filtrira < danes,
    vrne (months_sorted, meseci) z meseci = {'YYYY-MM': ['YYYY-MM-DD', ...]}.
    """
    today = date.today()
    meseci: dict[str, list[str]] = {}

    def add_file(p: Path):
        m = DATE_RE_ANY.match(p.name)
        if not m:
            return
        y, mth, d = map(int, m.groups()[:3])
        dt = date(y, mth, d)
        if dt >= today:
            return
        ym = f"{y:04d}-{mth:02d}"
        meseci.setdefault(ym, []).append(f"{y:04d}-{mth:02d}-{d:02d}")

    for p in sorted(base.glob("*.*")):
        if p.is_file():
            add_file(p)

    for folder in sorted(base.glob("20??-??")):
        if not folder.is_dir():
            continue
        for p in sorted(folder.glob("*.*")):
            if p.is_file():
                add_file(p)

    meseci = {ym: sorted(days, reverse=True) for ym, days in meseci.items() if days}
    months_sorted = sorted(meseci.keys(), reverse=True)
    return months_sorted, meseci

# --- ARHIV (KRIŽANKE) – samo pretekli datumi -------------------------------
@app.get("/arhiv/krizanke")
def arhiv_krizanke():
    months_sorted, meseci = zberi_pretekle(CC_BASE)
    return render_template(
        "arhiv.html",
        months_sorted=months_sorted,
        meseci=meseci,
        tip="krizanke",
    )

@app.get("/sudoku/arhiv/<tezavnost>", endpoint="arhiv_sudoku")
def arhiv_sudoku_v2(tezavnost):
    months_sorted, meseci = zberi_pretekle_sudoku(tezavnost)
    return render_template(
        "arhiv.html",
        months_sorted=months_sorted,
        meseci=meseci,
        tip="sudoku",
        tezavnost=tezavnost
    )

@app.get("/api/admin/arhiv_diag")
def arhiv_diag():
    what = request.args.get("what", "krizanke")
    tez = request.args.get("tezavnost", "")
    base = (SUDOKU_BASE / tez) if (what == "sudoku" and (SUDOKU_BASE / tez).exists()) else (SUDOKU_BASE if what == "sudoku" else CC_BASE)

    today = date.today()
    total = past = future = 0
    koren = [p.name for p in base.glob("*.*") if p.is_file()]
    mes_mape = [f.name for f in base.glob("20??-??") if f.is_dir()]

    for p in list(base.glob("*.*")) + [pp for f in base.glob("20??-??") if f.is_dir() for pp in f.glob("*.*")]:
        if not p.is_file():
            continue
        m = DATE_RE_ANY.match(p.name)
        if not m:
            continue
        total += 1
        y, mm, dd = map(int, m.groups()[:3])
        if date(y, mm, dd) < today:
            past += 1
        else:
            future += 1

    return jsonify({
        "ok": True,
        "base": str(base),
        "exists": base.exists(),
        "koren_files": koren[:10],
        "month_dirs": mes_mape[:10],
        "counts": {"total_named": total, "past": past, "future_or_today": future}
    })

# --- ARHIVIRANJE (premakni samo PRETEKLE v mesečne mape) ---------------------
def premakni_v_mesecne_mape(base: Path = CC_BASE):
    today = date.today()
    moved, skipped_existing, skipped_future = [], [], []
    for p in sorted(base.glob("*.*")):
        if not p.is_file():
            continue
        m = DATE_RE_ANY.match(p.name)
        if not m:
            continue
        y, mm, dd = map(int, m.groups()[:3])
        dt = date(y, mm, dd)
        if dt >= today:
            skipped_future.append(p.name)
            continue
        ym = f"{y:04d}-{mm:02d}"
        target_dir = base / ym
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / p.name
        if target.exists():
            skipped_existing.append(p.name)
            continue
        shutil.move(str(p), str(target))
        moved.append(p.name)
    return {"moved": moved, "skipped_existing": skipped_existing, "skipped_future": skipped_future}

@app.post("/api/admin/arhiviraj", endpoint="api_admin_arhiviraj_v4")
def api_admin_arhiviraj_v4():
    try:
        res = premakni_v_mesecne_mape()
        return jsonify({
            "ok": True,
            "moved_count": len(res["moved"]),
            "skipped_existing_count": len(res["skipped_existing"]),
            "skipped_future_count": len(res["skipped_future"]),
            "moved": res["moved"],
            "skipped_existing": res["skipped_existing"],
            "skipped_future": res["skipped_future"],
        })
    except Exception as e:
        app.logger.exception("Napaka pri arhiviranju")
        return jsonify({"ok": False, "error": str(e)}), 500

@app.get("/api/admin/arhiviraj/ping", endpoint="api_admin_arhiviraj_ping_v4")
def api_admin_arhiviraj_ping_v4():
    top_level = [p.name for p in CC_BASE.glob("*.*")]
    return jsonify({
        "ok": True,
        "base": str(CC_BASE),
        "base_exists": CC_BASE.exists(),
        "top_level_files": len(top_level),
        "sample": top_level[:5],
    })

# --- Poskrbi, da uploads mapa res obstaja -----------------------------------
if not os.path.isdir(app.config['UPLOAD_FOLDER']):
    if os.path.exists(app.config['UPLOAD_FOLDER']):  # obstaja kot datoteka
        os.remove(app.config['UPLOAD_FOLDER'])
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# ===== Diagnostika / Health ===================================================
@app.get("/ping")
def ping():
    return "OK iz Flaska!"

@app.get("/health")
def health():
    return "ok", 200

@app.get("/healthz")
def healthz():
    return jsonify(status="ok", db=str(DB_PATH))

@app.get("/_routes")
def show_routes():
    lines = []
    for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.rule):
        lines.append(f"{sorted(rule.methods)} {rule.rule}  ->  endpoint='{rule.endpoint}'")
    return "<pre>" + "\n".join(lines) + "</pre>"

@app.get("/test")
def test():
    return render_template("test.html")


# ===== Avtentikacija ==========================================================
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


# ===== Domača stran (root + /home) ===========================================
@app.route('/')
@app.route('/home')
def home():
    obvestilo = ""
    try:
        with open('obvestilo.txt', encoding="utf-8") as f:
            obvestilo = f.read().strip()
    except FileNotFoundError:
        pass
    return render_template('home.html', obvestilo=obvestilo)

# ===== 404 handler ============================================================
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for("home"))


# ===== Admin =================================================================
@app.get('/admin')
@login_required
def admin():
    print("[VUS] UPORABLJAM BAZO:", DB_PATH)
    try:
        with get_conn() as conn:
            cur = conn.execute("SELECT COUNT(*) FROM slovar")
            stevilo = cur.fetchone()[0]
        return render_template('admin.html', stevilo_gesel=stevilo)
    except Exception as e:
        return f"<h1>Napaka v admin: {e}</h1>"

@app.post('/admin/sync_db')
@login_required
def admin_sync_db():
    ok, msg = _download_and_swap_db(VUS_DB_URL, DB_PATH)
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


# ===== API-ji / CRUD ==========================================================
@app.post('/preveri')
def preveri():
    payload = request.get_json(silent=True) or {}
    if not payload and request.form:
        payload = request.form

    geslo = (payload.get('geslo') or '').strip()
    if not geslo:
        return jsonify({'obstaja': False, 'gesla': []})

    # normalizacija IDENTIČNA kot v indeksu/poizvedbi
    iskalno = geslo.upper().replace(' ', '').replace('-', '').replace('_', '')

    with get_conn() as conn:
        cur = conn.execute(
            """
            SELECT ID AS id, GESLO AS geslo, OPIS AS opis
            FROM slovar
            WHERE replace(replace(replace(upper(GESLO),' ',''),'-',''),'_','') = ?
            """,
            (iskalno,)
        )
        rezultati = cur.fetchall()

    # sortiranje: osebe najprej, po imenu; ostalo po opisu
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
        # deduplikacija po normaliziranem OPIS-u (brez šumnikov/case)
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
@app.get('/test_iscenje')
def test_iscenje():
    return render_template('isci_vzorec_test.html')

@app.route('/isci_vzorec', methods=['GET', 'POST'])
def isci_vzorec():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify([])

        data = request.get_json(silent=True) or {}
        vzorec = (data.get('vzorec') or '').upper().replace(' ', '')
        dodatno = data.get('dodatno', '')

        # dolžina
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
            if not inc and not exc:
                return True
            norm = normalize_search(row["OPIS"])
            return all(t in norm for t in inc) and all(t not in norm for t in exc)

        results = [row for row in results if match_row(row)]
        results = sorted(results, key=lambda row: sort_key_opis(row["OPIS"]))

        payload = [{
            "id": row["ID"],
            "GESLO": row["GESLO"].strip(),
            "OPIS": row["OPIS"],
            "ime": ime_za_sort(row["OPIS"])
        } for row in results]

        resp = jsonify(payload)
        resp.headers['Cache-Control'] = 'no-store'
        return resp

    return render_template('isci_vzorec.html')

@app.route('/isci_opis', methods=['GET', 'POST'])
def isci_opis():
    if request.method == 'POST':
        podatki = request.get_json(silent=True) or {}
        opis = podatki.get('opis', '')

        with get_conn() as conn:
            rezultat = conn.execute(
                "SELECT GESLO, OPIS FROM slovar WHERE OPIS LIKE ? LIMIT 100",
                (f"%{opis}%",)
            ).fetchall()

        rezultat = sorted(rezultat, key=lambda r: sort_key_opis(r['OPIS']))
        return jsonify([{'GESLO': r['GESLO'], 'OPIS': r['OPIS']} for r in rezultat])

    return render_template('isci_opis.html')

@app.get('/prispevaj_geslo')
def prispevaj_geslo():
    return render_template('prispevaj.html')

@app.get('/stevec_gesel')        # JSON
def stevec_gesel_json():
    with get_conn() as conn:
        st = conn.execute("SELECT COUNT(*) FROM slovar").fetchone()[0]
    resp = jsonify({"stevilo_gesel": st})
    resp.headers['Cache-Control'] = 'no-store'
    return resp

@app.get('/stevec_gesel.txt')    # PLAIN TEXT
def stevec_gesel_txt():
    with get_conn() as conn:
        st = conn.execute("SELECT COUNT(*) FROM slovar").fetchone()[0]
    return str(st), 200, {
        "Content-Type": "text/plain; charset=utf-8",
        "Cache-Control": "no-store",
    }


# ===== Križanka ===============================================================
@app.get('/krizanka/static/<path:filename>')
def krizanka_static_file(filename):
    pot = os.path.join('static', 'Krizanke', 'CrosswordCompilerApp')
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

# --- ARHIV (KRIŽANKE) – samo pretekli datumi ---
# kompatibilnost (stara pot -> nova)
@app.get("/krizanka/arhiv")
def arhiv_krizank_legacy_redirect():
    return redirect(url_for("arhiv_krizanke"))



# ===== Sudoku ================================================================
def _deaccent(s: str) -> str:
    if not s:
        return ""
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))

def _level_candidates(user_level: str) -> list[str]:
    lvl = _deaccent((user_level or "").strip().lower()).replace("-", " ").replace("_", " ")
    if lvl in {"zelo lahki", "zelo lahko", "very easy", "veryeasy"}:
        return ["very_easy", "easy", "zelo_lahki"]
    if lvl in {"lahki", "lahko", "easy"}:
        return ["easy", "lahki"]
    if lvl in {"srednji", "srednje", "medium"}:
        return ["medium", "srednji"]
    if lvl in {"tezki", "tezko", "težki", "hard"}:
        return ["hard", "tezki"]
    if lvl in {"zelo tezki", "zelo težki", "very hard", "veryhard"}:
        return ["very_hard", "hard", "zelo_tezki"]
    return [user_level.replace("-", "_").lower()]

# --- ARHIV (SUDOKU) – preberi samo pretekle datume iz static/Sudoku_<code> ---
DATE_RE_SUDOKU = re.compile(r"^Sudoku_(?P<code>[a-z_]+)_(?P<y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2})\.html$")

def zberi_pretekle_sudoku(tezavnost: str) -> tuple[list[str], dict[str, list[str]]]:
    """Vrne (months_sorted, meseci) za podani level. Gleda:
       static/Sudoku_<code>/*.html in static/Sudoku_<code>/<YYYY-MM>/*.html
       ter vrne le datume < danes.
    """
    code = _level_candidates(tezavnost)[0]            # npr. 'very_easy'
    base = Path(app.static_folder) / f"Sudoku_{code}" # npr. static/Sudoku_very_easy
    today = date.today()
    meseci: dict[str, list[str]] = {}

    if not base.exists():
        return [], {}

    def try_add(p: Path):
        m = DATE_RE_SUDOKU.match(p.name)
        if not m:
            return
        y, mth, d = int(m.group('y')), int(m.group('m')), int(m.group('d'))
        dt = date(y, mth, d)
        if dt >= today:
            return                                  # izloči danes/prihodnost
        ym = f"{y:04d}-{mth:02d}"
        meseci.setdefault(ym, []).append(f"{y:04d}-{mth:02d}-{d:02d}")

    # 1) koren: static/Sudoku_<code>/*.html
    for p in sorted(base.glob("Sudoku_{}_*.html".format(code))):
        if p.is_file():
            try_add(p)

    # 2) mesečne podmape: static/Sudoku_<code>/<YYYY-MM>/*.html
    for folder in sorted(base.glob("20??-??")):
        if folder.is_dir():
            for p in sorted(folder.glob("Sudoku_{}_*.html".format(code))):
                if p.is_file():
                    try_add(p)

    # sortiraj in očisti prazne
    for ym in list(meseci.keys()):
        meseci[ym] = sorted(meseci[ym], reverse=True)
        if not meseci[ym]:
            meseci.pop(ym, None)
    months_sorted = sorted(meseci.keys(), reverse=True)
    return months_sorted, meseci


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

@app.get('/sudoku')
def osnovni_sudoku():
    return redirect(url_for('prikazi_danasnji_sudoku', tezavnost='lahki'))

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
            return render_template('sudoku_embed.html',
                                   sudoku_url=sudoku_url,
                                   tezavnost=tezavnost,
                                   datum=datum)
    return render_template('napaka.html',
                           sporocilo="Sudoku za ta datum ali težavnost ni na voljo."), 404

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

@app.route('/preveri_sliko', methods=['GET', 'POST'])
@login_required
def preveri_sliko():
    ime_slike = None
    obstaja = None
    opis = ''
    resitev = ''
    koncnice = ['jpg', 'png', 'webp']
    if request.method == 'POST':
        opis = request.form.get('opis', '')
        resitev = request.form.get('resitev', '')
        osnovno_ime = generiraj_ime_slike(opis, resitev)
        for ext in koncnice:
            pot = os.path.join('static', 'Images', f"{osnovno_ime}.{ext}")
            if os.path.exists(pot):
                ime_slike = f"{osnovno_ime}.{ext}"
                obstaja = True
                break
        if not ime_slike:
            ime_slike = f"{osnovno_ime}.jpg"
            obstaja = False
    return render_template('preveri_sliko.html', opis=opis, resitev=resitev, ime_slike=ime_slike, obstaja=obstaja)


# ===== Zagon =================================================================
if __name__ == "__main__":
    print(f"[VUS] DB_PATH = {DB_PATH}")
    assert_baza_ok()
    ensure_indexes()
    app.run(host="127.0.0.1", port=5000, debug=True)
