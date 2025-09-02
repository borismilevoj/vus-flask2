# arhiviranje_util.py
import os, re, shutil
from datetime import datetime

# Križanke (XML/JS ležijo v korenu; v podmapah YYYY-MM je arhiv)
XW_DIR = os.path.join("static", "CrosswordCompilerApp")

# Sudoku mape po težavnosti
SUDOKU_ROOT = "static"
TEZAVNOSTI = ["very_easy", "easy", "medium", "hard", "very_hard"]

# Robustni vzorci imen
RE_XW   = re.compile(r'^(\d{4}[-–—−]\d{2}[-–—−]\d{2})\.(xml|js)$')  # npr. 2025-08-15.xml
RE_SUD  = re.compile(r'^Sudoku_(very_easy|easy|medium|hard|very_hard)_(\d{4}[-–—−]\d{2}[-–—−]\d{2})\.(html|js)$')

def _norm_dash(s: str) -> str:
    """Normalize en/em/minus dash na navaden '-'."""
    return s.replace("–","-").replace("—","-").replace("−","-")

def _month_from_date(date_str: str) -> str:
    """'2025-08-15' -> '2025-08' (normalizira pomišljaje)."""
    return _norm_dash(date_str)[:7]

def premakni_krizanke_v_mesece(mesec: str | None = None):
    """
    Premakne 2025-08-*.xml|js iz korena XW_DIR v XW_DIR/2025-08/.
    Vrne seznam premaknjenih imen datotek.
    """
    mesec_map = _norm_dash(mesec) if mesec else datetime.today().strftime("%Y-%m")
    premaknjeni: list[str] = []

    if not os.path.isdir(XW_DIR):
        return premaknjeni

    for ime in os.listdir(XW_DIR):
        src = os.path.join(XW_DIR, ime)
        if not os.path.isfile(src):
            continue
        m = RE_XW.match(ime)
        if not m:
            continue
        date_str, _ext = m.groups()
        if _month_from_date(date_str) != mesec_map:
            continue

        dst_dir = os.path.join(XW_DIR, mesec_map)
        os.makedirs(dst_dir, exist_ok=True)
        shutil.move(src, os.path.join(dst_dir, ime))
        premaknjeni.append(ime)

    return premaknjeni

def premakni_sudoku_v_mesece(mesec: str | None = None):
    """
    Premakne Sudoku_*_YYYY-MM-DD.html|js iz korena posamezne težavnosti
    v podmapo YYYY-MM. Vrne relativne poti premaknjenih datotek.
    """
    mesec_map = _norm_dash(mesec) if mesec else datetime.today().strftime("%Y-%m")
    premaknjeni: list[str] = []

    for tez in TEZAVNOSTI:
        root = os.path.join(SUDOKU_ROOT, f"Sudoku_{tez}")
        if not os.path.isdir(root):
            continue

        for ime in os.listdir(root):
            src = os.path.join(root, ime)
            if not os.path.isfile(src):
                continue
            m = RE_SUD.match(ime)
            if not m:
                continue
            _level, date_str, _ext = m.groups()
            if _month_from_date(date_str) != mesec_map:
                continue

            dst_dir = os.path.join(root, mesec_map)
            os.makedirs(dst_dir, exist_ok=True)
            shutil.move(src, os.path.join(dst_dir, ime))
            premaknjeni.append(os.path.join(f"Sudoku_{tez}", ime))


    return premaknjeni

def arhiviraj_danes():
    """Ohrani obstoječi API, če jo kličeš brez argumenta -> današnji mesec."""
    return premakni_krizanke_v_mesece() + premakni_sudoku_v_mesece()

if __name__ == "__main__":
    import sys
    target = _norm_dash(sys.argv[1]) if len(sys.argv) > 1 else None
    k = premakni_krizanke_v_mesece(target)
    s = premakni_sudoku_v_mesece(target)
    if k or s:
        print("Premaknjene križanke:")
        for f in k: print("  -", f)
        print("Premaknjeni sudoku:")
        for f in s: print("  -", f)
    else:
        print("Ni datotek za premik.")
