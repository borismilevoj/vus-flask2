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
    podatki = request.json
    geslo = podatki.get('geslo')

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT ID, GESLO, OPIS FROM slovar WHERE GESLO LIKE ?", (geslo,))
    rezultati = cur.fetchall()
    conn.close()

    if rezultati:
        return jsonify({
            "sporocilo": "Geslo že obstaja!",
            "rezultati": [{"id": r["ID"], "geslo": r["GESLO"], "opis": r["OPIS"]} for r in rezultati]
        }), 200
    else:
        return jsonify({"sporocilo": "Gesla ni v bazi!", "rezultati": []}), 200





@app.route('/dodaj_geslo', methods=['POST'])
def dodaj_geslo():
    podatki = request.json
    geslo = podatki.get('geslo')
    opis = podatki.get('opis')

    if not geslo or not opis:
        return jsonify({"sporocilo": "Geslo in opis sta obvezna!"}), 400

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO slovar (GESLO, OPIS, NORMALIZIRAN_OPIS) VALUES (?, ?, ?)",
        (geslo, opis, normaliziraj_geslo(opis))
    )
    conn.commit()
    steviloGesel = cur.execute("SELECT COUNT(*) FROM slovar").fetchone()[0]
    conn.close()

    return jsonify({"sporocilo": f"Geslo '{geslo}' dodano!", "steviloGesel": steviloGesel})



@app.route('/uredi_geslo/<int:id>', methods=['POST'])
def uredi_geslo(id):
    nov_opis = request.json.get('opis')
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE slovar SET OPIS = ?, NORMALIZIRAN_OPIS = ? WHERE ID = ?",
                (nov_opis, normaliziraj_geslo(nov_opis), id))
    conn.commit()
    conn.close()
    return jsonify({"sporocilo": "Geslo je uspešno posodobljeno."})


@app.route('/brisi_geslo/<int:id>', methods=['DELETE'])
def brisi_geslo(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM slovar WHERE ID = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"sporocilo": "Geslo uspešno izbrisano!"})





@app.route('/stevec_gesel', methods=['GET'])
def stevec_gesel():
    conn = get_db()
    cur = conn.cursor()
    steviloGesel = cur.execute("SELECT COUNT(*) FROM slovar").fetchone()[0]
    conn.close()
    return jsonify({"steviloGesel": steviloGesel})


# Primer postavitve v app.py (kamorkoli pred if __name__ == '__main__'):

@app.route('/admin')
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True, port=10000)

