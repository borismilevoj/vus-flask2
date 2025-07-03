import os
import re

# Seznam map za vse težavnosti (dodaj, če imaš še kakšno)
težavnosti = ["Sudoku_very_easy", "Sudoku_easy", "Sudoku_medium", "Sudoku_hard"]

for tezavnost in težavnosti:
    mapa = os.path.join('../static', tezavnost)
    if not os.path.exists(mapa):
        continue
    zamenjave = [
        (r'src="CrosswordCompilerApp/jquery.js"', rf'src="/static/{tezavnost}/CrosswordCompilerApp/jquery.js"'),
        (r'src="CrosswordCompilerApp/raphael.js"', rf'src="/static/{tezavnost}/CrosswordCompilerApp/raphael.js"'),
        (r'src="CrosswordCompilerApp/crosswordCompiler.js"', rf'src="/static/{tezavnost}/CrosswordCompilerApp/crosswordCompiler.js"'),
        (rf'src="{tezavnost}_(\d{{4}}-\d{{2}}-\d{{2}})\.js"', rf'src="/static/{tezavnost}/{tezavnost}_\1.js"'),
    ]
    for fname in os.listdir(mapa):
        if fname.endswith('.html'):
            fpath = os.path.join(mapa, fname)
            with open(fpath, encoding='utf-8') as f:
                vsebina = f.read()
            nova_vsebina = vsebina
            for vzorec, zamenjava in zamenjave:
                nova_vsebina = re.sub(vzorec, zamenjava, nova_vsebina)
            if nova_vsebina != vsebina:
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(nova_vsebina)
                print(f"Popravljeno: {tezavnost}/{fname}")
print("Popravljanje poti za vse težavnosti zaključeno!")
