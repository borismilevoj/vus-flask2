import os
import re

def popravi_ime(ime):
    # Odstrani "_jpg", "_skrajsano", ipd.
    osnovno_ime = re.sub(r'(_jpg|_skrajsano)+', '', ime)
    # Ograniči dolžino in ohrani .jpg
    return osnovno_ime[:64] + '.jpg'

def preimenuj_v_mapi(pot):
    for datoteka in os.listdir(pot):
        if datoteka.endswith('.jpg'):
            ime_brez_konc = os.path.splitext(datoteka)[0]
            novo_ime = popravi_ime(ime_brez_konc)
            staro = os.path.join(pot, datoteka)
            novo = os.path.join(pot, novo_ime)

            if not os.path.exists(novo):
                os.rename(staro, novo)
                print(f"✅ {datoteka} → {novo_ime}")
            else:
                print(f"⚠️ Preskočeno (obstaja): {novo_ime}")

if __name__ == '__main__':
    pot_do_slik = os.path.join('../static', 'Images')
    preimenuj_v_mapi(pot_do_slik)
