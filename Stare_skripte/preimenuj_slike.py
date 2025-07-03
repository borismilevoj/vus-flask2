import os
import unicodedata
import re

def normaliziraj_naziv(opis):
    import unicodedata
    import re
    opis = unicodedata.normalize('NFD', opis)
    opis = re.sub(r'[\u0300-\u036f]', '', opis)
    opis = re.sub(r'[-–—−]', '', opis)          # tukaj je glavna sprememba!
    opis = re.sub(r'[†().,;:!?]', '', opis)
    opis = opis.lower()
    opis = re.sub(r'[^a-z0-9\s]', '', opis)
    besede = opis.strip().split()
    return '_'.join(besede[:15])


def preimenuj_slike(vhodna_mapa):
    datoteke = os.listdir(vhodna_mapa)
    for ime in datoteke:
        if ime.lower().endswith(('.jpg', '.jpeg', '.png')):
            staro = os.path.join(vhodna_mapa, ime)
            osnovno_ime = os.path.splitext(ime)[0]
            koncnica = os.path.splitext(ime)[1].lower()

            novo_ime = normaliziraj_naziv(osnovno_ime)
            novo = os.path.join(vhodna_mapa, f"{novo_ime}{koncnica}")

            if staro != novo:
                if not os.path.exists(novo):
                    os.rename(staro, novo)
                    print(f"✅ {ime} → {os.path.basename(novo)}")
                else:
                    print(f"⚠️ Preskočeno (obstaja): {os.path.basename(novo)}")
            else:
                print(f"↪️ Brez spremembe: {ime}")

if __name__ == '__main__':
    pot_do_slik = os.path.join('../static', 'Images')
    preimenuj_slike(pot_do_slik)
