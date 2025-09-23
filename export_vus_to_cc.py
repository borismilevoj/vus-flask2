# export_vus_to_cc.py
import sqlite3, csv, re, json, unicodedata, argparse, os, sys
STATE_FILE = "cc_sync_state.json"

def norm_headword(s, keep_diacritics=False):
    s = s.strip().upper()
    if not keep_diacritics:
        s = unicodedata.normalize('NFD', s)
        s = ''.join(ch for ch in s if unicodedata.category(ch) != 'Mn')
    # ven presledki, pomišljaji, apostrofi, pike, vejice, poševnice, oklepaji
    s = re.sub(r"[-' .,/()]+", "", s)
    # ven vse, kar ni A-Z (pustiš Šumnike, če keep_diacritics=True)
    if keep_diacritics:
        s = re.sub(r"[^A-ZČŠŽĆĐÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛÄËÏÖÜÑŸ]", "", s)
    else:
        s = re.sub(r"[^A-Z]", "", s)
    return s

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"last_id": 0}

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def fetch_rows(conn, mode, last_id):
    cur = conn.cursor()
    # Prilagodi ime tabele/stolpcev, če imaš drugače.
    # Privzemam: slovar(id INTEGER PK, geslo TEXT, opis TEXT)
    if mode == "delta":
        q = "SELECT id, geslo, opis FROM slovar WHERE id > ? ORDER BY id ASC"
        return cur.execute(q, (last_id,)).fetchall()
    else:
        q = "SELECT id, geslo, opis FROM slovar ORDER BY id ASC"
        return cur.execute(q).fetchall()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="VUS.db")
    ap.add_argument("--outdir", default="out")
    ap.add_argument("--mode", choices=["full","delta"], default="full")
    ap.add_argument("--keep-diacritics", action="store_true", help="Ohrani šumnike/naglase v rešitvah")
    ap.add_argument("--source", default="VUS")
    ap.add_argument("--min_len", type=int, default=2, help="Spusti kratice 1-znakovne ipd.")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    words_path = os.path.join(args.outdir, "cc_words.txt")
    clues_path = os.path.join(args.outdir, "cc_clues.csv")

    state = load_state()
    last_id = 0 if args.mode=="full" else state.get("last_id", 0)

    conn = sqlite3.connect(args.db)
    rows = fetch_rows(conn, args.mode, last_id)

    seen = set()
    max_id = last_id
    added_words = 0
    added_clues = 0

    # TXT
    wf = open(words_path, "w", encoding="utf-8", newline="")
    # CSV
    cf = open(clues_path, "w", encoding="utf-8", newline="")
    cw = csv.writer(cf)
    cw.writerow(["Headword","Clue","Source"])  # CC-friendly glave

    for _id, geslo, opis in rows:
        max_id = max(max_id, _id)
        if not geslo:
            continue
        hw = norm_headword(geslo, keep_diacritics=args.keep_diatrics if hasattr(args, 'keep_diatrics') else args.keep_diacritics)
        if not hw or len(hw) < args.min_len:
            continue
        if hw not in seen:
            wf.write(hw + "\n")
            added_words += 1
            seen.add(hw)
        # Clue: vedno zapiši (CC bo merge-al, dvojnike ignorira)
        cw.writerow([hw, (opis or "").strip(), args.source])
        added_clues += 1

    wf.close(); cf.close()
    conn.close()

    if args.mode == "delta":
        state["last_id"] = max_id
        save_state(state)
    elif args.mode == "full":
        # resetiraj marker na max id baze
        state["last_id"] = max_id
        save_state(state)

    print(f"Words zapisano: {words_path} ({added_words})")
    print(f"Clues zapisano: {clues_path} ({added_clues})")
    print(f"last_id marker: {state['last_id']}")

if __name__ == "__main__":
    main()
