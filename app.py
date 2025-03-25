
from flask import Flask, render_template, request, g
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'VUS.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS slovar (ID INTEGER PRIMARY KEY AUTOINCREMENT, GESLO TEXT NOT NULL, OPIS TEXT NOT NULL)")
    conn.commit()
    conn.close()

init_db()

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    sporocilo = ""
    rezultat_preverjanja = ""
    if request.method == 'POST':
        geslo = request.form['geslo'].strip()
        opis = request.form['opis'].strip()
        if geslo and opis:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO slovar (GESLO, OPIS) VALUES (?, ?)", (geslo, opis))
            conn.commit()
            sporocilo = f"Geslo '{geslo}' uspešno dodano!"

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM slovar ORDER BY ID DESC")
    gesla = cur.fetchall()
    cur.execute("SELECT COUNT(*) FROM slovar")
    stevilo = cur.fetchone()[0]

    return render_template("admin.html", gesla=gesla, sporocilo=sporocilo, rezultat_preverjanja=rezultat_preverjanja, stevilo=stevilo)

@app.route('/preveri', methods=['POST'])
def preveri():
    rezultat = ""
    geslo = request.form['preveri_geslo'].strip()

    if geslo:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM slovar WHERE UPPER(GESLO) = UPPER(?)", (geslo,))
        obstaja = cur.fetchone()[0]

        if obstaja:
            rezultat = f"Geslo '{geslo}' že obstaja v bazi."
        else:
            rezultat = f"Geslo '{geslo}' še ne obstaja."

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM slovar ORDER BY ID DESC")
    gesla = cur.fetchall()
    cur.execute("SELECT COUNT(*) FROM slovar")
    stevilo = cur.fetchone()[0]

    return render_template("admin.html", gesla=gesla, sporocilo="", rezultat_preverjanja=rezultat, stevilo=stevilo)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
