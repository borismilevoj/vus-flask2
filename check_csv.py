p = r"C:\Users\bormi\OneDrive\Desktop\cc_clues_DISPLAY_UTF8.csv"
bad = []

print("start", flush=True)

with open(p, "r", encoding="utf-8", errors="replace") as f:
    for i, line in enumerate(f, 1):
        if line.count('"') % 2 == 1:
            bad.append(i)
        if i % 20000 == 0:
            print("at", i, flush=True)

print("bad_count=", len(bad))
print("first50=", bad[:50])
print("done")

