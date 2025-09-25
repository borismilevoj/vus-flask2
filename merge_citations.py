import csv, sys, os, re

NEW_PATH = r'out/cc_clues_DISPLAY_UTF8.csv'      # Word (z razmaki), Clue, Citation(prazno)
OLD_PATH = sys.argv[1] if len(sys.argv)>1 else r'imports/old_clues_with_citation.csv'
OUT_PATH = r'out/cc_clues_DISPLAY_MERGED_UTF8.csv'

def clean(s):
    if not s: return ""
    s = s.replace("\u00A0"," ")
    s = re.sub(r"[\uFEFF\u200B\u200C\u200D\u2060]", "", s)
    return re.sub(r"\s+", " ", s.strip())

def norm_keys(word):
    w = clean(word).upper()
    no_space = re.sub(r"[ \-\u2010-\u2015'’]", "", w)
    return w, no_space

def sniff(path):
    with open(path, encoding='utf-8-sig', newline='') as f:
        sample = f.read(8192)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=',;\t')
        except Exception:
            class D: delimiter=',' 
            dialect = D()
        rows = list(csv.reader(f, dialect))
    return rows, dialect.delimiter

def has_header(tokens):
    # če se kateri token glasi kot ime polja, obravnavaj kot header
    names = {'word','answer','entry','solution','clue','definition','opis','citation','source','vir','date'}
    t = [clean(x).lower() for x in tokens]
    return any(x in names for x in t)

# --- preberi STARI export (brez glave ali z glavo) ---
old_rows, old_delim = sniff(OLD_PATH)
old_map = {}
nonempty = 0
if not old_rows:
    print(f'! Prazen: {OLD_PATH}')
else:
    # ugotovi, ali je prva vrstica header
    header_mode = has_header(old_rows[0])
    start = 1 if header_mode else 0
    # postavi indekse stolpcev
    if header_mode:
        hdr = [clean(x).lower() for x in old_rows[0]]
        def idx(cands):
            cands = [c.lower().replace(' ','') for c in cands]
            hdr2  = [h.replace(' ','') for h in hdr]
            for i,h in enumerate(hdr2):
                if h in cands: return i
            return None
        w_i = idx(['word','answer','entry','solution'])
        cit_i = idx(['citation','citations','cite','source','vir','reference'])
        clue_i = idx(['clue','definition','opis'])
    else:
        # brez glave: najpogostejši format je Word,Clue,(Date),Citation
        ncol = len(old_rows[0])
        w_i   = 0
        clue_i= 1 if ncol >= 2 else None
        cit_i = 3 if ncol >= 4 else (2 if ncol >=3 else None)

    for r in old_rows[start:]:
        w = clean(r[w_i]) if w_i is not None and w_i < len(r) else ""
        cit = clean(r[cit_i]) if cit_i is not None and cit_i < len(r) else ""
        if not w or not cit: continue
        nonempty += 1
        k1,k2 = norm_keys(w)
        old_map.setdefault(k1, cit)
        old_map.setdefault(k2, cit)

print(f"Stari CSV: delimiter '{old_delim}', vrstic={len(old_rows)}, z nepraznim Citation={nonempty}")

# --- preberi NOV CSV (z glavo Word,Clue,Citation) in zlij ---
new_rows, new_delim = sniff(NEW_PATH)
if not new_rows:
    raise SystemExit(f'! Prazen: {NEW_PATH}')

# nova datoteka IMA glavo
hdr = [clean(x).lower() for x in new_rows[0]]
def nidx(cands):
    c = [x.lower().replace(' ','') for x in cands]
    h = [x.replace(' ','') for x in hdr]
    for i,x in enumerate(h):
        if x in c: return i
    return None
word_i = nidx(['word','answer','entry','solution'])
clue_i = nidx(['clue','definition','opis'])
cit_i  = nidx(['citation','source','vir','reference'])

merged = 0
with open(OUT_PATH, 'w', encoding='utf-8-sig', newline='') as fout:
    w = csv.writer(fout, lineterminator='\r\n')
    w.writerow(['Word','Clue','Citation'])
    for r in new_rows[1:]:
        word = clean(r[word_i]) if word_i is not None and word_i < len(r) else ""
        clue = clean(r[clue_i]) if clue_i is not None and clue_i < len(r) else ""
        cit  = clean(r[cit_i]) if cit_i is not None and cit_i < len(r) else ""
        if not cit:
            k1,k2 = norm_keys(word)
            cit = old_map.get(k1) or old_map.get(k2) or ""
            if cit: merged += 1
        w.writerow([word, clue, cit])

print(f"✔ Merged {merged} citations into {len(new_rows)-1} rows -> {OUT_PATH}")
