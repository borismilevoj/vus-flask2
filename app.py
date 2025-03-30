# === app.py ===

from flask import Flask, render_template, request, jsonify, session, redirect
import sqlite3
import os
import re
import unicodedata

app = Flask(__name__)
app.secret_key = 'Tifumamnam1VUS_flask2'  # obvezno za delovanje sej

DATABASE = 'VUS.db'

def get_db():
    if not hasattr(session, 'db'):
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        session.db = conn
    return session.db

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        geslo = request.form.get('geslo')
        if geslo == 'novogeslo123':
            session['admin'] = True
            return redirect('/admin')
        else:
            return render_template('login.html', napaka="Napačno geslo!")
    return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('admin'):
        return redirect('/login')

    def normalize(text):
        return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')

    def extract_ime(opis):
        if '-' in opis:
            kandidat = opis.rsplit('-', 1)[-1].strip()
            ime = re.split(r'\s*\(', kandidat)[0].strip()
            if ime and ime[0].isupper():
                return normalize(ime)
        return 'zzz'

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
            gesla.sort(key=lambda x: extract_ime(x['opis']))
            cur.execute("SELECT COUNT(*) FROM slovar")
            stevilo = cur.fetchone()[0]

            return render_template("admin.html",
                                   gesla=gesla,
                                   sporocilo="Geslo uspešno dodano!",
                                   rezultat_preverjanja=rezultat_preverjanja,
                                   stevilo=stevilo)

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM slovar")
    stevilo = cur.fetchone()[0]

    return render_template("admin.html",
                           gesla=[],
                           sporocilo="",
                           rezultat_preverjanja="",
                           stevilo=stevilo)


# === login.html ===
# (v templates/login.html)
# Primerna preprosta stran:

# <form method="post">
#     <input type="password" name="geslo" placeholder="Vnesi geslo">
#     <button type="submit">Prijava</button>
#     {% if napaka %}<p style="color:red">{{ napaka }}</p>{% endif %}
# </form>

if __name__ == '__main__':
    app.run(debug=True, port=10000)
