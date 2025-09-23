import io, re, subprocess, sys

SHA = sys.argv[1] if len(sys.argv)>1 else "41471c45"

def sh(cmd):
    return subprocess.check_output(cmd, shell=True, text=True, encoding="utf-8", errors="ignore")

# 1) seznam .py datotek v commitu
files = [p for p in sh(f"git ls-tree -r --name-only {SHA}").splitlines() if p.endswith(".py")]
if not files:
    print(f"❌ Ni .py datotek v commitu {SHA}")
    sys.exit(1)

route_pat = re.compile(r"^[ \t]*@[\w\.]+\\.(?:route|get|post|put|delete)\\b", re.M)

def extract_routes(text):
    lines = text.splitlines(True)
    n = len(lines); i = 0; chunks = []
    while i < n:
        if route_pat.match(lines[i]):
            # zajemi vse dekoratorje nad funkcijo
            start = i
            while start-1 >= 0 and lines[start-1].lstrip().startswith("@"):
                start -= 1
            # poišči def vrstice
            j = i
            while j < n and not lines[j].lstrip().startswith("def "):
                j += 1
            if j == n:
                break
            # zajemi telo funkcije do naslednjega dekoratorja na levi poravnavi ali EOF
            k = j + 1
            while k < n and not route_pat.match(lines[k]):
                k += 1
            chunk = "".join(lines[start:k]).rstrip() + "\n\n"
            chunks.append(chunk)
            i = k
        else:
            i += 1
    return chunks

all_chunks = []
for path in files:
    try:
        src = sh(f"git show {SHA}:{path}")
    except subprocess.CalledProcessError:
        continue
    chunks = extract_routes(src)
    if chunks:
        all_chunks.extend(chunks)

if not all_chunks:
    print(f"❌ Ni najdenih @*.route/get/post/... rut v commitu {SHA}")
    sys.exit(1)

routes = "".join(all_chunks)
out_routes = f"routes_from_{SHA}.py"
io.open(out_routes, "w", encoding="utf-8").write(routes)
print(f"✅ Najdene rute zapisane v {out_routes} (skupaj blokov: {len(all_chunks)})")

# 2) vstavi v trenutni app.py pod marker ali pred zagon
cur = io.open("app.py","r",encoding="utf-8").read()
marker = "# ====== Tvoje obstoječe rute"
zagon  = "# ====== Zagon"
insert = "\n# ==== Routes (harvested from commit {SHA}) ====\n" + routes + "\n"

if marker in cur:
    at = cur.find(marker); end = cur.find("\n", at); 
    if end == -1: end = at + len(marker)
    merged = cur[:end+1] + insert + cur[end+1:]
elif zagon in cur:
    at = cur.find(zagon)
    merged = cur[:at] + insert + "\n" + cur[at:]
else:
    merged = cur + "\n" + insert

io.open("app.py.bak","w",encoding="utf-8").write(cur)
io.open("app_merged.py","w",encoding="utf-8").write(merged)
print(f"✅ Vstavljeno v app_merged.py | Backup: app.py.bak")
