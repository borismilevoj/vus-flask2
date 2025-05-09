import sqlite3

conn = sqlite3.connect('VUS.db')
cur = conn.cursor()

zamenjave = {
    'šč': '†',
    'ščvici': 'Švici',
    'ščvica': 'Švica',
    'ščupaniji': 'županiji',
    'ščupanija': 'županija',
    ' nogometašč': ' nogometaš -',
    ' tekašč': ' tekač -',
    ' športnašč': ' športna š',
    'pristanišč e': 'pristanišče',
    'ščlovek': 'človek',
    'zaradišč': 'zaradi š',
    'ščiv': 'živ',
    'šču elkah': 'ščurelkah',
    'ščrk': 'črk',
    'ščrko': 'črko',
    'ščad': 'Čad',
    'ščkotske': 'Škotske',
    'ščpaniji': 'Španiji',
    'ščok': '– ok.',
    'ščportna': 'športna',
    'ščahovski': 'šahovski',
    'ščrkarska': 'črkarska',
    ' mednarodnišč': ' mednarodni š',
    ' zaradiščiv': ' zaradi živ',
    'ščena': 'ščena',
    'ščad': 'Čad',
    ' Mad arska': ' Madžarska',
    ' mjanmarsko-indijski mednarodniščahovski mojster': ' mjanmarsko-indijski mednarodni šahovski mojster',
}

popravljenih_skupaj = 0

for original, popravljeno in zamenjave.items():
    cur.execute("UPDATE slovar SET OPIS = REPLACE(OPIS, ?, ?) WHERE OPIS LIKE ?",
                (original, popravljeno, f'%{original}%'))
    stevilo = cur.rowcount
    popravljenih_skupaj += stevilo
    conn.commit()
    print(f"Zamenjanih '{original}' → '{popravljeno}': {stevilo}")

conn.close()

print(f"✅ Skupno popravljenih zapisov: {popravljenih_skupaj}")
