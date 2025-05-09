# pretvori.py
with open('vus.sql', 'r', encoding='cp1250', errors='ignore') as vhodna:
    vsebina = vhodna.read()

with open('vus_utf8.sql', 'w', encoding='utf-8') as izhodna:
    izhodna.write(vsebina)
