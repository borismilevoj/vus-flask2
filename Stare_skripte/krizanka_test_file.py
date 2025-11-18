from Stare_skripte.krizanka import pridobi_podatke_iz_xml

pot_do_xml = "static/CrosswordCompilerApp/2025-05-30.xml"

try:
    podatki = pridobi_podatke_iz_xml(pot_do_xml)

    print("\n🔍 Clue številke v križanki:")
    for g in podatki['gesla_opisi']:
        x, y = g['x'] + 1, g['y'] + 1
        print(f"🟩 {g['stevilka']}: {g['solution']} ({g['smer']}) na ({x},{y})")

except FileNotFoundError:
    print(f"❌ Napaka: Datoteka ni bila najdena na poti: {pot_do_xml}")
except Exception as e:
    print(f"❌ Napaka: {e}")
