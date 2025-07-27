from flask import Flask, jsonify, session, redirect, url_for, request, render_template, flash, send_from_directory
from functools import wraps
import sqlite3
import os
import glob
import unicodedata
import re
from krizanka import pridobi_podatke_iz_xml
from Stare_skripte.uvoz_datotek import premakni_krizanke, premakni_sudoku
from arhiviranje_util import arhiviraj_danes
import shutil
from datetime import datetime

# **Samo ENA inicializacija!**
app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = "skrivnost"
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['PROPAGATE_EXCEPTIONS'] = True

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

GESLO = "Tifumannam1_vus-flask2.onrender.com"

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'prijavljen' not in session:
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    napaka = None
    if request.method == 'POST':
        if request.form.get('geslo') == GESLO:
            session['prijavljen'] = True
            next_url = request.args.get('next') or url_for('home')
            return redirect(next_url)
        else:
            napaka = "Napačno geslo."
    return render_template('login.html', napaka=napaka)

@app.route('/logout')
def logout():
    session.pop('prijavljen', None)
    return redirect(url_for('login'))

def generiraj_ime_slike(opis, resitev):
    def norm(txt):
        txt = unicodedata.normalize('NFD', txt)
        txt = re.sub(r'[\u0300-\u036f]', '', txt)
        txt = txt.lower()
        txt = re.sub(r'[^a-z0-9 ]', '', txt)
        txt = '_'.join(txt.strip().split())
        return txt
    return f"{norm(opis)}_{norm(resitev)}"

def odstrani_cc_vrstico_iz_html(mapa):
    for datoteka in glob.glob(os.path.join(mapa, "*.html")):
        with open(datoteka, 'r', encoding='utf-8', errors='ignore') as f:
            vrstice = f.readlines()
        nove = [vr for vr in vrstice if "crossword-compiler.com" not in vr]
        if len(nove) < len(vrstice):
            with open(datoteka, 'w', encoding='utf-8') as f:
                f.writelines(nove)
            print(f"✂️ Očiščeno: {datoteka}")

import os
def get_db():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "VUS.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/admin/arhiviraj', methods=['POST'])
def sprozi_arhiviranje():
    premaknjeni = arhiviraj_danes()
    flash(f"Premaknjenih {len(premaknjeni)} datotek.", "success")
    return redirect(url_for('admin'))

@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/ping")
def ping():
    return "OK iz Flaska!"

def varnostna_kopija_baze():
    danes = datetime.now().strftime('%Y%m%d_%H%M%S')
    shutil.copy('Stare_skripte/VUS.db', f'backup/VUS_backup_{danes}.db')
    print("✅ Varnostna kopija shranjena.")

@app.route('/admin')
@login_required
def admin():
    import os
    print("UPORABLJAM BAZO:", os.path.abspath('VUS.db'))
    try:
        conn = sqlite3.connect('VUS.db')
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM slovar")
        stevilo = cur.fetchone()[0]
        conn.close()
        return render_template('admin.html', stevilo_gesel=stevilo)
    except Exception as e:
        return f"<h1>Napaka v admin: {e}</h1>"


import os
@app.route('/')
@app.route('/home')
@login_required
def home():
    return render_template('home.html')


import re

