"""
my own part of halma with minimax
"""

def ruchlosowy(plansza, gracz):
    """
    Przykladowa funkcja typu ruch - ale tylko losowa
    Uwaga - oczywiscie generuje takze nieprawidlowe ruchy
    @TODO: poprawic by zwracane byly tylko dobre ruchy
    """
    (pocz, kon) = minimax(plansza, gracz, 100, 101)[1]
    return (pocz, kon)

def znajdz(plansza, co):
    return [(i, j) for i in range(plansza.N()) for j in range(plansza.K())
            if plansza.t[i][j] == co]

def planszalosowa(N, K, M):
    """
    @TODO: zaimplementowac planszalosowa(N,K,M)
    """
    plansza = []
    m = M  # zmienna pozwalajaca nie zmieniac wartosci zmiennej M
    for i in range(N):  # wstawiamy pionki biale, pola puste oraz zablokowane
        plansza.append([])
        for j in range(m):
            plansza[-1].append('b')
        for j in range(K - m):
            plansza[-1].append(random.choice('............X...'))
        if m > 0:
            m -= 1

    m = M
    for i in range(N):  # wstawiamy pionki czarne
        for j in range(m):
            plansza[-i-1][-j-1] = 'c'
        if m > 0:
            m -= 1
    plansza2 = [''.join(i) for i in plansza]
    return Plansza(*plansza2)  # zwracamy plansze jako liste stringow

def stanrozgrywki(plansza):
    """
    @TODO: zaimplementowac stanrozgrywki(plansza):
    """
    m = M  # zmienna pozwalajaca nie zmieniac wartosci zmiennej M
    check = True
    for i in range(len(plansza.t)):
        for j in range(m):
            if plansza.t[i][j] != 1:
                check = False
        if m > 1:
            m -= 1
        else:
            break
    if check == True:
        return HBLACK  # zwraca wartosc dla HBLACK, gdy czarny wygrywa

    m = M
    check = True
    for i in range(len(plansza.t)):
        for j in range(m):
            if plansza.t[-i - 1][-j - 1] != 0:
                check = False
        if m > 1:
            m -= 1
        else:
            break
    if check == True:
        return HWHITE  # zwraca wartosc dla HWHITE, gdy bialy wygrywa
    return -1  # zwraca -1, gdy gra nierozstrzygnieta

def ruch(plansza, gracz):
    """
    @TODO: zaimplementowac ruch(plansza, gracz)
    """
    (pocz, kon) = minimax(plansza, gracz, 100, 101)[1]
    return (pocz, kon)

def minimax(plansza, gracz, glebokosc, limit):
    check = stanrozgrywki(plansza)
    # sprawdza stan rozgrywki
    if check == HWHITE:
        ocena = 99999
        return ocena, None
    elif check == HBLACK:
        ocena = -99999
        return ocena, None
    if limit == glebokosc:
        return wycena(plansza), None

    n = 100000  # duza liczba zamiast nieskonczonosci
    best_move = None

    # tworzy priorytet dla odpowiedniego gracza
    if gracz == HBLACK:
        best = n
    elif gracz == HWHITE:
        best = -1 * n

    for i in ruchy_sym(plansza, gracz):
        ocena = minimax(symulacja_ruchu(plansza, i), (gracz + 1) % 2, \
                        glebokosc + 1, limit)[0]
        if gracz == HBLACK:
            if ocena <= best:
                best = ocena
                best_move = i
        elif gracz == HWHITE:
            if ocena >= best:
                best = ocena
                best_move = i
    return best, best_move

def ruchy_sym(plansza, gracz):
    # zwraca liste ruchow w odpowiedniej postaci
    l = []  # tworzymy liste mozliwych ruchow
    for x in znajdz(plansza, gracz):
        for y in dostepne(x, plansza):
            l.append((x, y))
    return l  # zwraca liste krotek krotek

def wycena(plansza):
    # zwraca ocene w zaleznosci od "odleglosci" pionkow od celu
    check = stanrozgrywki(plansza)
    # sprawdza stan rozgrywki
    if check == HWHITE:
        ocena = 99999
        return ocena
    elif check == HBLACK:
        ocena = -99999
        return ocena
    elif check == -1:
        odlb = 0
        odlc = 0
        for i in znajdz(plansza, HBLACK):
            odlc = odlc + (i[0] + i[1])
        for i in znajdz(plansza, HWHITE):
            odlb = odlb + (plansza.N() - 1 - i[0] + plansza.K() - 1 - i[1])
        ocena = odlc - odlb
        return ocena

def symulacja_ruchu(plansza, pocz_kon):
    # funkcja symulujaca ruch na kopii planszy
    plansza2 = copy.deepcopy(plansza)  # kopiuje plansze
    # zamieniamy pole poczatkowe z koncowym
    plansza2.t[pocz_kon[1][0]][pocz_kon[1][1]] = \
    plansza2.t[pocz_kon[0][0]][pocz_kon[0][1]]
    plansza2.t[pocz_kon[0][0]][pocz_kon[0][1]] = HFREE
    return plansza2  # zwraca kopie planszy po symualcji

