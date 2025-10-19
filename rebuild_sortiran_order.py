import sqlite3, os
p = r".\var\data\VUS.db"
con = sqlite3.connect(p)
cur = con.cursor()

cur.execute("BEGIN")
cur.execute("DELETE FROM slovar_sortiran")
cur.execute("""
INSERT OR IGNORE INTO slovar_sortiran(geslo, opis)
SELECT geslo, opis
FROM slovar
ORDER BY
  CASE
    WHEN instr(opis, ' - ') > 0
      THEN lower(trim(substr(opis, instr(opis, ' - ')+3)))
    ELSE lower(opis)
  END
""")
cur.execute("COMMIT")

# hitri prikaz reda za KEATON
rows = cur.execute(
    "SELECT opis FROM slovar_sortiran WHERE TRIM(geslo)=? COLLATE NOCASE",
    ("KEATON",)
).fetchall()
print("KEATON vrstni red po rebuildu:")
for (o,) in rows:
    print("→", o)

con.close()
print("OK:", os.path.abspath(p))
