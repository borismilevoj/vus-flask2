import os, sqlite3, pathlib

# Kje iščemo – dodaš/odstraniš poti po želji
roots = [r"C:\Users\bormi", r"C:\var\data"]
exts = {".db", ".sqlite", ".sqlite3"}

def has_slovar(path):
    try:
        con = sqlite3.connect(path)
        ok = con.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='slovar'").fetchone() is not None
        n = None
        if ok:
            try:
                n = con.execute("SELECT COUNT(*) FROM slovar").fetchone()[0]
            except Exception:
                n = "?"
        con.close()
        return ok, n
    except Exception:
        return False, None

hits = []
for root in roots:
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if os.path.splitext(fn)[1].lower() in exts:
                p = os.path.join(dirpath, fn)
                try:
                    size = os.path.getsize(p)
                except Exception:
                    continue
                if size < 100*1024:
                    continue
                ok, n = has_slovar(p)
                if ok:
                    print(f"HIT | {p} | size={size} | slovar_rows={n}")
                    hits.append((p,size,n))
print("\nDone. Najdenih:", len(hits))