def dostepne(pole, plansza):
    # sprawdza plansze i zwraca zbior dostepnych pol
    sasiednie = []  # lista pol sasiednich
    for i in ((pole[0] + 1, pole[1] - 1), (pole[0] - 1, pole[1]),
              (pole[0] - 1, pole[1] - 1), (pole[0], pole[1] - 1),
              (pole[0], pole[1] + 1), (pole[0] + 1, pole[1] + 1),
              (pole[0] + 1, pole[1]), (pole[0] - 1, pole[1] + 1)):
        if i[0] in range(plansza.N()) and i[1] in range(plansza.K()):
            sasiednie.append(i)

    wolne = set()  # zbior dostepnych pol
    zajete = []  # lista zajetych pol
    for i in sasiednie:
        if plansza.t[i[0]][i[1]] == HFREE:
            wolne.add(i)
        elif plansza.t[i[0]][i[1]] != HFREE:
            zajete.append(i)

    # funkcja pomocnicza pozwalajaca znalezc dostepne pola z niesasiednich pol
    def kolejne(x, pole):
        y = list(x)
        if y[0] > pole[0]:
            y[0] += 1
        elif y[0] < pole[0]:
            y[0] -= 1
        if y[1] > pole[1]:
            y[1] += 1
        elif y[1] < pole[1]:
            y[1] -= 1
        z = tuple(y)
        return z  # zwraca kolejne pole do przeanalizowania

    while zajete:  # analiza kolejnych pol, gdy jakeis zajete
        zajete2 = zajete[:]
        for i in range(len(zajete)):
            (a, b) = zajete2.pop()
            (a, b) = kolejne((a, b), pole)
            if a in range(plansza.N()) and b in range(plansza.K()):
                if plansza.t[a][b] == HFREE:
                    wolne.add((a, b))
                elif plansza.t[a][b] != HFREE:
                    zajete2.append((a, b))
            else:
                continue
        zajete = zajete2[:]
    return wolne  # zwraca zbior dostepnych pol w krotkach

def dobryruch(plansza, skad, dokad):
    """
    Sprawdza czy ruch pionkiem z pola skad do dokad dla gracza gracz
    jest zgodny z zasadami gry
    @TODO: zaimplementowac dobryruch(plansza, skad, dokad, gracz)
    """
    # sprawdza czy pole jest wolne, jesli nie zwraca False
    if plansza.t[dokad[0]][dokad[1]] != HFREE:
        return False
    # sprawdza czy ruch o 1 pole, jesli tak - True
    if abs(dokad[0] - skad[0]) < 2 and abs(dokad[1] - skad[1]) < 2:
        return True
    # sprawdza czy wybrane pole jest dostepne, jesli nie - False
    if dokad not in dostepne(skad, plansza):
        return False
    return True

if __name__ == "__main__":
    print('Witaj w grze halma!\n\n')
    print('Czy chcesz skorzystać z pomocy?')
    pomoc = input('Wpisz POMOC, aby skorzystac. Cokolwiek, aby pominac: ')
    if pomoc == 'POMOC':
        plik = open('README.txt').read()
        print(plik)
        print('\n\n')
    print('Wybierz rozmiar planszy i ilosc pionkow jednego gracza.')
    check = False  # zmienna pomagajaca zatrzymac niepoprawny input
    while check != True:  # wybor liczby wierszy planszy
        try:
            N = float(input('Liczba wierszy: '))
        except:
            print('Niepoprawna fraza! Sprobuj ponownie.')
            continue
        if N < 2 or N != int(N):
            print('Nieprawidlowa liczba wierszy! Sprobuj ponownie.')
        else:
            check = True
            N = int(N)

    check = False
    while check != True:  # wybor liczby kolumn planszy
        try:
            K = float(input('Liczba kolumn: '))
        except:
            print('Niepoprawna fraza! Sprobuj ponownie.')
            continue
        if K < 2 or K != int(K):
            print('Nieprawidlowa liczba kolumn! Sprobuj ponownie.')
        else:
            check = True
            K = int(K)

    check = False
    while check != True:  # wybor liczby pionkow graczy
        try:
            m = float(input('Liczba pionkow (np.: 1, 3, 6, 10, 15, 21...): '))
        except:
            print('Niepoprawna fraza! Sprobuj ponownie.')
            continue
        M = ((8 * m + 1) ** 0.5 - 1) / 2
        if M < 1 or M != int(M):
            print('Nieprawidlowa liczba pionkow! Sprobuj ponownie.')
        elif M > K - 1 or M > N - 1:
            print('Za duza liczba pionkow! Sprobuj ponownie.')
        elif m != int(m):
            print('Wprowadz liczbe calkowita! Sprobuj ponownie.')
        else:
            check = True
            M = int(M)

    print('Wybierz tryb gry (odpowiednio: biale vs czarne):\n\
        1 - komputer vs gracz (czarne),\n\
        2 - komputer vs komputer,\n\
        3 - komputer vs gracz (biale),\n\
        4 - gracz vs gracz.')
    tryb = input('Wpisz numer trybu: ')  # wybor trybu gry
