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
con.close()
print("✅ slovar_sortiran osvežen:", os.path.abspath(p))
