# export_vus_to_cc.py
import os, sqlite3

DB_PATH   = "../VUS.db"
OUT_WORDS = "Gesla_s_sumniki (1).txt"
OUT_CLUES = "opisi_za_cc_utf8_1.txt"

WRITE_UTF8_BOM = True  # zaradi CC
ENC = "utf-8-sig" if WRITE_UTF8_BOM else "utf-8"

def clean(s: str) -> str:
    if s is None: return ""
    return " ".join(s.replace("\r", " ").replace("\n", " ").split())

def main():
    if not os.path.exists(DB_PATH):
        print(f"Ne najdem baze: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1) Gesla (unikatna, ne-prazna)
    cur.execute("""
        SELECT DISTINCT TRIM(GESLO)
        FROM slovar
        WHERE TRIM(GESLO) <> ''
        ORDER BY UPPER(GESLO)
    """)
    words = [row[0] for row in cur.fetchall()]

    with open(OUT_WORDS, "w", encoding=ENC, newline="") as f:
        for w in words:
            f.write(f"{w}\n")

    # 2) Geslo + Opis (tab-delimited), brez praznih, brez dvojnikov
    cur.execute("""
        SELECT TRIM(GESLO), TRIM(OPIS)
        FROM slovar
        WHERE TRIM(GESLO) <> '' AND TRIM(OPIS) <> ''
        ORDER BY UPPER(GESLO), OPIS
    """)
    pairs = cur.fetchall()

    seen = set()
    written = 0
    with open(OUT_CLUES, "w", encoding=ENC, newline="") as f:
        for g, o in pairs:
            g2, o2 = clean(g), clean(o)
            key = (g2, o2)
            if key in seen:
                continue
            seen.add(key)
            f.write(f"{g2}\t{o2}\n")
            written += 1

    conn.close()

    print(f"✔ Izvožena gesla: {len(words)} → {OUT_WORDS}")
    print(f"✔ Izvoženi pari (GESLO\\tOPIS): {written} → {OUT_CLUES}")
    print("Končano.")

if __name__ == "__main__":
    main()
