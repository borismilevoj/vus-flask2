from pathlib import Path
import xml.etree.ElementTree as ET

# Namespace za <rectangular-puzzle> v Crossword Compiler XML
NS_RP = {"rp": "http://crossword.info/xml/rectangular-puzzle"}


def pridobi_podatke_as_dict(xml_path):
    """
    Interna pomožna funkcija: prebere XML in vrne (width, height, crna_polja, sol_by_xy, numbers_xy, gesla_opisi)
    brez dodatne logike. Na koncu jo ovijemo v lepši slovar.
    """
    xml_path = Path(xml_path)
    try:
        tree = ET.parse(xml_path)
    except Exception as e:
        print("[KRIZANKA] Ne morem prebrati XML:", e)
        return 0, 0, [], {}, {}, []

    root = tree.getroot()

    # poiščemo <rectangular-puzzle>
    rp = root.find(".//rp:rectangular-puzzle", NS_RP)
    if rp is None and root.tag.endswith("rectangular-puzzle"):
        rp = root
    if rp is None:
        print("[KRIZANKA] Ni <rectangular-puzzle> v XML")
        return 0, 0, [], {}, {}, []

    # ===== GRID =====
    grid = rp.find(".//rp:grid", NS_RP)
    if grid is None:
        print("[KRIZANKA] Ni <grid> v XML")
        return 0, 0, [], {}, {}, []

    width = int(grid.get("width", "0") or "0")
    height = int(grid.get("height", "0") or "0")

    crna_polja = []
    sol_by_xy = {}
    numbers_xy = {}
    black_set = set()

    for cell in grid.findall("rp:cell", NS_RP):
        xs = cell.get("x")
        ys = cell.get("y")
        if xs is None or ys is None:
            continue
        try:
            x = int(xs) - 1
            y = int(ys) - 1
        except ValueError:
            continue
        if x < 0 or y < 0:
            continue

        if cell.get("type") == "block":
            crna_polja.append([x, y])
            black_set.add((x, y))
            continue

        sol = (cell.get("solution") or "").strip()
        if sol:
            sol_by_xy["%d,%d" % (x, y)] = sol.upper()

        num = (cell.get("number") or "").strip()
        if num:
            numbers_xy["%d,%d" % (x, y)] = num

    # ===== CLUES: zgradimo mapo (smer, številka) -> besedilo =====
    clues_by = {}  # key: (direction, number) -> text

    # POZOR: v tvojem XML so <clues> pod <crossword>, zato iščemo rekurzivno
    for clist in rp.findall(".//rp:clues", NS_RP):
        # ugotovimo smer iz <title> (npr. "Across", "Down")
        direction = "across"
        title_el = clist.find("rp:title", NS_RP)
        if title_el is not None:
            t = "".join(title_el.itertext()).strip().lower()
            if "down" in t or "navpi" in t:
                direction = "down"
            else:
                direction = "across"

        for cl in clist.findall("rp:clue", NS_RP):
            num = (cl.get("number") or "").strip()
            if not num:
                continue
            text = "".join(cl.itertext()).strip()
            clues_by[(direction, num)] = text

    # ===== IZ ŠTEVILK V GRIDU IZPELJEMO ZAČETKE BESED (across & down) =====
    gesla_opisi = []

    for key, num in numbers_xy.items():
        xs, ys = key.split(",")
        x = int(xs)
        y = int(ys)

        # vodoravno: imamo številko in desno ni blok
        if x + 1 < width and (x + 1, y) not in black_set:
            # začetek besede če levo je rob ali blok
            if x == 0 or (x - 1, y) in black_set:
                opis = clues_by.get(("across", num), "")
                if opis:
                    gesla_opisi.append(
                        {
                            "x": x,
                            "y": y,
                            "smer": "across",
                            "stevilka": num,
                            "opis": opis,
                            "slika": "",
                        }
                    )

        # navpično: imamo številko in spodaj ni blok
        if y + 1 < height and (x, y + 1) not in black_set:
            # začetek besede če zgoraj je rob ali blok
            if y == 0 or (x, y - 1) in black_set:
                opis = clues_by.get(("down", num), "")
                if opis:
                    gesla_opisi.append(
                        {
                            "x": x,
                            "y": y,
                            "smer": "down",
                            "stevilka": num,
                            "opis": opis,
                            "slika": "",
                        }
                    )

    return width, height, crna_polja, sol_by_xy, numbers_xy, gesla_opisi


def pridyti_podatke_iz_xml_OLD(xml_path):
    """Stara funkcija – ne uporabljaj, samo za referenco."""
    return pridobi_podatke_as_dict(xml_path)


def pridobi_podatke_iz_xml(xml_path):
    """
    Glavna funkcija, ki jo kliče app.py.
    Vrne slovar z 'width', 'height', 'crna_polja', 'gesla_opisi', 'sol_by_xy', 'numbers_xy'.
    """
    w, h, crna, sol_map, num_map, gesla = pridobi_podatke_as_dict(xml_path)
    return {
        "width": w,
        "height": h,
        "crna_polja": crna,
        "gesla_opisi": gesla,
        "sol_by_xy": sol_map,
        "numbers_xy": num_map,
    }
