import re, io, sys

OLD = "app_old.py"
CUR = "app_BIG_backup.DISABLED"
OUT = "app_merged.py"

old = io.open(OLD, "r", encoding="utf-8", errors="ignore").read()
cur = io.open(CUR, "r", encoding="utf-8").read()

lines = old.splitlines(True)
route_pat = re.compile(r"^@app\.(route|get|post|put|delete)\b", re.M)

chunks=[]; i=0; n=len(lines)
while i<n:
    if route_pat.match(lines[i]):
        start=i
        j=i-1
        while j>=0 and lines[j].startswith('@'):
            start=j; j-=1
        i+=1
        while i<n and not route_pat.match(lines[i]):
            i+=1
        chunk = ''.join(lines[start:i]).rstrip() + "\n\n"
        if "if __name__ == \"__main__\":" in chunk:
            chunk = chunk.split("if __name__ == \"__main__\":")[0].rstrip() + "\n\n"
        chunks.append(chunk)
    else:
        i+=1

routes = ''.join(chunks).strip()
print("Najdenih rut:", len(chunks))
if not routes:
    print("❌ Ni najdenih @app.rut v", OLD)
    sys.exit(1)

marker = "# ====== Tvoje obstoječe rute"
zagon  = "# ====== Zagon"
if marker in cur:
    at = cur.find(marker)
    end = cur.find("\n", at)
    if end == -1: end = at + len(marker)
    cur_new = cur[:end+1] + "\n# ==== Routes (merged from git) ====\n" + routes + "\n" + cur[end+1:]
elif zagon in cur:
    at = cur.find(zagon)
    cur_new = cur[:at] + "\n# ==== Routes (merged from git) ====\n" + routes + "\n\n" + cur[at:]
else:
    cur_new = cur + "\n\n# ==== Routes (merged from git) ====\n" + routes + "\n"

io.open("Stare_skripte/app.py.bak", "w", encoding="utf-8").write(cur)
io.open(OUT,"w",encoding="utf-8").write(cur_new)
print("✅ Vstavljeno v", OUT, "| Backup:", "app_BIG_backup.DISABLED.bak")
