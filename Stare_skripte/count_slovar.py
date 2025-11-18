import sqlite3, sys
p = sys.argv[1]
try:
    con = sqlite3.connect(p)
    cur = con.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='slovar'")
    if not cur.fetchone():
        print(-1); con.close(); sys.exit(0)
    n = con.execute("SELECT COUNT(*) FROM slovar").fetchone()[0]
    print(n); con.close()
except Exception as e:
    print(-2)
