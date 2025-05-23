import xml.etree.ElementTree as ET

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

def ocisti_znake(besedilo):
    # Odstrani presledke, pomišljaje, apostrofe, pike itd.
    return re.sub(r"[\s\-\'\.]", "", besedilo.upper())

def pridobi_podatke_iz_xml(xml_pot):
    tree = ET.parse(xml_pot)
    root = tree.getroot()

    grid = root.find('.//{http://crossword.info/xml/rectangular-puzzle}grid')
    width = int(grid.attrib['width'])
    height = int(grid.attrib['height'])

    crna_polja = []
    gesla_opisi = []

    cells = grid.findall('{http://crossword.info/xml/rectangular-puzzle}cell')
    cell_numbers = {}

    for cell in cells:
        x = int(cell.attrib.get('x', 0)) - 1
        y = int(cell.attrib.get('y', 0)) - 1
        solution = cell.attrib.get('solution')
        cell_type = cell.attrib.get('type')

        if cell_type == 'block' or not solution:
            crna_polja.append([x, y])

        if 'number' in cell.attrib:
            cell_numbers[f"{x},{y}"] = cell.attrib['number']  # ključ je zdaj string

    words = root.findall('.//{http://crossword.info/xml/rectangular-puzzle}word')
    clues = root.findall('.//{http://crossword.info/xml/rectangular-puzzle}clues/{http://crossword.info/xml/rectangular-puzzle}clue')

    for word, clue in zip(words, clues):
        x_range = word.attrib['x']
        y_range = word.attrib['y']
        solution = word.attrib['solution']
        number = clue.attrib['number']
        opis = clue.text
        smer = 'across' if '-' in x_range else 'down'

        x = int(x_range.split('-')[0]) - 1 if '-' in x_range else int(x_range) - 1
        y = int(y_range.split('-')[0]) - 1 if '-' in y_range else int(y_range) - 1

        gesla_opisi.append({
            'x': x,
            'y': y,
            'stevilka': number,
            'opis': opis,
            'solution': solution,
            'smer': smer,
            'dolzina': len(solution)
        })

    return {
        'sirina': width,
        'visina': height,
        'crna_polja': crna_polja,
        'gesla_opisi': gesla_opisi,
        'cell_numbers': cell_numbers
    }



