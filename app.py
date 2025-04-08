from flask import Flask, render_template, request, redirect, session, jsonify, g
from flask_cors import CORS  # ✅ omogoči CORS
from pretvornik import normaliziraj_geslo
from flask import flash

import sqlite3
import os
import re
import unicodedata

app = Flask(__name__)
CORS(app)  # ✅ omogoči CORS za celotno aplikacijo



app = Flask(__name__)
app.secret_key = 'Tifumannam1VUS_flask2'
DATABASE = 'VUS.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def normalize(text):
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII').lower()

def extract_ime(opis):
    if '-' in opis:
        kandidat = opis.rsplit('-', 1)[-1].strip()
        ime = re.split(r'\s*\(', kandidat)[0].strip()
        if ime and ime[0].isupper():
            return normalize(ime)
    return 'zzzzzzzz'

@app.route('/')
def index():
    return render_template('index.html')



@app.route("/isci_opis")
def isci_opis():
    return render_template("isci_opis.html")

def odstrani_sumnike(niz):
    zamenjave = {
        'Š': 'S', 'š': 's',
        'Č': 'C', 'č': 'c',
        'Ž': 'Z', 'ž': 'z'
    }
    return ''.join(zamenjave.get(c, c) for c in niz)


@app.route('/isci_po_opisu', methods=['POST'])
def isci_po_opisu():
    surovo = request.form.get('opis', '').strip()
    if not surovo:
        return jsonify({'error': 'Vnesi ključno besedo za iskanje po opisu.'}), 400

    # Če uporabljaš normalizacijo
    from pretvornik import normaliziraj_geslo
    normalizirano = normaliziraj_geslo(surovo).upper()
    besede = normalizirano.split()

    pogoji = []
    params = []

    for beseda in besede:
        if beseda.isdigit():
            # številke iščemo povsod
            pogoji.append("UPPER(OPIS) LIKE ?")
            params.append(f"%{beseda}%")
        else:
            # cele besede – uporabimo presledke levo in desno
            pogoji.append("(' ' || UPPER(OPIS) || ' ') LIKE ?")
            params.append(f"% {beseda} %")

    sql = "SELECT GESLO, OPIS FROM slovar WHERE " + " AND ".join(pogoji)

    conn = get_db()
    cur = conn.cursor()
    cur.execute(sql, params)
    rezultati = cur.fetchall()
    conn.close()

    gesla = [{'geslo': g, 'opis': o} for g, o in rezultati]
    return jsonify(gesla)



@app.route('/isci_vzorec')
def isci_vzorec():
    return render_template("isci_vzorec.html")


