import puz
import xml.etree.ElementTree as ET

def puz_to_xml(puz_file, xml_file):
    p = puz.read(puz_file)

    root = ET.Element('crossword-compiler', attrib={'xmlns': 'http://crossword.info/xml/rectangular-puzzle'})
    rect_puzzle = ET.SubElement(root, 'rectangular-puzzle')

    metadata = ET.SubElement(rect_puzzle, 'metadata')
    ET.SubElement(metadata, 'title').text = p.title
    ET.SubElement(metadata, 'creator').text = p.author
    ET.SubElement(metadata, 'copyright').text = p.copyright

    crossword = ET.SubElement(rect_puzzle, 'crossword', attrib={'rows': str(p.height), 'cols': str(p.width)})

    grid = ET.SubElement(crossword, 'grid', attrib={'width': str(p.width), 'height': str(p.height)})
    solution = p.solution

    for y in range(p.height):
        for x in range(p.width):
            i = y * p.width + x
            char = solution[i]
            if char == '.':
                ET.SubElement(grid, 'cell', attrib={'x': str(x+1), 'y': str(y+1), 'type': 'block'})
            else:
                ET.SubElement(grid, 'cell', attrib={'x': str(x+1), 'y': str(y+1), 'solution': char})

    clues = ET.SubElement(crossword, 'clues')
    across = ET.SubElement(clues, 'across')
    down = ET.SubElement(clues, 'down')

    numbering = p.clue_numbering()
    for clue in numbering.across:
        ET.SubElement(across, 'clue', attrib={'number': str(clue['num']), 'word': clue['clue']}).text = clue['clue']
    for clue in numbering.down:
        ET.SubElement(down, 'clue', attrib={'number': str(clue['num']), 'word': clue['clue']}).text = clue['clue']

    tree = ET.ElementTree(root)
    tree.write(xml_file, encoding='utf-8', xml_declaration=True)

# uporaba
puz_to_xml('krizanka.puz', 'krizanka.xml')
