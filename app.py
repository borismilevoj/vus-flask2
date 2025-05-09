from flask import Flask, request, jsonify, render_template, session
from pretvornik import normaliziraj_geslo
import sqlite3
import os
from werkzeug.utils import secure_filename
from krizanka import pridobi_podatke_iz_xml
conn = sqlite3.connect('VUS.db', check_same_thread=False)


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
def preveri():
    geslo = request.json['geslo'].upper().strip()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ID, geslo, opis FROM slovar
        WHERE UPPER(REPLACE(geslo, ' ', '')) = ?
    """, (geslo.replace(' ', '').upper(),))

    rezultati = cursor.fetchall()
    obstaja = len(rezultati) > 0

    return jsonify({
        'obstaja': obstaja,
        'gesla': [{'id': id, 'geslo': g, 'opis': o} for id, g, o in rezultati]
    })


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
    data = request.json
    id = data['id']
    opis = data['opis']
    cursor = conn.cursor()
    cursor.execute("UPDATE slovar SET opis=? WHERE ID=?", (opis, id))
    conn.commit()
    return jsonify({'sporocilo': 'Opis uspešno spremenjen'})

@app.route('/brisi_geslo', methods=['POST'])
def brisi_geslo():
    data = request.json
    id = data['id']
    cursor = conn.cursor()
    cursor.execute("DELETE FROM slovar WHERE ID=?", (id,))
    conn.commit()
    return jsonify({'sporocilo': 'Geslo izbrisano'})


@app.route('/isci_vzorec', methods=['GET', 'POST'])
def isci_vzorec():
    if request.method == 'POST':
        data = request.get_json()
        vzorec = data.get('vzorec').upper()
        dodatno = data.get('dodatno', '')

        # Odstrani prazne znake, pusti samo črke
        dolzina_vzorca = len(vzorec)

        conn = get_db()
        cursor = conn.cursor()

        query = """
            SELECT GESLO, OPIS FROM slovar
            WHERE LENGTH(REPLACE(REPLACE(REPLACE(GESLO, ' ', ''), '-', ''), '_', '')) = ?
            AND OPIS LIKE ?
        """

        params = [dolzina_vzorca, f'%{dodatno}%']

        # Dodaj preverjanje vsake črke posebej
        for i, crka in enumerate(vzorec):
            if crka != '_':
                query += f" AND SUBSTR(REPLACE(REPLACE(REPLACE(GESLO, ' ', ''), '-', ''), '_', ''), {i+1}, 1) = ?"
                params.append(crka)

        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()

        return jsonify([{"GESLO": row["GESLO"].strip(), "OPIS": row["OPIS"]} for row in results])

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
    original = data.get('original').strip()
    zamenjava = data.get('zamenjava').strip()

    conn = get_db()
    cur = conn.cursor()

    # Najprej preštej, koliko zapisov se ujema z originalnim izrazom
    cur.execute("SELECT COUNT(*) FROM slovar WHERE OPIS LIKE ?", (f"%{original}%",))
    stevilo_zadetkov = cur.fetchone()[0]

    if stevilo_zadetkov > 0:
        cur.execute("UPDATE slovar SET OPIS = REPLACE(OPIS, ?, ?) WHERE OPIS LIKE ?",
                    (original, zamenjava, f"%{original}%"))
        conn.commit()

    conn.close()

    # Vrni število dejanskih sprememb
    return jsonify({"spremembe": stevilo_zadetkov})


if __name__ == '__main__':
    app.run(debug=True, port=10000)
