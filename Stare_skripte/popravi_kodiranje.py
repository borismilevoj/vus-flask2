import sqlite3

conn = sqlite3.connect('VUS.db')
cur = conn.cursor()

def popravi_znake(text):
    zamenjave = {
        'Ă„': 'Ä', 'Ă¤': 'ä',
        'Ă–': 'Ö', 'Ă¶': 'ö',
        'Ăś': 'ć', 'ĂĆ': 'Ć',
        'ĂĄ': 'á', 'Ăł': 'ó',
        'Ă©': 'é', 'Ă¨': 'è',
        'ĂŹ': 'Ż', 'Ăź': 'ü',
        'Ă ': 'à', 'ÄŤ': 'č',
        'ÄŚ': 'Č', 'Ä‡': 'ć',
        'Ä†': 'Ć', 'Ĺž': 'ž',
        'Ĺ˝': 'Ž', 'Ĺˇ': 'š',
        'Ĺ ': 'Š', 'Â': '',
        'Ä‘': 'đ', 'Ä': 'Đ',
        '??': '–', '?': 'č',
        '†': 'šč',
        ' ametno ': ' žametno ',
        'afri  ki': 'afriški',
        'ju  noafri  ki': 'južnoafriški',
        'dr  ava': 'država',
        'razli  ica': 'različica',
        'pu  avski': 'puščavski',
        'etni  na': 'etnična',
        'nizozem ine': 'nizozemščine',
        ' dru  ina': ' družina',
        ' ju  ni': ' južni',
        'severnoafri  ki': 'severnoafriški',
        'centralnoafri  ki': 'centralnoafriški',
        '†rn': 'črn',
        '  ': ' ',  # dvojni presledki v enojne
    }

    for napacno, pravilno in zamenjave.items():
        text = text.replace(napacno, pravilno)
    return text

cur.execute("SELECT rowid, OPIS FROM slovar")
zapisi = cur.fetchall()

print(f"Število vseh zapisov za pregled in popravek: {len(zapisi)}")

for idx, (rowid, opis) in enumerate(zapisi, start=1):
    popravljeno = popravi_znake(opis)
    if popravljeno != opis:  # posodobi samo, če je prišlo do spremembe
        cur.execute("UPDATE slovar SET OPIS = ? WHERE rowid = ?", (popravljeno, rowid))

    if idx % 1000 == 0:
        print(f"Pregledanih zapisov: {idx}/{len(zapisi)}")
        conn.commit()

conn.commit()
conn.close()

print("✅ Končano popravljanje znakov.")
