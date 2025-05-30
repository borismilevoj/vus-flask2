import os
from datetime import datetime
import shutil


def arhiviraj_danes():
    danes = datetime.now().strftime("%Y-%m-%d")
    mesecna_mapa = datetime.now().strftime("%Y-%m")

    mape = {
        "static/Krizanke/CrosswordCompilerApp": f"static/Arhiv/Krizanke/{mesecna_mapa}",
        "static/Sudoku_very_easy": f"static/Arhiv/Sudoku_very_easy/{mesecna_mapa}",
        "static/Sudoku_easy": f"static/Arhiv/Sudoku_easy/{mesecna_mapa}",
        "static/Sudoku_medium": f"static/Arhiv/Sudoku_medium/{mesecna_mapa}",
        "static/Sudoku_hard": f"static/Arhiv/Sudoku_hard/{mesecna_mapa}",
    }

    premaknjeni = []

    for izvorna, ciljna in mape.items():
        os.makedirs(ciljna, exist_ok=True)
        for ime in os.listdir(izvorna):
            if ime.startswith(danes):
                pot_izvor = os.path.join(izvorna, ime)
                pot_cilj = os.path.join(ciljna, ime)
                shutil.move(pot_izvor, pot_cilj)
                premaknjeni.append(pot_cilj)

    return premaknjeni
