from flask import Flask, request, jsonify, render_template, session
from pretvornik import normaliziraj_geslo
import sqlite3
from krizanka import pridobi_podatke_iz_xml
from datetime import datetime
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.secret_key = 'tvoja_skrivna_koda'

# Funkcija, ki preveri dovoljene končnice slik
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Povezava z bazo
def get_db():
    conn = sqlite3.connect('VUS.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/krizanka')
def prikazi_krizanko():
    podatki = pridobi_podatke_iz_xml('1.xml')
    # print("Preverjanje podatkov pred pošiljanjem v predlogo:", podatki)
    return render_template('krizanka.html', podatki=podatki)

@app.route('/preveri_crko', methods=['POST'])
def preveri_crko():
    data = request.json
    x = data['x']
    y = data['y']
    crka = data['crka'].upper()

    podatki = pridobi_podatke_iz_xml('1.xml')

    for geslo in podatki['gesla_opisi']:
        gx, gy, smer, dolzina = geslo['x'], geslo['y'], geslo['smer'], geslo['dolzina']

        if smer == 'across' and y == gy and gx <= x < gx + dolzina:
            index = x - gx
            pravilna_crka = geslo['solution'][index].upper()
            return jsonify({'pravilno': crka == pravilna_crka})

        if smer == 'down' and x == gx and gy <= y < gy + dolzina:
            index = y - gy
            pravilna_crka = geslo['solution'][index].upper()
            return jsonify({'pravilno': crka == pravilna_crka})

    return jsonify({'pravilno': False})


# tu naprej so še ostale tvoje route...



@app.route('/')
def home():
    import os
    pot = os.path.abspath("templates/home.html")
    print("Trenutna pot do home.html:", pot)

    with open(pot, "r", encoding="utf-8") as f:
        vsebina = f.read()
        print("Vsebina home.html:\n", vsebina[:500])  # prvih 500 znakov

    return render_template('home.html')


@app.route('/prispevaj')
def prispevaj_geslo():
    return render_template('prispevaj.html')


@app.route('/isci_vzorec', methods=['GET', 'POST'])
def isci_vzorec():
    gesla = []
    vzorec = ''
    dodatno = ''

    if request.method == 'POST':
        podatki = request.json
        vzorec = podatki.get('vzorec', '').upper()
        dodatno = podatki.get('dodatno', '').upper()

        dolzina = len(vzorec)

        sql_vzorec = vzorec.replace('_', '%')
        sql = """
            SELECT GESLO, OPIS 
            FROM slovar 
            WHERE LENGTH(REPLACE(GESLO,' ','')) = ?
            AND REPLACE(REPLACE(GESLO,' ',''), '-', '') LIKE ?
        """

        params = [dolzina, sql_vzorec]

        if dodatno:
            sql += " AND UPPER(OPIS) LIKE ?"
            params.append(f"%{dodatno}%")

        conn = get_db()
        cur = conn.cursor()
        cur.execute(sql, params)
        rezultati = cur.fetchall()
        conn.close()

        gesla = [{'GESLO': r['GESLO'], 'OPIS': r['OPIS']} for r in rezultati]

        return jsonify(gesla)

    return render_template("isci_vzorec.html")




@app.route('/isci_opis', methods=['GET', 'POST'])
def isci_po_opisu():
    if request.method == 'POST':
        opis = request.form.get('opis', '').strip()
        if not opis:
            return jsonify({'error': "Vnesi opis za iskanje."}), 400

        normaliziran_opis = normaliziraj_geslo(opis).upper()
        besede = normaliziran_opis.split()

        pogoji = []
        params = []

        for beseda in besede:
            pogoji.append("UPPER(NORMALIZIRAN_OPIS) LIKE ?")
            params.append(f"%{beseda}%")

        sql = "SELECT GESLO, OPIS FROM slovar WHERE " + " AND ".join(pogoji)

        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute(sql, params)
            rezultati = cur.fetchall()
            gesla = [{"geslo": geslo, "opis": opis} for geslo, opis in rezultati]
            return jsonify(gesla)
        except Exception as e:
            print("Napaka pri izvajanju SQL:", e)
            return jsonify({'error': str(e)}), 500
        finally:
            conn.close()

    return render_template("isci_opis.html")



@app.route('/preveri', methods=['POST'])
@app.route('/preveri', methods=['GET', 'POST'])
def preveri():
    geslo = opis = ime_slike = None
    if request.method == 'POST':
        geslo = request.form['geslo_za_preverjanje']
        slika = request.files.get('slika_za_preverjanje')

        ime_slike = None
        if slika and allowed_file(slika.filename):
            ime_slike = secure_filename(slika.filename)
            slika.save(os.path.join(app.config['UPLOAD_FOLDER'], ime_slike))

        # shrani sliko ali preveri geslo
        conn = sqlite3.connect('VUS.db')
        c = conn.cursor()
        c.execute("SELECT * FROM slovar WHERE GESLO = ?", (geslo,))
        rezultat = c.fetchone()

        if rezultat:
            opis = rezultat[1]  # ali ustrezen indeks za opis
            # po potrebi shrani sliko obstoječemu geslu
            if ime_slike:
                c.execute("UPDATE slovar SET SLIKA = ? WHERE GESLO = ?", (ime_slike, geslo))
                conn.commit()

        conn.close()

    return render_template('preveri.html', geslo=geslo, opis=opis, slika=ime_slike)




