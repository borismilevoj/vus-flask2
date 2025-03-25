from flask import Flask, render_template, request, g
import sqlite3
import os
import logging
logging.basicConfig(level=logging.INFO)


app = Flask(__name__)

def init_db():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS slovar (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            GESLO TEXT NOT NULL,
            OPIS TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Ustvari tabelo ob zagonu aplikacije
init_db()


# --- Povezava z bazo ---
DATABASE = 'VUS.db'

# TEST: prisiljen deploy po init_db


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

# --- Domača stran ---
@app.route('/')
def index():
    return render_template('index.html')

# --- /home stran ---
@app.route('/home')
def home():
    return render_template('home.html')

# --- /admin stran z obrazcem ---

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    logging.info(f"Zahteva na /admin: {request.method}")

    sporocilo = ""

    if request.method == 'POST':
        geslo = request.form['geslo'].strip()
        opis = request.form['opis'].strip()

        if geslo and opis:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO slovar (GESLO, OPIS) VALUES (?, ?)", (geslo, opis))
            conn.commit()
            sporocilo = f"Geslo '{geslo}' uspešno dodano!"

    # Prikaz vseh vnosov
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM slovar ORDER BY ID DESC")
    gesla = cur.fetchall()

    return render_template('admin.html', sporocilo=sporocilo, gesla=gesla)


# --- Zagon aplikacije ---
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
