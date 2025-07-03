import os
import shutil

def premakni_krizanke():
    izvorna = os.path.join("../static", "Krizanke", "CrosswordCompilerApp", "CrosswordCompilerApp")
    ciljna = os.path.join("../static", "Krizanke", "CrosswordCompilerApp")
    html_arhiv = os.path.join(os.path.expanduser("~"), "Desktop", "CC_html_arhiv")
    os.makedirs(html_arhiv, exist_ok=True)

    if os.path.exists(izvorna):
        for ime in os.listdir(izvorna):
            izvorna_pot = os.path.join(izvorna, ime)
            if ime.endswith(".xml") or ime.endswith(".js"):
                shutil.move(izvorna_pot, os.path.join(ciljna, ime))
                print(f"✅ Premaknjeno: {ime}")
            elif ime.endswith(".html"):
                shutil.move(izvorna_pot, os.path.join(html_arhiv, ime))
                print(f"📥 HTML na namizje: {ime}")
        try:
            os.rmdir(izvorna)
        except OSError:
            pass
    else:
        print("❌ Pot do križank ne obstaja.")

def premakni_sudoku(tezavnost):
    izvorna = os.path.join("../static", "Sudoku_export")
    ciljna = os.path.join("../static", f"Sudoku_{tezavnost}")
    html_arhiv = os.path.join(os.path.expanduser("~"), "Desktop", "Sudoku_html_arhiv")
    os.makedirs(ciljna, exist_ok=True)
    os.makedirs(html_arhiv, exist_ok=True)

    if os.path.exists(izvorna):
        for ime in os.listdir(izvorna):
            izvorna_pot = os.path.join(izvorna, ime)
            if ime.endswith(".js"):
                shutil.move(izvorna_pot, os.path.join(ciljna, ime))
                print(f"✅ Sudoku JS: {ime}")
            elif ime.endswith(".html"):
                shutil.move(izvorna_pot, os.path.join(html_arhiv, ime))
                print(f"📥 HTML na namizje: {ime}")
    else:
        print("❌ Pot do sudokujev ne obstaja.")

if __name__ == "__main__":
    print("Kaj uvažaš?")
    print("1 = Križanka")
    print("2 = Sudoku")

    izbira = input("Izberi (1/2): ").strip()

    if izbira == "1":
        premakni_krizanke()
    elif izbira == "2":
        tezavnost = input("Vpiši težavnost (very_easy, easy, medium, hard): ").strip()
        premakni_sudoku(tezavnost)
    else:
        print("❌ Napačna izbira.")
