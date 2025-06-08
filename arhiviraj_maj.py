from arhiviranje_util import premakni_krizanke_v_mesece, premakni_sudoku_v_mesece

mesec = "2025-05"

krizanke = premakni_krizanke_v_mesece(mesec)
sudoku = premakni_sudoku_v_mesece(mesec)

print("Premaknjene križanke:")
for f in krizanke:
    print("-", f)

print("Premaknjeni sudoku:")
for f in sudoku:
    print("-", f)
