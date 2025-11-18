import csv
fin = r'out/cc_clues_UTF8.csv'
fout = r'out/cc_clues_for_add_utf8.txt'
with open(fin, encoding='utf-8-sig', newline='') as f, open(fout, 'w', encoding='utf-8-sig', newline='') as g:
    r = csv.DictReader(f)
    for row in r:
        ans  = (row.get('Answer') or '').strip()
        clue = (row.get('Clue') or '').strip()
        if ans:
            g.write(ans + '\t' + clue + '\r\n')  # CRLF, UTF-8-BOM
print('OK:', fout)
