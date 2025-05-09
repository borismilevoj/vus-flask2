import sqlite3
from collections import Counter
import re

conn = sqlite3.connect('VUS.db')
cur = conn.cursor()

cur.execute("SELECT OPIS FROM slovar WHERE OPIS LIKE '%†%'")
zapisi = cur.fetchall()

# Poiščemo besede, ki vsebujejo '†'
besede_z_napako = Counter()

for (opis,) in zapisi:
    # Razdelimo opis na posamezne besede
    besede = opis.split()
    for beseda in besede:
        if '†' in beseda and not re.match(r'\(\d{4}†\d{4}\)', beseda):
            besede_z_napako[beseda] += 1

# Izpišemo najpogostejše napačne besede
for beseda, pogostost in besede_z_napako.most_common(50):
    print(beseda, pogostost)

conn.close()
