
from flask import Flask, render_template, request, jsonify, g, session, redirect
import sqlite3
import os
import re
import unicodedata

app = Flask(__name__)
app.secret_key = 'Tifumannam1VUS_flask2'
DATABASE = 'VUS.db'

 # ========== POVEZAVA Z BAZO ====================

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

# =================================================

@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def normalize(text):
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII').lower()

# ================ SORTIRANJE ===========================

def extract_ime(opis):
    if '-' in opis:
        kandidat = opis.rsplit('-', 1)[-1].strip()
        ime = re.split(r'\s*\(', kandidat)[0].strip()
        if ime and ime[0].isupper():
            return normalize(ime)
    return 'zzz'

# ===================== LOGIN ===========================

@app.route('/login', methods=['GET', 'POST'])
def login():
    napaka = ""
    if request.method == 'POST':
        password = request.form['geslo']
        if password == 'admin123':
            session['admin'] = True
            return redirect('/admin')
        else:
            napaka = "Napačno geslo."
    return render_template("login.html", napaka=napaka)

# ========================= ADMIN ===========================


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('admin'):
        return redirect('/login')

    def normalize(text):
        return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII').lower()

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

            # ⬇️ Vstavi geslo v bazo
            cur.execute("INSERT INTO slovar (GESLO, OPIS) VALUES (?, ?)", (geslo.upper(), opis))
            conn.commit()

            # ⬇️ Pridobi vnešeno geslo
            cur.execute("SELECT * FROM slovar WHERE UPPER(GESLO) = ?", (geslo.upper(),))
            gesla = cur.fetchall()

            # ⬇️ Sortiranje po imenu za zadnjim vezajem
            gesla.sort(key=lambda x: extract_ime(x['opis']))

            # ⬇️ Števec
            cur.execute("SELECT COUNT(*) FROM slovar")
            stevilo = cur.fetchone()[0]

            conn.close()

            return render_template("admin.html",
                                   gesla=gesla,
                                   sporocilo="Geslo uspešno dodano!",
                                   rezultat_preverjanja="",
                                   stevilo=stevilo)

    # GET zahteva – ob ponastavitvi ali prvem zagonu
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM slovar")
    stevilo = cur.fetchone()[0]
    conn.close()

    return render_template("admin.html",
                           gesla=[],
                           sporocilo="",
                           rezultat_preverjanja="",
                           stevilo=stevilo)

# ===================== PREVERI =================================

@app.route('/preveri', methods=['POST'])
def preveri():
    rezultat = ""
    geslo = request.form['preveri_geslo'].strip()

    if geslo:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM slovar WHERE UPPER(GESLO) = UPPER(?)", (geslo,))
        obstaja = cur.fetchone()[0]
        if obstaja:
            rezultat = f"Geslo '{geslo}' že obstaja v bazi."
        else:
            rezultat = f"Geslo '{geslo}' še ne obstaja."
        cur.execute("SELECT * FROM slovar WHERE UPPER(GESLO) = UPPER(?)", (geslo,))
        gesla = cur.fetchall()
        cur.execute("SELECT COUNT(*) FROM slovar")
        stevilo = cur.fetchone()[0]
        return render_template("admin.html", gesla=gesla, sporocilo="", rezultat_preverjanja=rezultat, stevilo=stevilo)

    cur = get_db().cursor()
    cur.execute("SELECT COUNT(*) FROM slovar")
    stevilo = cur.fetchone()[0]
    return render_template("admin.html", gesla=[], sporocilo="", rezultat_preverjanja=rezultat, stevilo=stevilo)

# ==============IZBRIŠI GESLO  =======================


@app.route('/izbrisi_geslo', methods=['POST'])
def izbrisi_geslo():
    if not session.get('admin'):
        return redirect('/login')

    geslo_id = request.form['id']
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM slovar WHERE ID = ?", (geslo_id,))
    conn.commit()

    # Pridobi ponovno podatke za prikaz
    cur.execute("SELECT * FROM slovar WHERE ID = ?", (geslo_id,))
    gesla = cur.fetchall()
    cur.execute("SELECT COUNT(*) FROM slovar")
    stevilo = cur.fetchone()[0]

    return render_template("admin.html",
                           gesla=gesla,
                           sporocilo="Geslo uspešno izbrisano.",
                           rezultat_preverjanja="",
                           stevilo=stevilo)


# =============== LOGOUT ==============================


@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/login')

# =================IŠČI PO VZORCU =========================

@app.route('/isci_po_vzorcu', methods=['POST'])
def isci_po_vzorcu():
    vzorec = request.form['vzorec'].strip().upper()
    dolzina = int(request.form['dolzina'])

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT GESLO, OPIS FROM slovar WHERE LENGTH(GESLO) = ? AND GESLO LIKE ?", (dolzina, vzorec))
    rezultati = cur.fetchall()
    conn.close()

    gesla = [{'geslo': g, 'opis': o} for g, o in rezultati]
    return jsonify(gesla)

# ===================IŠČI PO OPISU ==============?=========

@app.route('/isci_po_opisu', methods=['POST'])
def isci_po_opisu():
    izraz = request.form['iskalni_izraz'].strip().lower()

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT GESLO, OPIS FROM slovar WHERE lower(OPIS) LIKE ?", ('%' + izraz + '%',))
    rezultati = cur.fetchall()
    conn.close()

    gesla = [{'geslo': g, 'opis': o} for g, o in rezultati]
    return jsonify(gesla)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
