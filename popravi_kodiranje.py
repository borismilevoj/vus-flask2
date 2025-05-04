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
        '??': '–', '?': 'č'
    }

    for napacno, pravilno in zamenjave.items():
        text = text.replace(napacno, pravilno)
    return text

cur.execute("SELECT rowid, OPIS FROM slovar WHERE OPIS LIKE '%?%'")
zapisi = cur.fetchall()

print(f"Število zapisov za popravit: {len(zapisi)}")

for idx, (rowid, opis) in enumerate(zapisi, start=1):
    popravljeno = popravi_znake(opis)
    cur.execute("UPDATE slovar SET OPIS = ? WHERE rowid = ?", (popravljeno, rowid))

    if idx % 1000 == 0:
        print(f"Popravljenih zapisov: {idx}/{len(zapisi)}")
        conn.commit()

conn.commit()
conn.close()

print("Končano popravljanje znakov.")
