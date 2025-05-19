from flask import Flask, request, jsonify, render_template,  redirect, url_for,session, render_template_string
from datetime import datetime
from pretvornik import normaliziraj_geslo
import sqlite3
import os
from flask import send_from_directory
from werkzeug.utils import secure_filename
from krizanka import pridobi_podatke_iz_xml
conn = sqlite3.connect('VUS.db', check_same_thread=False)
from uvoz_datotek import premakni_krizanke, premakni_sudoku


app = Flask(__name__, static_folder='static', static_url_path='/static')
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

@app.route("/ping")
def ping():
    return "OK iz Flaska!"


@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/')
def redirect_to_home():
    return redirect(url_for('home'))


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

@app.route('/test_iscenje')
def test_iscenje():
    return render_template('isci_vzorec_test.html')


@app.route('/isci_vzorec', methods=['GET', 'POST'])
def isci_vzorec():
    if request.method == 'POST':
        print("🔎 Zahtevek s telefona?")
        print("request.is_json:", request.is_json)
        print("request.data:", request.data)
        print("request.get_json():", request.get_json(silent=True))
        if not request.is_json:
            return jsonify([])

        data = request.get_json(silent=True)
        if not data or 'vzorec' not in data:
            return jsonify([])

        vzorec = data.get('vzorec', '').upper()
        dodatno = data.get('dodatno', '')

        dolzina_vzorca = len(vzorec)

        conn = get_db()
        cursor = conn.cursor()

        query = """
            SELECT GESLO, OPIS FROM slovar
            WHERE LENGTH(REPLACE(REPLACE(REPLACE(GESLO, ' ', ''), '-', ''), '_', '')) = ?
            AND OPIS LIKE ?
        """
        params = [dolzina_vzorca, f'%{dodatno}%']

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

# Ta route mora biti ZUNAJ vseh funkcij!
@app.route('/krizanka/static/<path:filename>')
def krizanka_static_file(filename):
    pot = os.path.join('static', 'Krizanke', 'CrosswordCompilerApp')
    return send_from_directory(pot, filename)


@app.route('/krizanka', defaults={'datum': None})
@app.route('/krizanka/<datum>')
def prikazi_krizanko(datum):
    if datum is None:
        datum = datetime.today().strftime('%Y-%m-%d')

    ime_datoteke = f'{datum}.xml'
    osnovna_pot = os.path.dirname(os.path.abspath(__file__))
    pot_do_datoteke = os.path.join(osnovna_pot, 'static', 'CrosswordCompilerApp', ime_datoteke)

    if not os.path.exists(pot_do_datoteke):
        return render_template('napaka.html', sporocilo="Križanka za ta datum še ni objavljena.")

    podatki = pridobi_podatke_iz_xml(pot_do_datoteke)
    return render_template('krizanka.html', podatki=podatki)





from datetime import datetime

@app.route('/krizanka/arhiv')
def arhiv_krizank():
    mapa = os.path.join('static', 'CrosswordCompilerApp')
    danes = datetime.today().strftime('%Y-%m-%d')

    datoteke = []
    for f in os.listdir(mapa):
        if f.endswith('.xml'):
            datum = f.replace('.xml', '')
            try:
                datetime.strptime(datum, "%Y-%m-%d")  # preveri, da je pravi format
                if datum < danes:
                    datoteke.append(datum)
            except ValueError:
                pass  # preskoči napačne datoteke

    datoteke.sort(reverse=True)
    return render_template('arhiv.html', datumi=datoteke)




@app.route('/sudoku')
def osnovni_sudoku():
    return redirect(url_for('prikazi_danasnji_sudoku', tezavnost='easy'))

@app.route('/sudoku/<tezavnost>/<datum>')
def prikazi_sudoku(tezavnost, datum):
    mapa_sudoku = f"Sudoku_{tezavnost}"
    ime_datoteke = f"Sudoku_{tezavnost}_{datum}.html"
    pot_do_datoteke = os.path.join('static', mapa_sudoku, ime_datoteke)

    if not os.path.exists(pot_do_datoteke):
        return render_template('napaka.html', sporocilo="Sudoku za ta datum ali težavnost ni na voljo.")

    with open(pot_do_datoteke, 'r', encoding='utf-8') as f:
        vsebina = f.read()

    return render_template_string(vsebina)

@app.route('/sudoku/<tezavnost>')
def prikazi_danasnji_sudoku(tezavnost):
    danes = datetime.today().strftime('%Y-%m-%d')
    return redirect(url_for('prikazi_sudoku', tezavnost=tezavnost, datum=danes))

@app.route('/sudoku/meni')
def sudoku_meni():
    return render_template('sudoku_meni.html')


from datetime import datetime

@app.route('/sudoku/arhiv/<tezavnost>')
def arhiv_sudoku(tezavnost):
    mapa_sudoku = os.path.join('static', f"Sudoku_{tezavnost}")
    danes = datetime.today().strftime('%Y-%m-%d')

    datumi = []
    for f in os.listdir(mapa_sudoku):
        if f.endswith('.html'):
            datum = f.replace(f'Sudoku_{tezavnost}_', '').replace('.html', '')
            try:
                datetime.strptime(datum, "%Y-%m-%d")
                if datum < danes:
                    datumi.append(datum)
            except ValueError:
                pass

    datumi.sort(reverse=True)
    return render_template('sudoku_arhiv.html', datumi=datumi, tezavnost=tezavnost)


@app.route('/sudoku/arhiv')
def arhiv_sudoku_pregled():
    return render_template('sudoku_arhiv_glavni.html')

from flask import request, flash, redirect, url_for

@app.route('/uvoz', methods=['GET', 'POST'])
def uvoz_datotek():
    if request.method == 'POST':
        tip = request.form.get('tip')
        if tip == 'krizanka':
            premakni_krizanke()
            flash("Križanke so bile uspešno uvožene.", "success")
        elif tip == 'sudoku':
            tezavnost = request.form.get('tezavnost')
            premakni_sudoku(tezavnost)
            flash(f"Sudoku ({tezavnost}) je bil uspešno uvožen.", "success")
        else:
            flash("Neznan tip uvoza.", "danger")
        return redirect(url_for('uvoz_datotek'))

    return render_template('uvoz.html')


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
    app.run(debug=True, host='0.0.0.0')