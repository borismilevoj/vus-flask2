# -*- coding: utf-8 -*-

import re
import os
import xml.etree.ElementTree as ET


def popravi_sumnike(besedilo: str) -> str:
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


def normaliziraj_ime(opis: str) -> str:
    """Iz opisa naredi ime slike (ASCII, spodnje črte, .jpg)."""
    s = (opis or "").lower()
    s = re.sub(r'[čć]', 'c', s)
    s = re.sub(r'[š]', 's', s)
    s = re.sub(r'[ž]', 'z', s)
    s = re.sub(r'[^a-z0-9 ]', '', s)
    s = s.replace(' ', '_')
    return s + '.jpg'


def _ns(tag: str) -> str:
    """Pomožna: polni naziv z uradnim namespace za rectangular-puzzle."""
    return f'{{http://crossword.info/xml/rectangular-puzzle}}{tag}'


def _clue_text_plain(clue_el: ET.Element) -> str:
    """Vrne plain besedilo clua (vključno znotraj <i>, <b>, ...)."""
    return ''.join(clue_el.itertext()).strip()


def pridobi_podatke_iz_xml(xml_pot: str) -> dict:
    tree = ET.parse(xml_pot)
    root = tree.getroot()

    grid = root.find(f'.//{_ns("grid")}')
    if grid is None:
        raise ValueError("XML ne vsebuje <grid> elementa.")

    width = int(grid.attrib['width'])
    height = int(grid.attrib['height'])

    crna_polja = []
    gesla_opisi = []

    # Vsi <cell>
    cells = grid.findall(_ns('cell'))
    cell_numbers = {}
    stevilke_ze_dodane = set()

    for cell in cells:
        x = int(cell.attrib.get('x', 0)) - 1
        y = int(cell.attrib.get('y', 0)) - 1
        solution = cell.attrib.get('solution')
        cell_type = cell.attrib.get('type')

        if cell_type == 'block' or not solution:
            crna_polja.append([x, y])

        # številke clue-jev (samo enkrat na koordinati)
        if 'number' in cell.attrib and (x, y) not in stevilke_ze_dodane:
            cell_numbers[f"{x},{y}"] = cell.attrib['number']
            stevilke_ze_dodane.add((x, y))

    # Vsi <word> elementi
    words = root.findall(f'.//{_ns("word")}')

    # Vsi <clue> (ne glede na namespace nad njimi)
    clues = root.findall('.//{*}clues/{*}clue')

    # Mapiranje word-id -> podatki o cluu
    clue_map = {}
    for c in clues:
        wid = c.attrib.get('word')
        if not wid:
            continue
        plain = _clue_text_plain(c)  # <-- tu je glavni popravek
        number = c.attrib.get('number', '?')
        clue_map[wid] = {
            "plain": plain,
            "number": number,
        }

    # Debug (po želji)
    # print("🔎 words:", len(words), "clues:", len(clues))

    slika_iz_opisa = None

    for word in words:
        word_id = word.attrib.get('id')
        info = clue_map.get(word_id)
        if not info:
            print(f"⚠️  Word ID brez pripadajočega clue: {word_id}")
            continue

        x_range = word.attrib['x']
        y_range = word.attrib['y']
        solution = word.attrib.get('solution')
        if not solution:
            continue

        # Plain opis (lahko vsebuje vejice, oklepaje... iz itertext())
        celi_opis = info["plain"] or ''
        # Če v opisu uporabljaš # za ločevanje slike, odreži del po #
        prikaz_opis = celi_opis.split('#')[0].strip()

        # Smer: across, če ima x razpon (npr. "10-12"), sicer down
        smer = 'across' if '-' in x_range else 'down'

        # Začetne koordinate
        x = int(x_range.split('-')[0]) - 1 if '-' in x_range else int(x_range) - 1
        y = int(y_range.split('-')[0]) - 1 if '-' in y_range else int(y_range) - 1

        # Dolžina brez presledkov/vezajev
        dolzina = len(solution.replace('-', '').replace(' ', ''))

        gesla_opisi.append({
            'x': x,
            'y': y,
            'stevilka': cell_numbers.get(f"{x},{y}", info.get("number", '?')),
            'opis': prikaz_opis,
            'solution': solution,
            'smer': smer,
            'dolzina': dolzina
        })

        # Prvo najdeno besedilo lahko uporabimo kot vir za ime slike
        if slika_iz_opisa is None:
            slika_iz_opisa = celi_opis.strip()

    # Ime slike iz prvega opisa (če obstaja)
    slika_ime = normaliziraj_ime(slika_iz_opisa) if slika_iz_opisa else None

    return {
        'sirina': width,
        'visina': height,
        'crna_polja': crna_polja,
        'gesla_opisi': gesla_opisi,
        'cell_numbers': cell_numbers,
        'slika': slika_ime
    }
