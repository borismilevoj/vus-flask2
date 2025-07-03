# arhiviranje_util.py

import os
import shutil
from datetime import datetime

POT = os.path.join("static", "CrosswordCompilerApp")

TEZAVNOSTI = ["very_easy", "easy", "medium", "hard"]
SUDOKU_POT = os.path.join("static")

def premakni_krizanke_v_mesece(mesec=None):
    if mesec is None:
        danes = datetime.today()
        mesec_map = danes.strftime("%Y-%m")
    else:
        mesec_map = mesec
    arhivna_mapa = os.path.join(POT, mesec_map)
    if not os.path.exists(arhivna_mapa):
        os.makedirs(arhivna_mapa)
    premaknjeni = []
    for ime in os.listdir(POT):
        if ime.endswith(".xml") or ime.endswith(".js"):
            if ime.startswith(mesec_map):
                polna_pot = os.path.join(POT, ime)
                nova_pot = os.path.join(arhivna_mapa, ime)
                shutil.move(polna_pot, nova_pot)
                premaknjeni.append(ime)
    return premaknjeni

def premakni_sudoku_v_mesece(mesec=None):
    if mesec is None:
        danes = datetime.today()
        mesec_map = danes.strftime("%Y-%m")
    else:
        mesec_map = mesec
    premaknjeni = []
    for tezavnost in TEZAVNOSTI:
        mapa = os.path.join(SUDOKU_POT, f"Sudoku_{tezavnost}")
        arhiv = os.path.join(mapa, mesec_map)
        if not os.path.exists(arhiv):
            os.makedirs(arhiv)
        for ime in os.listdir(mapa):
            if ime.endswith(".js") and ime.startswith(mesec_map):
                polna_pot = os.path.join(mapa, ime)
                nova_pot = os.path.join(arhiv, ime)
                shutil.move(polna_pot, nova_pot)
                premaknjeni.append(os.path.join(f"Sudoku_{tezavnost}", ime))
    return premaknjeni

def arhiviraj_danes():
    return premakni_krizanke_v_mesece() + premakni_sudoku_v_mesece()
