from flask import (
    Flask, jsonify, session, redirect, url_for, request, render_template,
    flash, send_from_directory, render_template_string, send_file
)
from functools import wraps
import sqlite3
import os
import glob
import unicodedata
import re
import shutil
import zipfile
import io
from datetime import datetime

from krizanka import pridobi_podatke_iz_xml
from Stare_skripte.uvoz_datotek import premakni_krizanke, premakni_sudoku
from arhiviranje_util import arhiviraj_danes

# ==== Inicializacija ==========================================================
app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = "Tifumannam1_vus-flask2.onrender.com"
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['PROPAGATE_EXCEPTIONS'] = True

# Varneje poskrbi za uploads: če obstaja datoteka z istim imenom, jo odstrani, nato ustvari mapo
if not os.path.isdir(app.config['UPLOAD_FOLDER']):
    if os.path.exists(app.config['UPLOAD_FOLDER']):  # obstaja kot datoteka
        os.remove(app.config['UPLOAD_FOLDER'])
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

GESLO = "Tifumannam1_vus-flask2.onrender.com"

# ==== Pomožne funkcije ========================================================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'prijavljen' not in session:
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function

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

def get_db():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "VUS.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# --- sortiranje po imenu (osebe najprej) ---
def normalize_ascii(text: str) -> str:
    if not text:
        return ""
    s = unicodedata.normalize('NFD', text)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return ' '.join(s.lower().split())

def ime_za_sort(opis: str) -> str:
    if not opis or ' - ' not in opis:
        return ""
    blok = opis.split(' - ', 1)[1].strip()
    if '(' in blok:
        blok = blok.split('(', 1)[0].strip()
    if ',' in blok:
        blok = blok.split(',', 1)[1].strip()
    ime = blok.split()[0] if blok else ""
    return normalize_ascii(ime)

def sort_key_opis(opis: str):
    je_oseba = 0 if ' - ' in (opis or '') else 1
    return (je_oseba, ime_za_sort(opis), normalize_ascii(opis))

# --- indeks za hitro /preveri (brez before_first_request v Flask 3.1) ---
def ensure_indexes():
    conn = get_db()
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_slovar_norm_expr
        ON slovar(replace(replace(replace(upper(GESLO),' ',''),'-',''),'_',''));
    """)
    conn.close()

with app.app_context():
    ensure_indexes()

# ==== Diagnostika / Health ====================================================

@app.route("/ping")
def ping():
    return "OK iz Flaska!"

@app.route("/health", methods=["GET", "HEAD"])
def health():
    return "ok", 200

@app.route("/_routes")
def show_routes():
    lines = []
    for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.rule):
        lines.append(f"{sorted(rule.methods)} {rule.rule}  ->  endpoint='{rule.endpoint}'")
    return "<pre>" + "\n".join(lines) + "</pre>"

@app.route("/test")
def test():
    return render_template("test.html")

# ==== Avtentikacija ===========================================================

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

# ==== Domača stran (root + /home) =============================================

@app.route('/')
@app.route('/home')
def home():
    obvestilo = ""
    try:
        with open('obvestilo.txt', encoding="utf-8") as f:
            obvestilo = f.read().strip()
    except FileNotFoundError:
        pass
    return render_template('home.html', obvestilo=obvestilo)

# ==== 404 handler =============================================================

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for("home"))

# ==== Admin ===================================================================

@app.route('/admin')
@login_required
def admin():
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

@app.route('/admin/arhiviraj', methods=['POST'])
@login_required
def sprozi_arhiviranje():
    premaknjeni = arhiviraj_danes()
    flash(f"Premaknjenih {len(premaknjeni)} datotek.", "success")
    return redirect(url_for('admin'))

# ==== API-ji / CRUD ===========================================================

@app.route('/preveri', methods=['POST'])
def preveri():
    payload = request.get_json(silent=True) or {}
    if not payload and request.form:
        payload = request.form

    geslo = (payload.get('geslo') or '').strip()
    if not geslo:
        return jsonify({'obstaja': False, 'gesla': []})

    # normalizacija IDENTIČNA kot v indeksu/poizvedbi
    iskalno = geslo.upper().replace(' ', '').replace('-', '').replace('_', '')

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT ID AS id, GESLO AS geslo, OPIS AS opis
        FROM slovar
        WHERE replace(replace(replace(upper(GESLO),' ',''),'-',''),'_','') = ?
    """, (iskalno,))
    rezultati = cur.fetchall()
    conn.close()

    # sortiranje: osebe najprej, po imenu; ostalo po opisu
    rezultati = sorted(rezultati, key=lambda r: sort_key_opis(r['opis']))

    return jsonify({
        'obstaja': len(rezultati) > 0,
        'gesla': [{'id': r['id'], 'geslo': r['geslo'], 'opis': r['opis']} for r in rezultati]
    })

