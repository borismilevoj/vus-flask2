import os
import unicodedata
import re

def normaliziraj_naziv(ime):
    # Odstrani šumnike in posebne znake
    ime = unicodedata.normalize('NFD', ime).encode('ascii', 'ignore').decode('utf-8')
    ime = ime.lower()
    ime = ime.replace('-', ' ').replace('(', '').replace(')', '').replace(':', '').replace('.', '')
    besede = re.findall(r'\w+', ime)
    return '_'.join(besede[:8])[:64]  # max 64 znakov

def preimenuj_slike(vhodna_mapa):
    datoteke = os.listdir(vhodna_mapa)
    for ime in datoteke:
        if ime.endswith('.jpg'):
            staro = os.path.join(vhodna_mapa, ime)
            # odstrani pripono pred normalizacijo
            osnovno_ime = os.path.splitext(ime)[0]
            novo_ime = normaliziraj_naziv(osnovno_ime)
            novo = os.path.join(vhodna_mapa, f"{novo_ime}.jpg")

            if not os.path.exists(novo):
                os.rename(staro, novo)
                print(f"✅ {ime} → {os.path.basename(novo)}")
            else:
                print(f"⚠️ Preskočeno (obstaja): {os.path.basename(novo)}")

if __name__ == '__main__':
    pot_do_slik = os.path.join('static', 'Images')
    preimenuj_slike(pot_do_slik)
