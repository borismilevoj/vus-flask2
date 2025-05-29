
def popravi_sumnike(besedilo):
    return (besedilo
            .replace('ÄŤ', 'č')
            .replace('Ä‡', 'ć')
            .replace('Å¡', 'š')
            .replace('Ĺˇ', 'š')
            .replace('Ĺľ', 'ž')
            .replace('Ĺ˝', 'Ž')
            .replace('Ä‘', 'đ')
            .replace('Ă©', 'é')
            .replace('Ă¨', 'è')
            .replace('Ă¶', 'ö')
            .replace('Ă¼', 'ü')
            .replace('Ă¤', 'ä')
            .replace('Ă¸', 'ø')
            .replace('ĂŚ', 'Ć')
            .replace('Ă', 'Á')
            .replace('Ã', 'à')
            .replace('Ăˇ', 'á')
            .replace('Ăł', 'ó')
            .replace('Ăş', 'ú')
            .replace('Ă±', 'ñ')
            .replace('Ă§', 'ç')
            .replace('ĂŹ', 'í'))

import xml.etree.ElementTree as ET
import re

def normaliziraj_ime(opis):
    opis = opis.lower()
    opis = re.sub(r'[čć]', 'c', opis)
    opis = re.sub(r'[š]', 's', opis)
    opis = re.sub(r'[ž]', 'z', opis)
    opis = re.sub(r'[^a-z0-9 ]', '', opis)
    opis = opis.replace(' ', '_')
    return opis + '.jpg'

def pridobi_podatke_iz_xml(xml_pot):
    import xml.etree.ElementTree as ET

    tree = ET.parse(xml_pot)
    root = tree.getroot()

    grid = root.find('.//{http://crossword.info/xml/rectangular-puzzle}grid')
    if grid is None:
        raise ValueError("XML ne vsebuje <grid> elementa.")

    width = int(grid.attrib['width'])
    height = int(grid.attrib['height'])

    crna_polja = []
    gesla_opisi = []

    cells = grid.findall('{http://crossword.info/xml/rectangular-puzzle}cell')
    cell_numbers = {}
    stevilke_ze_dodane = set()

    for cell in cells:
        x = int(cell.attrib.get('x', 0)) - 1
        y = int(cell.attrib.get('y', 0)) - 1
        solution = cell.attrib.get('solution')
        cell_type = cell.attrib.get('type')

        if cell_type == 'block' or not solution:
            crna_polja.append([x, y])

        if 'number' in cell.attrib and (x, y) not in stevilke_ze_dodane:
            cell_numbers[f"{x},{y}"] = cell.attrib['number']
            stevilke_ze_dodane.add((x, y))

    words = root.findall('.//{http://crossword.info/xml/rectangular-puzzle}word')
    clues = root.findall('.//{http://crossword.info/xml/rectangular-puzzle}clues/{http://crossword.info/xml/rectangular-puzzle}clue')

    print("🔎 Vseh words:", len(words))
    print("🔎 Vseh clues:", len(clues))

    slika_iz_opisa = None

    clue_map = {str(c.attrib['word']): c for c in clues}

    for word in words:
        word_id = str(word.attrib.get('id'))
        if word_id not in clue_map:
            print(f"⚠️  Word ID brez pripadajočega clue: {word_id}")
            continue

        clue = clue_map[word_id]

        x_range = word.attrib['x']
        y_range = word.attrib['y']
        solution = word.attrib.get('solution')
        if not solution:
            print(f"❗ Word ID {word_id} nima 'solution' in bo preskočen.")
            continue

        number = clue.attrib.get('number', '?')
        celi_opis = clue.text or ''
        prikaz_opis = celi_opis.split('#')[0].strip()
        smer = 'across' if '-' in x_range else 'down'

        x = int(x_range.split('-')[0]) - 1 if '-' in x_range else int(x_range) - 1
        y = int(y_range.split('-')[0]) - 1 if '-' in y_range else int(y_range) - 1

        gesla_opisi.append({
            'x': x,
            'y': y,
            'stevilka': cell_numbers.get(f"{x},{y}", '?'),
            'opis': prikaz_opis,
            'solution': solution,
            'smer': smer,
            'dolzina': len(solution)
        })

        print(f"🟩 {number}: {solution} ({smer}) na ({x+1},{y+1})")

        if slika_iz_opisa is None:
            slika_iz_opisa = celi_opis.strip()

    if slika_iz_opisa:
        slika_ime = normaliziraj_ime(slika_iz_opisa)
    else:
        slika_ime = None

    return {
        'sirina': width,
        'visina': height,
        'crna_polja': crna_polja,
        'gesla_opisi': gesla_opisi,
        'cell_numbers': cell_numbers,
        'slika': slika_ime
    }