@app.route('/dodaj_geslo', methods=['POST'])
def dodaj_geslo():
    data = request.json or {}
    geslo = (data.get('geslo') or '').strip()
    opis = (data.get('opis') or '').strip()

    if not geslo or not opis:
        return jsonify({"napaka": "Manjka geslo ali opis."}), 400

    conn = get_db()
    cur = conn.cursor()

    # deduplikacija po normaliziranem OPIS-u (brez šumnikov/case)
    opis_norm = normalize_ascii(opis)
    cur.execute("SELECT ID, OPIS FROM slovar WHERE UPPER(GESLO) = UPPER(?)", (geslo,))
    obstojece = cur.fetchall()
    for r in obstojece:
        if normalize_ascii(r['OPIS']) == opis_norm:
            conn.close()
            return jsonify({"sporocilo": "Ta zapis že obstaja – nič dodano."}), 200

    cur.execute("INSERT INTO slovar (GESLO, OPIS) VALUES (?, ?)", (geslo, opis))
    conn.commit()
    conn.close()
    return jsonify({"sporocilo": "Geslo uspešno dodano!"})

@app.route('/uredi_geslo', methods=['POST'])
def uredi_geslo():
    data = request.json or {}
    id = data.get('id')
    opis = (data.get('opis') or '').strip()
    if not id:
        return jsonify({'napaka': 'Manjka ID.'}), 400
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE slovar SET OPIS = ? WHERE ID = ?", (opis, id))
    conn.commit()
    return jsonify({'sporocilo': 'Opis uspešno spremenjen'})

@app.route('/brisi_geslo', methods=['POST'])
def brisi_geslo():
    data = request.json or {}
    id = data.get('id')
    if not id:
        return jsonify({'napaka': 'Manjka ID.'}), 400
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM slovar WHERE ID = ?", (id,))
    conn.commit()
    return jsonify({'sporocilo': 'Geslo izbrisano.'})

# ==== Iskanje =================================================================

@app.route('/test_iscenje')
def test_iscenje():
    return render_template('isci_vzorec_test.html')

@app.route('/isci_vzorec', methods=['GET', 'POST'])
def isci_vzorec():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify([])

        data = request.get_json(silent=True) or {}
        vzorec = (data.get('vzorec') or '').upper().replace(' ', '')
        dodatno = data.get('dodatno', '')

        # 💡 robustno: dolžino vzamemo iz payload-a, sicer iz spinnerja/rezervnih ključev, sicer iz len(vzorec)
        try:
            dolzina_vzorca = int(data.get('dolzina') or data.get('stevilo') or 0)
        except Exception:
            dolzina_vzorca = 0
        if dolzina_vzorca <= 0:
            dolzina_vzorca = len(vzorec)  # fallback

        # Če vzorec nima vseh pozicij, ga DOPOLNI z '_' do izbrane dolžine
        if len(vzorec) < dolzina_vzorca:
            vzorec = vzorec + '_' * (dolzina_vzorca - len(vzorec))
        elif len(vzorec) > dolzina_vzorca:
            vzorec = vzorec[:dolzina_vzorca]

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
                query += (
                    f" AND SUBSTR("
                    f"REPLACE(REPLACE(REPLACE(GESLO, ' ', ''), '-', ''), '_', ''), {i + 1}, 1"
                    f") = ?"
                )
                params.append(crka)

        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()

        # (ostanek tvojega konca: sortiranje + jsonify) ostane enak

        # 3) SORTIRAJ: osebe najprej, znotraj po imenu
        results = sorted(results, key=lambda row: sort_key_opis(row["OPIS"]))

        # 4) vrni tudi 'ime' + izklopi cache
        payload = [
            {
                "id": row["ID"],
                "GESLO": row["GESLO"].strip(),
                "OPIS": row["OPIS"],
                "ime": ime_za_sort(row["OPIS"])
            }
            for row in results
        ]
        resp = jsonify(payload)
        resp.headers['Cache-Control'] = 'no-store'
        return resp

    # GET: vrni stran
    return render_template('isci_vzorec.html')

