import os

mapa = 'static'

zamenjave = {
    'Crossword Compiler': 'VUS',
    'www.crossword-compiler.com': 'https://vus-flask2.onrender.com/',
}

for koren, mape, datoteke in os.walk(mapa):
    for datoteka in datoteke:
        if datoteka.endswith('.html') or datoteka.endswith('.js'):
            pot = os.path.join(koren, datoteka)

            with open(pot, 'r', encoding='utf-8') as f:
                vsebina = f.read()

            popravljeno = vsebina
            for originalno, novo in zamenjave.items():
                popravljeno = popravljeno.replace(originalno, novo)

            if popravljeno != vsebina:
                print(f'Popravljam datoteko: {pot}')
                with open(pot, 'w', encoding='utf-8') as f:
                    f.write(popravljeno)

print('Vse zamenjave so uspešno izvedene.')
