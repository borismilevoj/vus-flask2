import os
import shutil

mesec = "2025-06"  # Spremeni po potrebi!
težavnosti = ["very_easy", "easy", "medium", "hard"]

for tezavnost in težavnosti:
    mapa = os.path.join('static', f'Sudoku_{tezavnost}')
    arhiv = os.path.join(mapa, mesec)
    if not os.path.exists(arhiv):
        os.makedirs(arhiv)
    premaknjeni = 0
    for f in os.listdir(mapa):
        if (f.startswith(f'Sudoku_{tezavnost}_{mesec}-') and
            (f.endswith('.html') or f.endswith('.js'))):
            src = os.path.join(mapa, f)
            dst = os.path.join(arhiv, f)
            shutil.move(src, dst)
            print(f"[{tezavnost}] Premaknjeno: {f}")
            premaknjeni += 1
    if premaknjeni == 0:
        print(f"[{tezavnost}] Ni datotek za premik za mesec {mesec}.")
print("Premikanje zaključeno za vse težavnosti!")
