import os
import unicodedata
import re

def normaliziraj_naziv(ime, max_besed=8, max_znakov=64):
    # 1. Odstrani šumnike
    ime = unicodedata.normalize('NFD', ime).encode('ascii', 'ignore').decode('utf-8')
    ime = ime.lower()

    # 2. Pretvori vse vrste vezajev in ločil v presledke, PODČRTAJE pa OHRANI!
    ime = re.sub(r'[–—−\-/(),.:;]', ' ', ime)  # ne vključimo _ tukaj!

    # 3. Odstrani vse razen črk, številk, presledkov in _
    ime = re.sub(r'[^a-z0-9\s_]', '', ime)

    # 4. Zamenjaj vse vrste presledkov z enojnimi
    ime = re.sub(r'\s+', ' ', ime)

    # 5. Razbij v besede (tudi podcrtaji ostanejo)
    besede = ime.strip().split()

    # 6. Zdruzi z _
    rezultat = '_'.join(besede[:max_besed])
    return rezultat[:max_znakov]

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
    pot_do_slik = os.path.join('static', 'Images')
    preimenuj_slike(pot_do_slik)
