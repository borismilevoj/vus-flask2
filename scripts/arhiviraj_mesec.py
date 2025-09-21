from scripts.arhiviranje_util import premakni_krizanke_v_mesece, premakni_sudoku_v_mesece

MESEC = "2025-08"   # <-- spremeni po potrebi

k = premakni_krizanke_v_mesece(MESEC)
s = premakni_sudoku_v_mesece(MESEC)

print(f"Križanke ({MESEC}): {len(k)}")
for f in k: print(" -", f)
print(f"Sudoku ({MESEC}): {len(s)}")
for f in s: print(" -", f)
