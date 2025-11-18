#!/usr/bin/env python3
import sys, os, argparse, glob, unicodedata

REPLACEMENTS = {
    # narekovaji
    '\u201C':'"', '\u201D':'"', '\u201E':'"', '\u00AB':'"', '\u00BB':'"',
    '\u2018':"'", '\u2019':"'", '\u201A':"'", '\u2039':"'", '\u203A':"'",
    # pomišljaji / vezaji
    '\u2013':'-', '\u2014':'-', '\u2212':'-',
    # elipsa
    '\u2026':'...',
    # presledki
    '\u00A0':' ', '\u2007':' ', '\u202F':' ',
    # pike/simboli pogosti po copy-paste
    '\u2022':'-', '\u25CF':'-', '\u00B7':'-',
    # stopinje
    '\u00B0':'°',
}

def strip_bom_zw(s: str) -> str:
    # BOM/zero-width in soft line sep
    for ch in ('\ufeff', '\u200b', '\u200c', '\u200d', '\u2060', '\u2028', '\u2029'):
        s = s.replace(ch, '')
    return s

def remove_control_chars(s: str) -> str:
    # dovoli tab, CR, LF; odstrani ostalo (vključno z U+0080–009F, torej U+0090)
    return ''.join(c for c in s
                   if c in '\t\r\n' or (32 <= ord(c) <= 126) or (160 <= ord(c)))

def replace_typography(s: str) -> str:
    for k, v in REPLACEMENTS.items():
        s = s.replace(k, v)
    return s

def deaccent_if_needed(s: str) -> str:
    # ne odstranjujemo šumnikov! (ti so v cp1250)
    return s

def to_crlf(s: str) -> str:
    return s.replace('\r\n','\n').replace('\r','\n').replace('\n','\r\n')

def sanitize(s: str) -> str:
    s = strip_bom_zw(s)
    s = replace_typography(s)
    s = remove_control_chars(s)
    s = '\n'.join(line.rstrip(' \t') for line in s.splitlines())
    return to_crlf(s)

def process_file(path, inplace=False, suffix="_ANSI"):
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        txt = f.read()

    txt = sanitize(txt)

    root, ext = os.path.splitext(path)
    out_path = path if inplace else f"{root}{suffix}{ext}"

    try:
        data = txt.encode('cp1250', errors='strict')
    except UnicodeEncodeError as e:
        # zadnji poskus: odstrani diakritične znake, ki niso v cp1250
        nfkd = unicodedata.normalize('NFKD', txt)
        stripped = ''.join(ch for ch in nfkd if not unicodedata.combining(ch))
        data = stripped.encode('cp1250', errors='ignore')

    with open(out_path, 'wb') as f:
        f.write(data)

    print(f"✔ {path}  →  {out_path}  (cp1250, CRLF)")

def expand_inputs(args_paths):
    inputs = []
    for p in args_paths:
        if os.path.isdir(p):
            inputs += glob.glob(os.path.join(p, "*.txt"))
            inputs += glob.glob(os.path.join(p, "*.csv"))
        else:
            inputs.append(p)
    return sorted(set(inputs))

def main():
    ap = argparse.ArgumentParser(description="Pretvori TXT/CSV v ANSI (cp1250) + CRLF za CC")
    ap.add_argument('paths', nargs='+', help="Datoteke ali mape (npr. out)")
    ap.add_argument('--inplace', action='store_true', help="Prepiši izvorne datoteke")
    ap.add_argument('--suffix', default="_ANSI", help="Pripona izhodnih datotek")
    args = ap.parse_args()

    files = expand_inputs(args.paths)
    if not files:
        print("Ni najdenih .txt/.csv")
        sys.exit(1)

    for f in files:
        try:
            process_file(f, inplace=args.inplace, suffix=args.suffix)
        except Exception as e:
            print(f"✖ {f}: {e}")

if __name__ == "__main__":
    main()
