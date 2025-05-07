from flask import Flask, request, jsonify, render_template, session
from pretvornik import normaliziraj_geslo
import sqlite3
import os
from werkzeug.utils import secure_filename
from krizanka import pridobi_podatke_iz_xml


app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'tvoja_skrivna_koda'

app.config['UPLOAD_FOLDER'] = 'static/uploads'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


# Database connection
def get_db():
    conn = sqlite3.connect('VUS.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/preveri', methods=['POST'])
def preveri_geslo():
    data = request.get_json()
    geslo = data['geslo'].strip().upper()

    conn = sqlite3.connect('VUS.db')
    cur = conn.cursor()

    # Dodan TRIM(), da odstrani presledke iz baze
    cur.execute("SELECT geslo, opis FROM slovar WHERE TRIM(UPPER(geslo)) = ?", (geslo,))
    vrstice = cur.fetchall()

    conn.close()

    if vrstice:
        return jsonify({"obstaja": True, "gesla": [{"geslo": v[0].strip(), "opis": v[1]} for v in vrstice]})
    else:
        return jsonify({"obstaja": False})




@app.route('/dodaj_geslo', methods=['POST'])
def dodaj_geslo():
    data = request.json
    geslo = data.get('geslo')
    opis = data.get('opis')

    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO slovar (GESLO, OPIS) VALUES (?, ?)", (geslo, opis))
    conn.commit()
    conn.close()

    return jsonify({"status": "uspesno", "sporocilo": "Geslo uspešno dodano!"})

# UREJANJE GESLA

@app.route('/uredi_geslo', methods=['POST'])
def uredi_geslo():
    data = request.get_json()
    geslo = data['geslo']
    nov_opis = data['opis']

    conn = sqlite3.connect('VUS.db')
    cur = conn.cursor()
    cur.execute("UPDATE slovar SET opis = ? WHERE TRIM(UPPER(geslo)) = ?", (nov_opis, geslo.upper()))
    conn.commit()
    conn.close()

    return jsonify({"sporocilo": f"Geslo '{geslo}' je uspešno posodobljeno."})


# BRISANJE
@app.route('/brisi_geslo', methods=['POST'])
def brisi_geslo():
    data = request.get_json()
    geslo = data['geslo']

    conn = sqlite3.connect('VUS.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM slovar WHERE TRIM(UPPER(geslo)) = ?", (geslo.upper(),))
    conn.commit()
    conn.close()

    return jsonify({"sporocilo": f"Geslo '{geslo}' je bilo uspešno izbrisano."})


@app.route('/isci_vzorec', methods=['GET', 'POST'])
def isci_vzorec():
    if request.method == 'POST':
        data = request.get_json()
        vzorec = data.get('vzorec').replace('_', '_')  # tukaj ne spreminjaš nič
        dodatno = data.get('dodatno')
        dolzina_vzorca = len(data.get('vzorec'))

        conn = get_db()
        cursor = conn.cursor()

        query = """
            SELECT GESLO, OPIS FROM slovar 
            WHERE GESLO LIKE ? 
            AND LENGTH(GESLO) = ? 
            AND OPIS LIKE ? LIMIT 100
        """

        cursor.execute(query, (vzorec, dolzina_vzorca, f'%{dodatno}%'))
        results = cursor.fetchall()
        conn.close()

        return jsonify([{"GESLO": row["GESLO"], "OPIS": row["OPIS"]} for row in results])

    else:
        return render_template('isci_vzorec.html')



@app.route('/isci_opis', methods=['GET', 'POST'])
def isci_opis():
    if request.method == 'POST':
        podatki = request.get_json()
        opis = podatki.get('opis', '')

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT GESLO, OPIS FROM slovar WHERE OPIS LIKE ? LIMIT 100", (f"%{opis}%",))
        rezultat = cursor.fetchall()
        conn.close()

        return jsonify([{'GESLO': r['GESLO'], 'OPIS': r['OPIS']} for r in rezultat])

    return render_template('isci_opis.html')


@app.route('/prispevaj_geslo')
def prispevaj_geslo():
    return render_template('prispevaj.html')


@app.route('/stevec_gesel')
def stevec_gesel():
    conn = sqlite3.connect('VUS.db')
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM slovar")
    steviloGesel = cur.fetchone()[0]
    conn.close()
    return jsonify({"steviloGesel": steviloGesel})





@app.route('/krizanka')
def prikazi_krizanko():
    podatki = pridobi_podatke_iz_xml('1.xml')
    return render_template('krizanka.html', podatki=podatki)

@app.route('/krizanke')
def krizanke():
    return render_template('krizanke.html')


@app.route('/sudoku', methods=['GET', 'POST'])
def sudoku():
    tezavnosti = {
        'lažja': 'easy',
        'srednja': 'medium',
        'težka': 'hard',
        'najtežja': 'very_hard'
    }
    izbrana_tezavnost = None
    tezavnost_datoteka = None

    if request.method == 'POST':
        izbrana_tezavnost = request.form.get('tezavnost')
        tezavnost_datoteka = tezavnosti.get(izbrana_tezavnost)

    return render_template('sudoku.html',
                           tezavnosti=tezavnosti,
                           izbrana_tezavnost=izbrana_tezavnost,
                           tezavnost_datoteka=tezavnost_datoteka)


@app.route('/zamenjaj', methods=['POST'])
def zamenjaj():
    data = request.json
    original = data.get('original')
    zamenjava = data.get('zamenjava')

    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE slovar SET OPIS = REPLACE(OPIS, ?, ?) WHERE OPIS LIKE ?",
                (original, zamenjava, f"%{original}%"))
    spremembe = cur.rowcount
    conn.commit()
    conn.close()

    return jsonify({"spremembe": spremembe})

if __name__ == '__main__':
    app.run(debug=True, port=10000)
