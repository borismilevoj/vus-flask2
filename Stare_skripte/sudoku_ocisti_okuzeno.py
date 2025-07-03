import os

# Težavnosti in mape
tezavnosti = {
    "easy": "Sudoku_easy",
    "medium": "Sudoku_medium",
    "hard": "Sudoku_hard",
    "very_easy": "Sudoku_very_easy"
}

rezultati = []

for tezavnost, mapa in tezavnosti.items():
    sudoku_pot = os.path.join("../static", mapa, "CrosswordCompilerApp")
    if not os.path.exists(sudoku_pot):
        rezultati.append(f"❌ Mapa ne obstaja: {sudoku_pot}")
        continue

    for datoteka in os.listdir(sudoku_pot):
        if datoteka.endswith(".js"):
            polna_pot = os.path.join(sudoku_pot, datoteka)
            try:
                with open(polna_pot, "r", encoding="utf-8") as f:
                    vsebina = f.read(500)  # Preveri samo začetek datoteke

                if "var sudokuData" in vsebina:
                    rezultati.append(f"✅ PRAVILNO: {datoteka}")
                elif "var CrosswordPuzzleData" in vsebina:
                    # Označi kot okuženo
                    os.remove(polna_pot)
                    rezultati.append(f"🗑️ IZBRISANA križanka v Sudoku mapi: {datoteka}")
                else:
                    rezultati.append(f"⚠️ NEPREPOZNANA: {datoteka}")
            except Exception as e:
                rezultati.append(f"❌ Napaka pri branju {datoteka}: {e}")

for vrstica in rezultati:
    print(vrstica)
print("\n✔️ Čiščenje zaključeno.")