@app.route('/dodaj_geslo', methods=['POST'])
def dodaj_geslo():
    data = request.get_json()
    geslo = data['geslo']
    opis = data['opis']

    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO slovar (GESLO, OPIS) VALUES (?, ?)", (geslo, opis))
        conn.commit()
        conn.close()

        return jsonify({"status": "uspesno", "sporocilo": "Geslo uspešno dodano!"})

    except sqlite3.IntegrityError:
        return jsonify({"status": "napaka", "sporocilo": "Geslo že obstaja v bazi."})

    except Exception as e:
        print(e)  # če je napaka, izpiši za lažje reševanje težav
        return jsonify({"status": "napaka", "sporocilo": "Prišlo je do napake."})





@app.route('/uredi_geslo', methods=['POST'])
def uredi_geslo():
    data = request.get_json()
    geslo = data['geslo']
    novi_opis = data['opis']

    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("UPDATE slovar SET OPIS=? WHERE GESLO=?", (novi_opis, geslo))
        conn.commit()
        conn.close()

        return jsonify({"status": "uspesno", "sporocilo": "Geslo uspešno urejeno!"})
    except Exception as e:
        print(e)
        return jsonify({"status": "napaka", "sporocilo": "Prišlo je do napake pri urejanju."})


@app.route('/brisi_geslo', methods=['POST'])
def brisi_geslo():
    data = request.get_json()
    geslo = data['geslo']
    opis = data['opis']

    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM slovar WHERE GESLO=? AND OPIS=?", (geslo, opis))
        conn.commit()
        conn.close()

        return jsonify({"status": "uspesno", "sporocilo": "Geslo uspešno izbrisano!"})
    except Exception as e:
        print(e)
        return jsonify({"status": "napaka", "sporocilo": "Napaka pri brisanju."})

@app.route('/zamenjaj_geslo', methods=['POST'])
def zamenjaj_geslo():
    data = request.get_json()
    original = data.get('original', '').strip()
    zamenjava = data.get('zamenjava', '').strip()

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE slovar
        SET GESLO = REPLACE(GESLO, ?, ?)
        WHERE GESLO LIKE ?
    """, (original, zamenjava, f"%{original}%"))
    conn.commit()
    spremembe = cur.rowcount
    conn.close()

    return jsonify({"spremembe": spremembe})




@app.route('/stevec_gesel', methods=['GET'])
def stevec_gesel():
    conn = get_db()
    cur = conn.cursor()
    steviloGesel = cur.execute("SELECT COUNT(*) FROM slovar").fetchone()[0]
    conn.close()
    return jsonify({"steviloGesel": steviloGesel})

@app.route('/pretvori_crke', methods=['POST'])
def pretvori_crke():
    try:
        conn = get_db()
        cur = conn.cursor()

        cur.execute("SELECT GESLO, OPIS FROM slovar")
        gesla = cur.fetchall()

        spremembe = 0

        for geslo, opis in gesla:
            nov_opis = opis.swapcase()
            if nov_opis != opis:
                cur.execute("UPDATE slovar SET OPIS=? WHERE GESLO=? AND OPIS=?", (nov_opis, geslo, opis))
                spremembe += 1

        conn.commit()
        conn.close()

        return jsonify({"sporocilo": f"Uspešno pretvorjenih opisov: {spremembe}"})

    except Exception as e:
        print("NAPAKA:", e)  # Dodaj to vrstico
        return jsonify({"sporocilo": f"Napaka pri pretvorbi črk: {str(e)}"})


# Primer postavitve v app.py (kamorkoli pred if __name__ == '__main__'):

@app.route('/zamenjaj', methods=['POST'])
def zamenjaj():
    data = request.get_json()
    original = data.get('original', '')
    zamenjava = data.get('zamenjava', '')

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE slovar
        SET OPIS = REPLACE(OPIS, ?, ?)
        WHERE OPIS LIKE ?
    """, (original, zamenjava, f"%{original}%"))
    conn.commit()
    spremembe = cur.rowcount
    conn.close()

    return jsonify({"spremembe": spremembe})


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
        tezavnost_datoteka = tezavnosti[izbrana_tezavnost]

    return render_template('sudoku.html',
                           tezavnosti=tezavnosti,
                           izbrana_tezavnost=izbrana_tezavnost,
                           tezavnost_datoteka=tezavnost_datoteka)



# Stran za posamezno težavnost Sudoku
@app.route('/sudoku/<stopnja>')
def sudoku_tezavnost(stopnja):
    dovoljene_tezavnosti = ['lažja', 'srednja', 'težka', 'najtežja']
    if stopnja not in dovoljene_tezavnosti:
        return "Neveljavna težavnost.", 404

    # ime datoteke HTML naj bo recimo sudoku_lazja.html, sudoku_srednja.html itd.
    ime_datoteke = f'sudoku_{stopnja}.html'
    return render_template(ime_datoteke, stopnja=stopnja)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        geslo = request.form['geslo']
        opis = request.form['opis']
        slika = request.files['slika']

        ime_slike = None
        if slika and allowed_file(slika.filename):
            ime_slike = secure_filename(slika.filename)
            slika.save(os.path.join(app.config['UPLOAD_FOLDER'], ime_slike))

        conn = sqlite3.connect('VUS.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO slovar (GESLO, OPIS, SLIKA) VALUES (?, ?, ?)", (geslo, opis, ime_slike))
        conn.commit()
        conn.close()

    conn = sqlite3.connect('VUS.db')
    cur = conn.cursor()
    cur.execute("SELECT rowid, GESLO, OPIS, SLIKA FROM slovar ORDER BY rowid DESC")
    gesla = cur.fetchall()
    conn.close()

    return render_template('admin.html', gesla=gesla)


if __name__ == '__main__':
    app.run(debug=True, port=10000)
