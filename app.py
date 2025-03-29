from flask import Flask, render_template, request, jsonify,g
from flask import session, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'admin123'  # obvezno za delo s sejami
DATABASE = 'VUS.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS slovar (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            GESLO TEXT NOT NULL,
            OPIS TEXT NOT NULL
        )
    """)
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

@app.route('/isci_opis')
def isci_opis():
    return render_template("isci_opis.html", gesla=None)


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    napaka = ""
    if request.method == 'POST':
        password = request.form['password']
        if password == 'admin123':  # Geslo lahko spremeniš!
            session['admin'] = True
            return redirect('/admin')
        else:
            napaka = "Napačno geslo!"
    return render_template('login.html', napaka=napaka)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('admin'):
        return redirect('/login')

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

            # Sort po zadnjem vezaju
            gesla.sort(key=lambda x: (
                0 if '-' in x['opis'] else 1,
                x['opis'].rsplit('-', 1)[-1].strip().split(' ')[0].upper() if '-' in x['opis'] else x['opis']
            ))

            print("PO SORTIRANJU:")
            for g in gesla:
                print(g['opis'])

            return render_template("admin.html",
                                   gesla=gesla,
                                   sporocilo=sporocilo,
                                   rezultat_preverjanja=rezultat_preverjanja,
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

    # GET: Prazna tabela + števec
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



    # GET zahteva: prazen seznam gesel
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


@app.route('/isci_vzorec')
def isci_vzorec():
    return render_template('isci_vzorec.html')



@app.route('/preveri', methods=['POST'])
def preveri():
    rezultat = ""
    geslo = request.form['preveri_geslo'].strip()
    print(f"Preverjam geslo: {geslo}")
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
    cur.execute("SELECT * FROM slovar WHERE UPPER(GESLO) = UPPER(?)", (geslo,))
    gesla = cur.fetchall()
    cur.execute("SELECT COUNT(*) FROM slovar")
    stevilo = cur.fetchone()[0]

    return render_template("admin.html",
                           gesla=gesla,
                           sporocilo="",
                           rezultat_preverjanja=rezultat,
                           stevilo=stevilo)




@app.route('/uredi_geslo', methods=['POST'])
def uredi_geslo():
    podatki = request.form
    geslo_id = podatki.get('id')
    novi_opis = podatki.get('novi_opis')

    if geslo_id and novi_opis:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("UPDATE slovar SET OPIS=? WHERE ID=?", (novi_opis, geslo_id))
        conn.commit()

    # Po posodobitvi
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM slovar WHERE ID = ?", (geslo_id,))
    gesla = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM slovar")
    stevilo = cur.fetchone()[0]
    conn.close()

    return render_template("admin.html",
                           gesla=gesla,
                           sporocilo="Opis gesla uspešno posodobljen!",
                           rezultat_preverjanja="",
                           stevilo=stevilo)


@app.route('/izbrisi_geslo', methods=['POST'])
def izbrisi_geslo():
    if not session.get('admin'):
        return redirect('/login')

    geslo_id = request.form.get('id')

    if geslo_id:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM slovar WHERE ID=?", (geslo_id,))
        conn.commit()

        # Ponovno preverimo, če še obstajajo druga gesla z istim geslom
        geslo = request.form.get('geslo', '').strip()
        cur.execute("SELECT * FROM slovar WHERE UPPER(GESLO) = ?", (geslo.upper(),))
        gesla = cur.fetchall()
        cur.execute("SELECT COUNT(*) FROM slovar")
        stevilo = cur.fetchone()[0]
        conn.close()

        # Uredi po zadnjem vezaju
        gesla.sort(key=lambda x: (
            0 if '-' in x['opis'] else 1,
            x['opis'].rsplit('-', 1)[-1].strip().split(' ')[0].upper() if '-' in x['opis'] else x['opis']
        ))

        return render_template("admin.html",
                               gesla=gesla,
                               sporocilo="Geslo uspešno izbrisano!",
                               rezultat_preverjanja="",
                               stevilo=stevilo)



@app.route('/isci_po_vzorcu', methods=['POST'])
def isci_po_vzorcu():
    vzorec = request.form['vzorec'].strip().upper()
    dolzina = int(request.form['dolzina'])

    conn = sqlite3.connect('VUS.db')
    cur = conn.cursor()

    # Popolna ujemajoča dolžina in LIKE po vzorcu
    cur.execute(
        "SELECT TRIM(GESLO), OPIS FROM slovar WHERE LENGTH(TRIM(GESLO)) = ? AND GESLO LIKE ?",
        (dolzina, vzorec)
    )

    rezultati = cur.fetchall()
    print(f"[VZOREC] {vzorec} | [DOLŽINA] {dolzina} | [REZULTATI]: {len(rezultati)}")
    conn.close()

    gesla = [{'geslo': g, 'opis': o} for g, o in rezultati]

    return jsonify(gesla)

@app.route('/isci_po_opisu', methods=['POST', 'GET'])
def isci_po_opisu():
    kljucna_beseda = request.form['opis'].strip().upper() if request.method == 'POST' else ""

    if not kljucna_beseda:
        return render_template("isci_opis.html", gesla=None)

    conn = sqlite3.connect("VUS.db")
    cur = conn.cursor()

    besede = kljucna_beseda.split()

    pogoji = []
    params = []

    for beseda in besede:
        if beseda.isdigit():  # če je letnica, iščemo prosto
            pogoji.append("UPPER(OPIS) LIKE ?")
            params.append(f"%{beseda}%")
        else:  # sicer iščemo besedo kot samostojno
            pogoji.append("(UPPER(OPIS) LIKE ? OR UPPER(OPIS) LIKE ? OR UPPER(OPIS) LIKE ? OR UPPER(OPIS) LIKE ?)")
            params.extend([
                beseda + ' %',        # na začetku
                '% ' + beseda + ' %', # v sredini
                '% ' + beseda,        # na koncu
                beseda                # čista beseda
            ])

    sql = "SELECT GESLO, OPIS FROM slovar WHERE " + " AND ".join(pogoji)

    cur.execute(sql, params)
    rezultati = cur.fetchall()
    conn.close()

    gesla = [{'GESLO': g, 'OPIS': o} for g, o in rezultati]

    return render_template("isci_opis.html", gesla=gesla)




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
