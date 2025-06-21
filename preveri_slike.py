import os
import unicodedata
import re

# ⚙️ Nastavi pot do mape s slikami
MAPA_SLIK = os.path.join("static", "Images")

# 🧠 Opisi gesel (primer – lahko zamenjaš z realnimi opisi iz baze)
opisi = [
    "kamerunski nogometaš - Samuel (1981-)",
    "južnoameriška kukavica",
    "kanadska igralka Pascale, 1968, modri metulji",
    "angleški fizik – Newton (1643–1727)",
    # dodaj še ostale ...
]

def normaliziraj_naziv(opis):
    opis = unicodedata.normalize('NFD', opis)
    opis = re.sub(r'[\u0300-\u036f]', '', opis)            # Odstrani diakritične
    opis = re.sub(r'[-–—−]', '', opis)                     # Pomišljaje čisto odstrani
    opis = re.sub(r'[†().,;:!?]', '', opis)                # Ostale znake odstrani
    opis = opis.lower()
    opis = re.sub(r'[^a-z0-9\s]', '', opis)
    besede = opis.strip().split()
    return '_'.join(besede[:15])


manjkajoce_slike = []

for opis in opisi:
    ime = normaliziraj_naziv(opis)
    found = False
    for ext in [".jpg", ".png"]:
        pot = os.path.join(MAPA_SLIK, ime + ext)
        if os.path.exists(pot):
            found = True
            break
    if not found:
        manjkajoce_slike.append((opis, ime))


print("=== Manjkajoče slike ===")
for opis, ime in manjkajoce_slike:
    print(f"- {ime} (za opis: {opis})")

print(f"\nSkupaj manjkajočih: {len(manjkajoce_slike)}")
