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


@app.route('/isci_vzorec', methods=['GET', 'POST'])
def isci_po_vzorcu():
    if request.method == 'POST':
        vzorec = request.form.get('vzorec', '').upper()

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT GESLO, OPIS FROM slovar WHERE GESLO LIKE ?", (vzorec,))
        rezultati = cur.fetchall()
        conn.close()

        gesla = [{"geslo": g, "opis": o} for g, o in rezultati]
        session['zadnji_zadetki'] = gesla

        return render_template("isci_vzorec.html", gesla=gesla)

    return render_template("isci_vzorec.html", gesla=[])


@app.route('/asistent_isci', methods=['POST'])
def asistent_isci():
    dodatno = request.json.get('dodatno', '').upper()
    zadetki = session.get('zadnji_zadetki', [])

    filtrirani = [g for g in zadetki if dodatno in g['opis'].upper()]

    return jsonify(filtrirani)


if __name__ == '__main__':
    app.run(debug=True)
