# pretvornik.py - Modul za normalizacijo črk

def normaliziraj_geslo(geslo):
    pretvornik = {
        # Slovenski znaki
        'Š': 'S', 'š': 's',
        'Ž': 'Z', 'ž': 'z',
        'Č': 'C', 'č': 'c',
        'Ć': 'C', 'ć': 'c',
        'Đ': 'D', 'đ': 'd',

        # Ostali znaki
        'Á': 'A', 'À': 'A', 'Â': 'A', 'Ä': 'A', 'Ā': 'A', 'Ã': 'A', 'Å': 'A', 'Ą': 'A',
        'á': 'a', 'à': 'a', 'â': 'a', 'ä': 'a', 'ā': 'a', 'ã': 'a', 'å': 'a', 'ą': 'a',

        'É': 'E', 'È': 'E', 'Ê': 'E', 'Ë': 'E', 'Ē': 'E', 'Ę': 'E',
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e', 'ē': 'e', 'ę': 'e',

        'Ń': 'N', 'Ñ': 'N', 'Ň': 'N', 'Ņ': 'N', 'Ŋ': 'N',
        'ń': 'n', 'ñ': 'n', 'ň': 'n', 'ņ': 'n', 'ŋ': 'n',

        'Ó': 'O', 'Ò': 'O', 'Ô': 'O', 'Ö': 'O', 'Ō': 'O', 'Ő': 'O', 'Ø': 'O', 'Ŏ': 'O', 'Ơ':'O',
        'ó': 'o', 'ô': 'o', 'ö': 'o', 'ō': 'o', 'ő': 'o', 'ø': 'o', 'õ': 'o', 'ŏ': 'o', 'ơ':'o',

        'Ú': 'U', 'Ù': 'U', 'Û': 'U', 'Ü': 'U', 'Ū': 'U', 'Ů': 'U', 'Ű': 'U', 'Ų': 'U',
        'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u', 'ū': 'u', 'ů': 'u', 'ű': 'u', 'ų': 'u',

        'Í': 'I', 'Ì': 'I', 'Î': 'I', 'Ï': 'I', 'Ī': 'I', 'Ĭ': 'I', 'Į': 'I', 'İ': 'I',
        'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i', 'ī': 'i', 'ĭ': 'i', 'į': 'i', 'ı': 'i',

        'B́': 'B', 'B̀': 'B', 'B̂': 'B', 'B̈': 'B', 'B̄': 'B', 'Ḃ': 'B', 'B̨': 'B',
        'b́': 'b', 'b̀': 'b', 'b̂': 'b', 'b̈': 'b', 'ḃ': 'b', 'b̨': 'b',

        'Ĉ': 'C', 'Ç': 'C', 'Ċ': 'C', 'C̄': 'C',
        'ĉ': 'c', 'ç': 'c', 'ċ': 'c', 'c̄': 'c',

        'D́': 'D', 'D̀': 'D', 'D̂': 'D', 'D̈': 'D', 'D̄': 'D', 'Ḋ': 'D', 'D̨': 'D',
        'd́': 'd', 'd̀': 'd', 'd̂': 'd', 'd̈': 'd', 'd̄': 'd', 'ḋ': 'd', 'd̨': 'd',

        'F́': 'F', 'F̀': 'F', 'F̂': 'F', 'F̈': 'F', 'F̄': 'F', 'Ḟ': 'F', 'F̨': 'F',
        'f́': 'f', 'f̀': 'f', 'f̂': 'f', 'f̈': 'f', 'f̄': 'f', 'ḟ': 'f', 'f̨': 'f',

        'Ǵ': 'G', 'G̀': 'G', 'Ĝ': 'G', 'G̈': 'G', 'Ḡ': 'G', 'Ġ': 'G', 'G̨': 'G',
        'ǵ': 'g', 'g̀': 'g', 'ĝ': 'g', 'g̈': 'g', 'ḡ': 'g', 'ġ': 'g', 'g̨': 'g',

        'H́': 'H', 'H̀': 'H', 'Ĥ': 'H', 'Ḧ': 'H', 'H̄': 'H', 'Ḣ': 'H', 'H̨': 'H',
        'h́': 'h', 'h̀': 'h', 'ĥ': 'h', 'ḧ': 'h', 'h̄': 'h', 'ḣ': 'h', 'h̨': 'h',

        'J́': 'J', 'J̀': 'J', 'Ĵ': 'J', 'J̈': 'J', 'J̄': 'J', 'J̇': 'J', 'J̨': 'J',
        'j́': 'j', 'j̀': 'j', 'ĵ': 'j', 'j̈': 'j', 'j̄': 'j', 'j̇': 'j', 'j̨': 'j',

        'Ḱ': 'K', 'K̀': 'K', 'K̂': 'K', 'K̈': 'K', 'K̄': 'K', 'K̇': 'K', 'K̨': 'K',
        'ḱ': 'k', 'k̀': 'k', 'k̂': 'k', 'k̈': 'k', 'k̄': 'k', 'k̇': 'k', 'k̨': 'k',

        'Ĺ': 'L', 'Ļ': 'L', 'Ľ': 'L', 'Ŀ': 'L', 'Ł': 'L',
        'ĺ': 'l', 'ļ': 'l', 'ľ': 'l', 'ŀ': 'l', 'ł': 'l',

        'Ś': 'S', 'ś': 's', 'Ź': 'Z', 'Ż': 'Z', 'ź': 'z', 'ż': 'z',
        # Ostale črke nadaljuj tukaj, če jih boš še dodajal.
    }

    return ''.join(pretvornik.get(char, char) for char in geslo)
import unicodedata
import re

def normaliziraj_ime(opis):
    # Pretvori vse črke z naglasi v ASCII ekvivalente
    ime = unicodedata.normalize('NFD', opis).encode('ascii', 'ignore').decode('utf-8')
    ime = ime.lower()

    # Presledke pretvori v podčrtaje
    ime = ime.replace(' ', '_')

    # Odstrani vse, kar ni črka, številka ali podčrtaj
    ime = re.sub(r'[^a-z0-9_]', '', ime)

    # Po potrebi: omeji na prvih 15 "besed"
    besede = ime.split('_')
    ime = '_'.join(besede[:20])

    return ime
