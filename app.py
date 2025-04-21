from flask import Flask, request, jsonify, render_template, session
from pretvornik import normaliziraj_geslo
import sqlite3

app = Flask(__name__)
app.secret_key = 'tvoja_skrivna_koda'

# Povezava z bazo
def get_db():
    conn = sqlite3.connect('VUS.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/')
def home():
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
def preveri():
    data = request.get_json()
    geslo = data.get('geslo', '').upper().replace(' ', '')

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT GESLO, OPIS FROM slovar WHERE UPPER(REPLACE(GESLO,' ','')) = ?",
        (geslo,)
    )
    rezultati = cur.fetchall()
    conn.close()

    if rezultati:
        gesla = [{"geslo": rez[0], "opis": rez[1]} for rez in rezultati]
        return jsonify({"obstaja": True, "gesla": gesla})
    else:
        return jsonify({"obstaja": False})






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



@app.route('/stevec_gesel', methods=['GET'])
def stevec_gesel():
    conn = get_db()
    cur = conn.cursor()
    steviloGesel = cur.execute("SELECT COUNT(*) FROM slovar").fetchone()[0]
    conn.close()
    return jsonify({"steviloGesel": steviloGesel})


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


@app.route('/admin')
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True, port=10000)

