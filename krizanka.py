import xml.etree.ElementTree as ET
import re

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
            .replace('Ăź', 'ü')
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
            .replace('ĂŹ', 'í')
            .replace('Ăł', 'ó')
            .replace('Ă©', 'é')
            .replace('Ă', 'í')
            .replace('Ă', 'à')
            .replace('Ă', 'è')
            .replace('Ă', 'ì'))



def pridobi_podatke_iz_xml(xml_pot):
    tree = ET.parse(xml_pot)
    root = tree.getroot()

    ns = {'ns': 'http://crossword.info/xml/rectangular-puzzle'}

    grid = root.find('.//ns:grid', ns)
    width = int(grid.get('width'))
    height = int(grid.get('height'))

    # Črna polja
    crna_polja = []
    for cell in grid.findall(".//ns:cell[@type='block']", ns):
        x = int(cell.get('x')) - 1
        y = int(cell.get('y')) - 1
        crna_polja.append((x, y))

    gesla_opisi = []

    words = root.findall('.//ns:word', ns)
    for word in words:
        geslo_id = word.get('id')
        x_range = word.get('x')
        y_range = word.get('y')

        if '-' in x_range:
            smer = 'across'
            x_start = int(x_range.split('-')[0]) - 1
            y_start = int(y_range) - 1
            dolzina = int(x_range.split('-')[1]) - int(x_range.split('-')[0]) + 1
        elif '-' in y_range:
            smer = 'down'
            x_start = int(x_range) - 1
            y_start = int(y_range.split('-')[0]) - 1
            dolzina = int(y_range.split('-')[1]) - int(y_range.split('-')[0]) + 1
        else:
            smer = 'across'
            x_start = int(x_range) - 1
            y_start = int(y_range) - 1
            dolzina = 1

        clue = root.find(f".//ns:clue[@word='{geslo_id}']", ns)
        opis = popravi_sumnike(clue.text.strip()) if clue is not None else "Ni opisa"
        opis = popravi_sumnike(opis)  # Uporaba funkcije

        # Pridobimo solution (rešitev) za geslo
        solution = word.get('solution', '').upper()
        stevilka = clue.get('number') if clue is not None else "?"
        gesla_opisi.append({
            'geslo_id': geslo_id,
            'opis': opis,
            'stevilka': stevilka,
            'x': x_start,
            'y': y_start,
            'smer': smer,
            'dolzina': dolzina,
            'solution': solution
        })

    podatki = {
        'sirina': width,
        'visina': height,
        'crna_polja': crna_polja,
        'gesla_opisi': gesla_opisi
    }

    return podatki
