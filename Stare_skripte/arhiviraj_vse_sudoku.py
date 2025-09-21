import os
import shutil

# Glavna mapa za vse sudoku
base_path = "../static"
tezavnosti = [
    "Sudoku_very_easy",
    "Sudoku_easy",
    "Sudoku_medium",
    "Sudoku_hard"
]

# Nastavi mesec za arhiviranje (npr. "2025-07" ali input())
mesec_za_arhiv = "2025-08"

for tezavnost in tezavnosti:
    sudoku_dir = os.path.join(base_path, tezavnost)
    arhiv_dir = os.path.join(sudoku_dir, mesec_za_arhiv)
    os.makedirs(arhiv_dir, exist_ok=True)
    print(f"\n-- {tezavnost} ({mesec_za_arhiv}) --")
    premaknjeni = 0
    for ime in os.listdir(sudoku_dir):
        if (ime.endswith(".js") or ime.endswith(".html")) and mesec_za_arhiv in ime:
            stara_pot = os.path.join(sudoku_dir, ime)
            nova_pot = os.path.join(arhiv_dir, ime)
            shutil.move(stara_pot, nova_pot)
            print(f"Premaknjeno: {ime}")
            premaknjeni += 1
    if premaknjeni == 0:
        print("Ni datotek za premik v tem mesecu.")
    else:
        print(f"Skupaj premaknjenih: {premaknjeni}")

print("\n✅ Arhiviranje za vse težavnosti je zaključeno!")