@app.route('/isci_po_vzorcu', methods=['POST'])
def isci_po_vzorcu():
    vzorec = request.form['vzorec'].strip()
    vzorec = normaliziraj_geslo(vzorec).replace(" ", "").replace("'", "").replace("’", "").upper()
    dolzina = len(vzorec)

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT GESLO, OPIS FROM slovar WHERE LENGTH(REPLACE(REPLACE(GESLO, ' ', ''), '''', '')) = ? "
        "AND REPLACE(REPLACE(UPPER(GESLO), ' ', ''), '''', '') LIKE ?",
        (dolzina, vzorec)
    )

    rezultati = cur.fetchall()
    conn.close()

    gesla = [{'geslo': g, 'opis': o} for g, o in rezultati]
    return jsonify(gesla)



def sortiraj_gesla(gesla):
    def sortirni_kljuc(vrstica):
        opis = vrstica["OPIS"]
        ...

        # 1. Ali vsebuje vezaj?
        if "-" in opis:
            deli = opis.split("-")
            za_vezajem = deli[1].strip() if len(deli) > 1 else ""

            # 2. Če je prva črka po vezaju velika → uporabi za sortiranje
            if za_vezajem and za_vezajem[0].isupper():
                return (0, za_vezajem.upper())

            # 3. Vezaj obstaja, ampak ni veliko ime
            return (1, opis.upper())

        # 4. Gesla brez vezaja gredo na konec
        return (2, opis.upper())

    return sorted(gesla, key=sortirni_kljuc)

import sqlite3

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        geslo = request.form.get("geslo", "").strip()
        opis = request.form.get("opis", "").strip()

        if geslo and opis:
            # Ločena povezava za dodajanje
            conn_dodaj = sqlite3.connect("VUS.db")
            cur_dodaj = conn_dodaj.cursor()
            cur_dodaj.execute("INSERT INTO slovar (GESLO, OPIS) VALUES (?, ?)", (geslo.upper(), opis))
            conn_dodaj.commit()
            conn_dodaj.close()

    # Druga ločena povezava za branje
    conn_beri = get_db()
    cur = conn_beri.cursor()
    cur.execute("SELECT * FROM slovar")
    gesla = cur.fetchall()
    cur.execute("SELECT COUNT(*) FROM slovar")
    stevilo = cur.fetchone() [0]
    conn_beri.close()
    

    # Sortiranje (če ga uporabljaš)
    gesla = sortiraj_gesla(gesla)

    return render_template("admin.html", gesla=gesla, stevilo=stevilo)


@app.route('/preveri', methods=['POST'])
def preveri():
    podatki = request.get_json()
    geslo = podatki.get('preveri_geslo', '').strip()
    if not geslo:
        return jsonify({"sporocilo": "Vnesi geslo za preverjanje.", "rezultati": []}), 400

    # Uporabi normalizacijo za primerjavo
    normalizirano_geslo = normaliziraj_geslo(geslo).upper()

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT ID, GESLO, OPIS FROM slovar WHERE UPPER(GESLO) = ?", (normalizirano_geslo,))
    rezultat = cur.fetchall()
    conn.close()

    if rezultat:
        gesla = [{"id": r["ID"], "geslo": r["GESLO"], "opis": r["OPIS"]} for r in rezultat]
        return jsonify({
            "sporocilo": f"Število zadetkov: {len(gesla)}",
            "rezultati": gesla
        }), 200
    else:
        return jsonify({
            "sporocilo": "Gesla ni v bazi!",
            "rezultati": []
        }), 200



@app.route('/uredi_geslo', methods=['POST'])
def uredi_geslo():
    id = request.form['id']
    novi_opis = request.form['novi_opis'].strip()

    if id and novi_opis:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("UPDATE slovar SET OPIS = ? WHERE ID = ?", (novi_opis, id))
        conn.commit()
        cur.execute("SELECT * FROM slovar WHERE ID = ?", (id,))
        gesla = cur.fetchall()
        gesla.sort(key=lambda x: extract_ime(x['opis']))
        cur.execute("SELECT COUNT(*) FROM slovar")
        stevilo = cur.fetchone()[0]
        conn.close()

        return render_template("admin.html", gesla=gesla, sporocilo="Opis posodobljen!", rezultat_preverjanja="", stevilo=stevilo)

    return redirect("/admin")

@app.route('/izbrisi_geslo', methods=['POST'])
def izbrisi_geslo():
    id = request.form['id']

    if id:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM slovar WHERE ID = ?", (id,))
        conn.commit()
        conn.close()

    return redirect("/admin")


@app.route('/stevilo_gesel', methods=['GET'])
def stevilo_gesel():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM slovar")
    stevilo = cur.fetchone()[0]
    conn.close()
    return jsonify({"stevilo": stevilo})

@app.route('/zamenjaj_opis', methods=['POST'])
def zamenjaj_opis():
    star = request.form.get('star_izraz', '').strip()
    novi = request.form.get('novi_izraz', '').strip()

    if not star or not novi:
        return redirect('/admin')

    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE slovar SET OPIS = REPLACE(OPIS, ?, ?) WHERE OPIS LIKE ?",
   (star, novi, f"%{star}%"))
    st_sprememb = cur.rowcount
    conn.commit()
    conn.close()

    # 🔙 Posreduj sporočilo naprej (če želiš)
    flash(f"Zamenjanih opisov: {st_sprememb}", "info")

    return redirect('/admin')


@app.route("/prispevaj", methods=["GET", "POST"])
def prispevaj():
    if request.method == "POST":
        uporabnik = request.form.get("uporabnik", "").strip()
        geslo = request.form.get("geslo", "").strip().upper()
        opis = request.form.get("opis", "").strip()

        if geslo and opis:
            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO prispevki (uporabnik, geslo, opis) VALUES (?, ?, ?)",
                (uporabnik, geslo, opis)
            )
            conn.commit()
            conn.close()
            return render_template("prispevaj.html", sporocilo="Hvala za prispevek!")

    return render_template("prispevaj.html")



if __name__ == '__main__':
    port = int(os.environ.get("PORT",1000))
    app.run(host='0.0.0.0', port=port)
