import xml.etree.ElementTree as ET
from pathlib import Path

xml_name = input("Ime XML datoteke: ").strip()

if not xml_name.endswith(".xml"):
    xml_name += ".xml"

xml_file = Path(xml_name)
out_file = xml_file.with_name(xml_file.stem + "_clues.txt")

tree = ET.parse(xml_file)
root = tree.getroot()

def local_name(tag):
    return tag.split("}")[-1] if "}" in tag else tag

count = 0

with out_file.open("w", encoding="utf-8") as f:
    for elem in root.iter():
        if local_name(elem.tag) == "clue":
            number = (elem.get("number") or "").strip()
            word = (elem.get("word") or "").strip()
            citation = (elem.get("citation") or "").strip()
            text = "".join(elem.itertext()).strip()

            if text:
                line = f'{number} | word={word} | citation={citation} | {text}'
                print(line)
                f.write(line + "\n")
                count += 1

print(f"\nNajdenih opisov: {count}")
print(f"Shranjeno v: {out_file}")