@app.route('/isci_opis', methods=['GET', 'POST'])
def isci_opis():
    if request.method == 'POST':
        podatki = request.get_json() or {}
        opis = podatki.get('opis', '')

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT GESLO, OPIS FROM slovar WHERE OPIS LIKE ? LIMIT 100", (f"%{opis}%",))
        rezultat = cursor.fetchall()
        conn.close()

        # opcijsko: sortiraj osebe najprej po imenu
        rezultat = sorted(rezultat, key=lambda r: sort_key_opis(r['OPIS']))

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

# ==== Križanka =================================================================

@app.route('/krizanka/static/<path:filename>')
def krizanka_static_file(filename):
    pot = os.path.join('static', 'Krizanke', 'CrosswordCompilerApp')
    return send_from_directory(pot, filename)

@app.route('/krizanka', defaults={'datum': None})
@app.route('/krizanka/<datum>')
def prikazi_krizanko(datum):
    if datum is None:
        datum = datetime.today().strftime('%Y-%m-%d')

    ime_datoteke = f"{datum}.xml"
    osnovna_pot = os.path.dirname(os.path.abspath(__file__))
    mesec = datum[:7]
    pot_arhiv = os.path.join(osnovna_pot, 'static', 'CrosswordCompilerApp', mesec, ime_datoteke)
    pot_glavna = os.path.join(osnovna_pot, 'static', 'CrosswordCompilerApp', ime_datoteke)

    if os.path.exists(pot_arhiv):
        pot_do_datoteke = pot_arhiv
    elif os.path.exists(pot_glavna):
        pot_do_datoteke = pot_glavna
    else:
        return render_template('napaka.html', sporocilo="Križanka za ta datum še ni objavljena.")

    try:
        podatki = pridobi_podatke_iz_xml(pot_do_datoteke)
    except Exception as e:
        import traceback; traceback.print_exc()
        return render_template('napaka.html', sporocilo=f"Napaka pri branju križanke: {e}")

    # >>> pomembno: posreduj datum v template
    return render_template('krizanka.html', podatki=podatki, datum=datum)


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
    return render_template('arhiv.html', aktualne=aktualne, meseci=meseci)

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

# ==== Sudoku ==================================================================

@app.route('/sudoku')
def osnovni_sudoku():
    return redirect(url_for('prikazi_danasnji_sudoku', tezavnost='easy'))
@app.route('/sudoku/<tezavnost>/<datum>')
def prikazi_sudoku(tezavnost, datum):
    leto_mesec = datum[:7]  # "YYYY-MM"
    ime = f"Sudoku_{tezavnost}_{datum}.html"

    pot_arhiv = os.path.join('static', f"Sudoku_{tezavnost}", leto_mesec, ime)
    pot_aktualno = os.path.join('static', f"Sudoku_{tezavnost}", ime)

    if os.path.exists(pot_arhiv):
        rel_pot = f"Sudoku_{tezavnost}/{leto_mesec}/{ime}"
    elif os.path.exists(pot_aktualno):
        rel_pot = f"Sudoku_{tezavnost}/{ime}"
    else:
        return render_template('napaka.html', sporocilo="Sudoku za ta datum ali težavnost ni na voljo.")

    sudoku_url = url_for('static', filename=rel_pot)
    return render_template('sudoku_embed.html', sudoku_url=sudoku_url, tezavnost=tezavnost, datum=datum)


@app.route('/sudoku/<tezavnost>')
def prikazi_danasnji_sudoku(tezavnost):
    danes = datetime.today().strftime('%Y-%m-%d')
    return redirect(url_for('prikazi_sudoku', tezavnost=tezavnost, datum=danes))

@app.route('/sudoku/meni')
def sudoku_meni():
    return render_template('sudoku_meni.html')

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

    return render_template('sudoku_arhiv.html', tezavnost=tezavnost, meseci=meseci, aktualni=aktualni)

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

# ==== Uvoz / utility ==========================================================

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
    data = request.json or {}
    original = (data.get('original') or '').strip()
    zamenjava = (data.get('zamenjava') or '').strip()

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM slovar WHERE OPIS LIKE ?", (f"%{original}%",))
    stevilo_zadetkov = cur.fetchone()[0]

    if stevilo_zadetkov > 0:
        cur.execute(
            "UPDATE slovar SET OPIS = REPLACE(OPIS, ?, ?) WHERE OPIS LIKE ?",
            (original, zamenjava, f"%{original}%")
        )
        conn.commit()

    conn.close()
    return jsonify({"spremembe": stevilo_zadetkov})

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
    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name='slike_static_Images.zip'
    )

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
    return render_template('preveri_sliko.html', opis=opis, resitev=resitev, ime_slike=ime_slike, obstaja=obstaja)

# ==== Main ====================================================================

if __name__ == "__main__":
    app.run(debug=True)
