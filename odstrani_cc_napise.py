import os
import re

# SEZNAM MAP ZA VSE TEŽAVNOSTI
težavnosti = ["Sudoku_very_easy", "Sudoku_easy", "Sudoku_medium", "Sudoku_hard"]

for tezavnost in težavnosti:
    mapa = os.path.join('static', tezavnost)
    if not os.path.exists(mapa):
        continue

    for fname in os.listdir(mapa):
        if fname.endswith('.html'):
            fpath = os.path.join(mapa, fname)
            with open(fpath, encoding='utf-8') as f:
                vsebina = f.read()
            nova_vsebina = vsebina

            # ODSTRANI <span> in <div> z Copyrighti, footerji in podobnimi
            # 1. <SPAN ...>Web page created by ...</SPAN>
            nova_vsebina = re.sub(r'<SPAN[^>]*?>\s*Web page created by.*?</SPAN>', '', nova_vsebina, flags=re.DOTALL|re.IGNORECASE)
            # 2. <span> ali <div> s "Software © crossword-compiler.com"
            nova_vsebina = re.sub(r'<(span|div)[^>]*?>\s*Software © crossword-compiler\.com.*?</\1>', '', nova_vsebina, flags=re.DOTALL|re.IGNORECASE)
            # 3. Vse z "Crossword Compiler" v footerju ali copyrightu
            nova_vsebina = re.sub(r'<[^>]*?>([^<]*Crossword Compiler[^<]*)</[^>]*?>', lambda m: '' if 'footer' in m.group(0).lower() or 'copy' in m.group(0).lower() else m.group(0), nova_vsebina, flags=re.DOTALL|re.IGNORECASE)
            # 4. Dodatno: kar koli s class="CopyTag" ali "PuzCopyright" ali "PuzFooter"
            nova_vsebina = re.sub(r'<[^>]*class="(?:CopyTag|PuzCopyright|PuzFooter)"[^>]*>.*?</[^>]+>', '', nova_vsebina, flags=re.DOTALL|re.IGNORECASE)

            if nova_vsebina != vsebina:
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(nova_vsebina)
                print(f"CC napisi odstranjeni v: {tezavnost}/{fname}")

print("Odstranjevanje vseh sledi Crossword Compilerja zaključeno!")
