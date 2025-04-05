from flask import Flask, render_template, request, redirect, session, jsonify, g
from flask_cors import CORS  # ✅ omogoči CORS

import sqlite3
import os
import re
import unicodedata

app = Flask(__name__)
CORS(app)  # ✅ omogoči CORS za celotno aplikacijo



app = Flask(__name__)
app.secret_key = 'Tifumannam1VUS_flask2'
DATABASE = 'VUS.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def normalize(text):
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII').lower()

def extract_ime(opis):
    if '-' in opis:
        kandidat = opis.rsplit('-', 1)[-1].strip()
        ime = re.split(r'\s*\(', kandidat)[0].strip()
        if ime and ime[0].isupper():
            return normalize(ime)
    return 'zzzzzzzz'

@app.route('/')
def index():
    return render_template('index.html')



@app.route("/isci_opis")
def isci_opis():
    return render_template("isci_opis.html")



@app.route('/isci_po_opisu', methods=['POST'])
def isci_po_opisu():
    kljucne_besede = request.form['opis'].strip().upper()

    if not kljucne_besede:
        return jsonify({'error': 'Vnesi ključno besedo za iskanje po opisu.'}), 400

    besede = kljucne_besede.split()
    pogoji = []
    params = []

    for beseda in besede:
        pogoji.append(
            "(UPPER(OPIS) LIKE ? OR UPPER(OPIS) LIKE ? OR UPPER(OPIS) LIKE ? OR UPPER(OPIS) = ?)"
        )
        params.extend([
            beseda + ' %',        # na začetku
            '% ' + beseda + ' %', # v sredini
            '% ' + beseda,        # na koncu
            beseda                # samo beseda
        ])

    sql = "SELECT GESLO, OPIS FROM slovar WHERE " + " AND ".join(pogoji)

    conn = get_db()
    cur = conn.cursor()
    cur.execute(sql, params)
    rezultati = cur.fetchall()
    conn.close()

    gesla = [{'geslo': g, 'opis': o} for g, o in rezultati]
    return jsonify(gesla)





@app.route('/isci_vzorec')
def isci_vzorec():
    return render_template("isci_vzorec.html")


@app.route('/isci_po_vzorcu', methods=['POST'])
def isci_po_vzorcu():
    vzorec = request.form['vzorec'].strip().upper()
    dolzina = int(request.form['dolzina'])

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT GESLO, OPIS FROM slovar WHERE LENGTH(GESLO) = ? AND GESLO LIKE ?", (dolzina, vzorec))
    rezultati = cur.fetchall()
    conn.close()

    gesla = [{'geslo': g, 'opis': o} for g, o in rezultati]

    # 🔠 Sortiraj po geslu (ali po opisu, če želiš)
    gesla.sort(key=lambda x: x['geslo'])  # lahko zamenjaš z x['opis']

    return jsonify(gesla)


@app.route('/login', methods=['GET', 'POST'])
def login():
    napaka = ""
    if request.method == 'POST':
        geslo = request.form['geslo']
        if geslo == 'admin123':
            session['admin'] = True
            return redirect('/admin')
        else:
            napaka = "Napačno geslo."
    return render_template("login.html", napaka=napaka)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    #if not session.get('admin'):
    #    return redirect('/login')

    sporocilo = ""
    rezultat_preverjanja = ""
    gesla = []

    if request.method == 'POST':
        geslo = request.form['geslo'].strip()
        opis = request.form['opis'].strip()

        if geslo and opis:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO slovar (GESLO, OPIS) VALUES (?, ?)", (geslo.upper(), opis))
            conn.commit()
            cur.execute("SELECT * FROM slovar WHERE UPPER(GESLO) = ?", (geslo.upper(),))
            gesla = cur.fetchall()
            gesla.sort(key=lambda x: extract_ime(x['opis']))
            cur.execute("SELECT COUNT(*) FROM slovar")
            stevilo = cur.fetchone()[0]
            conn.close()

            return render_template("admin.html", gesla=gesla, sporocilo="Geslo uspešno dodano!", rezultat_preverjanja="", stevilo=stevilo)

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM slovar")
    stevilo = cur.fetchone()[0]
    conn.close()

    return render_template("admin.html", gesla=[], sporocilo="", rezultat_preverjanja="", stevilo=stevilo)

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
        cur.execute("SELECT * FROM slovar WHERE UPPER(GESLO) = UPPER(?)", (geslo,))
        gesla = cur.fetchall()
        gesla.sort(key=lambda x: extract_ime(x['opis']))
        cur.execute("SELECT COUNT(*) FROM slovar")
        stevilo = cur.fetchone()[0]
        conn.close()

        return render_template("admin.html", gesla=gesla, sporocilo="", rezultat_preverjanja=rezultat, stevilo=stevilo)

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM slovar")
    stevilo = cur.fetchone()[0]
    conn.close()

    return render_template("admin.html", gesla=[], sporocilo="", rezultat_preverjanja=rezultat, stevilo=stevilo)

@app.route('/uredi_geslo', methods=['POST'])
def uredi_geslo():
    id = request.form['id']
    novi_opis = request.form['novi_opis'].strip()

    if id and novi_opis:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("UPDATE slovar SET OPIS = ? WHERE ID = ?", (novi_opis, id))
        conn.commit()
        cur.execute("SELECT * FROM slovar WHERE ID = ?", (id,))
        gesla = cur.fetchall()
        gesla.sort(key=lambda x: extract_ime(x['opis']))
        cur.execute("SELECT COUNT(*) FROM slovar")
        stevilo = cur.fetchone()[0]
        conn.close()

        return render_template("admin.html", gesla=gesla, sporocilo="Opis posodobljen!", rezultat_preverjanja="", stevilo=stevilo)

    return redirect("/admin")

@app.route('/izbrisi_geslo', methods=['POST'])
def izbrisi_geslo():
    id = request.form['id']

    if id:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM slovar WHERE ID = ?", (id,))
        conn.commit()
        conn.close()

    return redirect("/admin")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)