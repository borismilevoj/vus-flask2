# app_BIG_backup.DISABLED — minimal, da se zanesljivo zažene

from pathlib import Path
import os, shutil, sqlite3
from flask import Flask, jsonify

# --- DB ---
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get("DB_PATH", "../var/data/VUS.db")).resolve()
LEGACY_PATH = (BASE_DIR / "VUS.db").resolve()
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
if not DB_PATH.exists() and LEGACY_PATH.exists():
    try:
        shutil.copy2(LEGACY_PATH, DB_PATH)
        print(f"[VUS] Legacy DB skopirana na {DB_PATH}")
    except Exception as e:
        print(f"[VUS] OPOZORILO: kopiranje baze ni uspelo: {e}")

def get_conn():
    return sqlite3.connect(str(DB_PATH), check_same_thread=False)

def tabela_obstaja(conn, ime: str) -> bool:
    cur = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=? COLLATE NOCASE",
        (ime,)
    )
    return cur.fetchone() is not None

def assert_baza_ok() -> None:
    """Preveri bazo; če datoteka manjka/prazna ali tabela 'slovar' ne obstaja, vrzi jasno napako."""
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

def ensure_indexes():
    with get_conn() as conn:
        cur = conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='slovar'")
        if not cur.fetchone():
            tabele = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")]
            raise RuntimeError(
                f"[VUS] V bazi {DB_PATH} ni tabele 'slovar'. Najdene: {tabele or '—'}. "
                f"Napačna/prazna .db → nastavi DB_PATH."
            )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_slovar_norm_expr ON slovar(replace(replace(replace(upper(geslo),' ',''),'-',''),'_',''))")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_slovar_geslo ON slovar(geslo)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_slovar_opis  ON slovar(opis)")
        print("[VUS] Indeksi OK.")



# --- Flask ---
app = Flask(__name__, static_folder='static', static_url_path='../static')
app.secret_key = "Tifumannam1_vus-flask2.onrender.com"





@app.get("/healthz")
def healthz():
    return jsonify(status="ok", db=str(DB_PATH))

if __name__ == "__main__":
    print(f"[VUS] DB_PATH = {DB_PATH}")
    assert_baza_ok()
    ensure_indexes()
    app.run(host="127.0.0.1", port=5000, debug=True)




