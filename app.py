from flask import Flask, render_template, request, jsonify, g, session, redirect
import sqlite3
import os
import re
import unicodedata

app = Flask(__name__)
app.secret_key = 'Tifumannam1VUS_flask2'  # obvezno za delo s sejo
DATABASE = 'VUS.db'

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

def normalize(text):
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII').lower()


def extract_ime(opis):
    if '-' in opis:
        kandidat = opis.rsplit('-', 1)[-1].strip()
        ime = re.split(r'\s*\(', kandidat)[0].strip()
        if ime and ime[0].isupper():
            return normalize(ime)
    return 'zzz'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    napaka = ""
    if request.method == 'POST':
        geslo = request.form['password']
        if geslo == 'admin123':
            session['admin'] = True
            return redirect('/admin')
        else:
            napaka = "Napačno geslo!"
    return render_template('login.html', napaka=napaka)



@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('admin'):
        return redirect('/login')

    import unicodedata
    import re

    def normalize(text):
        return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII').lower()

    def extract_ime(opis):
        if '-' in opis:
            kandidat = opis.rsplit('-', 1)[-1].strip()
            ime = re.split(r'\s*\(', kandidat)[0].strip()
            if ime and ime[0].isupper():
                return normalize(ime)
        return 'zzz'  # če ni z veliko črko, gre na konec

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
            cur.execute("SELECT COUNT(*) FROM slovar")
            stevilo = cur.fetchone()[0]
            conn.close()

            gesla.sort(key=lambda x: extract_ime(x['opis']))

            return render_template("admin.html",
                                   gesla=gesla,
                                   sporocilo="Geslo uspešno dodano!",
                                   rezultat_preverjanja="",
                                   stevilo=stevilo)

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM slovar")
    stevilo = cur.fetchone()[0]
    conn.close()

    return render_template("admin.html",
                           gesla=[],
                           sporocilo="",
                           rezultat_preverjanja="",
                           stevilo=stevilo)


# =====================PREVERI =================================


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

        cur.execute("SELECT * FROM slovar WHERE UPPER(GESLO) = ?", (geslo.upper(),))
        gesla = cur.fetchall()
        cur.execute("SELECT COUNT(*) FROM slovar")
        stevilo = cur.fetchone()[0]
        conn.close()

        gesla.sort(key=lambda x: extract_ime(x['opis']))

        return render_template("admin.html",
                               gesla=gesla,
                               sporocilo="",
                               rezultat_preverjanja=rezultat,
                               stevilo=stevilo)

    return redirect("/admin")

@app.route('/uredi_geslo', methods=['POST'])
def uredi_geslo():
    geslo_id = request.form['id']
    novi_opis = request.form['novi_opis']

    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE slovar SET OPIS=? WHERE ID=?", (novi_opis, geslo_id))
    conn.commit()
    cur.execute("SELECT * FROM slovar WHERE ID = ?", (geslo_id,))
    gesla = cur.fetchall()
    cur.execute("SELECT COUNT(*) FROM slovar")
    stevilo = cur.fetchone()[0]
    conn.close()

    gesla.sort(key=lambda x: extract_ime(x['opis']))

    return render_template("admin.html",
                           gesla=gesla,
                           sporocilo="Opis gesla uspešno posodobljen!",
                           rezultat_preverjanja="",
                           stevilo=stevilo)

@app.route('/izbrisi_geslo', methods=['POST'])
def izbrisi_geslo():
    geslo_id = request.form['id']

    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM slovar WHERE ID=?", (geslo_id,))
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM slovar")
    stevilo = cur.fetchone()[0]
    conn.close()

    return render_template("admin.html",
                           gesla=[],
                           sporocilo="Geslo uspešno izbrisano!",
                           rezultat_preverjanja="",
                           stevilo=stevilo)

@app.route('/isci_vzorec')
def isci_vzorec():
    return render_template('isci_vzorec.html')

@app.route('/isci_po_vzorcu', methods=['POST'])
def isci_po_vzorcu():
    vzorec = request.form['vzorec'].strip().upper()
    dolzina = int(request.form['dolzina'])

    conn = sqlite3.connect('VUS.db')
    cur = conn.cursor()
    cur.execute("SELECT GESLO, OPIS FROM slovar WHERE LENGTH(GESLO) = ? AND GESLO LIKE ?", (dolzina, vzorec))
    rezultati = cur.fetchall()
    conn.close()

    gesla = [{'geslo': g, 'opis': o} for g, o in rezultati]

    return jsonify(gesla)

@app.route('/isci_opis')
def isci_opis():
    return render_template('isci_opis.html')

@app.route('/isci_po_opisu', methods=['POST'])
def isci_po_opisu():
    kljucna_beseda = request.form['opis'].strip().upper()

    if not kljucna_beseda:
        return jsonify({'error': 'Vnesi ključno besedo za iskanje po opisu.'}), 400

    conn = sqlite3.connect('VUS.db')
    cur = conn.cursor()

    besede = kljucna_beseda.split()
    pogoji = []
    params = []

    for beseda in besede:
        if beseda.isdigit():
            pogoji.append("UPPER(OPIS) LIKE ?")
            params.append(f"%{beseda}%")
        else:
            pogoji.append("(UPPER(OPIS) LIKE ? OR UPPER(OPIS) LIKE ? OR UPPER(OPIS) LIKE ? OR UPPER(OPIS) LIKE ?)")
            params.extend([
                beseda + ' %',
                '% ' + beseda + ' %',
                '% ' + beseda,
                beseda
            ])

    sql = "SELECT GESLO, OPIS FROM slovar WHERE " + " AND ".join(pogoji)
    cur.execute(sql, params)
    rezultati = cur.fetchall()
    conn.close()

    gesla = [{'geslo': g, 'opis': o} for g, o in rezultati]

    return jsonify(gesla)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