@app.route('/preveri', methods=['POST'])
def preveri():
    geslo = request.json['geslo']
    iskalno = re.sub(r'[^A-Z0-9]', '', geslo.upper())

    conn = get_db()
    cursor = conn.cursor()
    # Pobereš kandidate, ki se ujemajo po velikih črkah (veliko manj kot cela baza!)
    cursor.execute('''
        SELECT ID, geslo, opis FROM slovar WHERE UPPER(geslo) LIKE ?
    ''', (f"%{geslo.strip().upper()}%",))
    kandidati = cursor.fetchall()

    def norm(s):
        return re.sub(r'[^A-Z0-9]', '', s.upper())

    rezultati = [r for r in kandidati if norm(r['geslo']) == iskalno]
    return jsonify({
        'obstaja': len(rezultati) > 0,
        'gesla': [{'id': r['ID'], 'geslo': r['geslo'], 'opis': r['opis']} for r in rezultati]
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
    return jsonify({"sporocilo": "Geslo uspešno dodano!"})

# UREJANJE GESLA

@app.route('/uredi_geslo', methods=['POST'])
def uredi_geslo():
    data = request.json
    id = data['id']
    opis = data['opis']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE slovar SET OPIS = ? WHERE ID = ?", (opis, id))
    conn.commit()
    return jsonify({'sporocilo': 'Opis uspešno spremenjen'})

@app.route('/brisi_geslo', methods=['POST'])
def brisi_geslo():
    data = request.json
    id = data['id']
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM slovar WHERE ID = ?", (id,))
    conn.commit()
    return jsonify({'sporocilo': 'Geslo izbrisano.'})

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
            SELECT ID, GESLO, OPIS FROM slovar
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

        return jsonify([{
            "id": row["ID"],
            "GESLO": row["GESLO"].strip(),
            "OPIS": row["OPIS"]
        } for row in results])

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
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM slovar")
    st = cur.fetchone()[0]
    conn.close()
    return jsonify({"stevilo_gesel": st})


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

    print(f"✅ KLICANO: prikazi_krizanko za datum: {datum}")

    ime_datoteke = f"{datum}.xml"
    osnovna_pot = os.path.dirname(os.path.abspath(__file__))

    # Najprej poskusi v podmapi (arhiv za mesec)
    mesec = datum[:7]
    pot_arhiv = os.path.join(osnovna_pot, 'static', 'CrosswordCompilerApp', mesec, ime_datoteke)
    pot_glavna = os.path.join(osnovna_pot, 'static', 'CrosswordCompilerApp', ime_datoteke)

    print("📁 Iščem arhivsko datoteko:", pot_arhiv)
    print("📁 Iščem v glavni mapi:", pot_glavna)

    if os.path.exists(pot_arhiv):
        pot_do_datoteke = pot_arhiv
    elif os.path.exists(pot_glavna):
        pot_do_datoteke = pot_glavna
    else:
        return render_template('napaka.html', sporocilo="Križanka za ta datum še ni objavljena.")

    try:
        podatki = pridobi_podatke_iz_xml(pot_do_datoteke)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return render_template('napaka.html', sporocilo=f"Napaka pri branju križanke: {e}")

    return render_template('krizanka.html', podatki=podatki)


@app.route('/krizanka/arhiv')
def arhiv_krizank():
    mapa = os.path.join('static', 'CrosswordCompilerApp')
    vse_mape = [f for f in os.listdir(mapa) if os.path.isdir(os.path.join(mapa, f))]
    meseci = sorted([m for m in vse_mape if len(m) == 7 and m[:4].isdigit() and m[5:7].isdigit()], reverse=True)

    danes = datetime.today().strftime('%Y-%m-%d')
    aktualne = []
    for f in os.listdir(mapa):
        polna_pot = os.path.join(mapa, f)
        if f.endswith('.xml') and os.path.isfile(polna_pot):
            datum = f.replace('.xml', '')
            try:
                datetime.strptime(datum, "%Y-%m-%d")
                if datum < danes:
                    aktualne.append(datum)
            except ValueError:
                pass

    aktualne.sort(reverse=True)

    return render_template(
        'arhiv.html',
        aktualne=aktualne,
        meseci=meseci
    )

@app.route('/krizanka/arhiv/<mesec>')
def arhiv_krizank_mesec(mesec):
    mapa = os.path.join('static', 'CrosswordCompilerApp', mesec)
    datoteke = []
    if os.path.exists(mapa):
        for f in os.listdir(mapa):
            if f.endswith('.xml'):
                datum = f.replace('.xml', '')
                try:
                    datetime.strptime(datum, "%Y-%m-%d")
                    datoteke.append(datum)
                except ValueError:
                    pass
    datoteke.sort(reverse=True)
    return render_template('arhiv_mesec.html', mesec=mesec, datumi=datoteke)




@app.route('/sudoku')
def osnovni_sudoku():
    return redirect(url_for('prikazi_danasnji_sudoku', tezavnost='easy'))

from flask import render_template_string


@app.route('/sudoku/<tezavnost>/<datum>')
def prikazi_sudoku(tezavnost, datum):
    leto_mesec = datum[:7]  # "2025-06"
    ime = f'Sudoku_{tezavnost}_{datum}.html'
    # Najprej preveri v podmapi (arhiv za mesec)
    pot_arhiv = os.path.join('static', f'Sudoku_{tezavnost}', leto_mesec, ime)
    # Če ni tam, preveri še v glavni mapi (za aktualne)
    pot_aktualno = os.path.join('static', f'Sudoku_{tezavnost}', ime)

    if os.path.exists(pot_arhiv):
        pot = pot_arhiv
    elif os.path.exists(pot_aktualno):
        pot = pot_aktualno
    else:
        return render_template('napaka.html', sporocilo="Sudoku za ta datum ali težavnost ni na voljo.")

    with open(pot, encoding="utf-8") as f:
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

    vse_mape = [f for f in os.listdir(mapa_sudoku) if os.path.isdir(os.path.join(mapa_sudoku, f))]
    meseci = sorted([m for m in vse_mape if len(m) == 7 and m[:4].isdigit() and m[5:7].isdigit()], reverse=True)

    aktualni = []
    for f in os.listdir(mapa_sudoku):
        polna_pot = os.path.join(mapa_sudoku, f)
        if f.endswith('.html') and os.path.isfile(polna_pot):
            datum = f.replace(f'Sudoku_{tezavnost}_', '').replace('.html', '')
            try:
                datetime.strptime(datum, "%Y-%m-%d")
                aktualni.append(datum)
            except ValueError:
                pass
    aktualni.sort(reverse=True)

    return render_template(
        'sudoku_arhiv.html',
        tezavnost=tezavnost,
        meseci=meseci,
        aktualni=aktualni
    )


@app.route('/sudoku/arhiv/<tezavnost>/<mesec>')
def arhiv_sudoku_mesec(tezavnost, mesec):
    mapa = os.path.join('static', f'Sudoku_{tezavnost}', mesec)
    datumi = []
    if os.path.exists(mapa):
        for f in os.listdir(mapa):
            if f.endswith('.html'):
                datum = f.replace(f'Sudoku_{tezavnost}_', '').replace('.html', '')
                try:
                    datetime.strptime(datum, "%Y-%m-%d")
                    datumi.append(datum)
                except ValueError:
                    pass
    datumi.sort(reverse=True)
    return render_template('sudoku_arhiv_mesec.html', tezavnost=tezavnost, mesec=mesec, datumi=datumi)




@app.route('/sudoku/arhiv')
def arhiv_sudoku_pregled():
    return render_template('sudoku_arhiv_glavni.html')

from flask import flash, redirect, url_for

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
            mapa = os.path.join("static", f"Sudoku_{tezavnost}")
            odstrani_cc_vrstico_iz_html(mapa)
            flash(f"Sudoku ({tezavnost}) je bil uspešno uvožen in očiščen.", "success")

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


from flask import send_file
import zipfile
import io


@app.route('/prenesi_slike_zip')
def prenesi_slike_zip():
    pot_mape = os.path.join('static', 'Images')
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for koren, _, datoteke in os.walk(pot_mape):
            for ime_datoteke in datoteke:
                polna_pot = os.path.join(koren, ime_datoteke)
                rel_pot = os.path.relpath(polna_pot, pot_mape)
                zipf.write(polna_pot, rel_pot)

    zip_buffer.seek(0)
    return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name='slike_static_Images.zip')

from flask import request, render_template
import os

@app.route('/preveri_sliko', methods=['GET', 'POST'])
def preveri_sliko():
    ime_slike = None
    obstaja = None
    opis = ''
    resitev = ''
    koncnice = ['jpg', 'png', 'webp']
    if request.method == 'POST':
        opis = request.form.get('opis', '')
        resitev = request.form.get('resitev', '')
        osnovno_ime = generiraj_ime_slike(opis, resitev)
        for ext in koncnice:
            pot = os.path.join('static', 'Images', f"{osnovno_ime}.{ext}")
            if os.path.exists(pot):
                ime_slike = f"{osnovno_ime}.{ext}"
                obstaja = True
                break
        if not ime_slike:
            ime_slike = f"{osnovno_ime}.jpg"  # default prikazano ime
            obstaja = False
    return render_template(
        'preveri_sliko.html',
        opis=opis,
        resitev=resitev,
        ime_slike=ime_slike,
        obstaja=obstaja
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')