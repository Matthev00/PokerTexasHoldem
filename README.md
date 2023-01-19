## Poker Texas Hold'em

## Cel

Celem projektu było zrealizowanie gry w poker w odmianie texas hold'em, w której gracz może zmierzyc się z komputerem/ami, których decyzje mają być zauważalnie lepsze niż losowe.

## Uruchomienie i sposób użytkowania

Aby zagrać należy uruchomić plik texas_holdem.py(cała rozgrywka odbywa się w terminalu).
Następnie nalezy wprowadzić nazwę gracza, jeżeli nie zostanie wprowadzona to domyślnie ustawiana jest na 'Player', oraz liczbę graczy komputerowych(od 1 do 10 włącznie)
Gra się rozpoczyna.
Każdy z graczy ma na początku 10000.
Gracz może rozegrać nieskończenie wiele rund dopóki nie zdecyduje się odejść od stołu bądź straci wszystkie pieniądze.
Każda z rund rozpoczyna się od fazy licytacji, w której kazdy z graczy dostaje 2 karty.
Gracz podczas licytacji w kazdej turze może wybrać jedną z 4 opcji:
    - raise (podbicie powyżej podanej minimalnej stawki, wielokrotność 50)
    - call (sprawdzenie z podaną stawką)
    - fold (odpadznięcie z rundy)
    - all in (wejście ze wszystkimi swoimi pieniędzmi)
Kolejną fazą jest flop, w której pojawiają się trzy karty na stole. Znowu nastepuje licytacja.
Następną fazą jest river w której na stole pojawia się jedna karta. Licytacja analogicznie.
W fazie turn równiez pojawia się na stole jedna karta. Licytacja ma wymiar ostateczny.
Nastepnie ogłaszany jest zwycięzsca.
Jeżeli w ktorym kolwiek momencie przy stole zostaje jeden gracz runda się kończy, a zwycięzszca zgarnia nagrodę.
Wszelkie potrzebnę komunikaty wyświetlane są w terminalu.

## Co i jak ze sobą gada

Głównym plikiem jest texas_holdem.py gdzie znajduję się wstępny interfejs i tworzą sie instacje klas game oraz databese. Importowane są one z plików calasses.py oraz database.py.

Wszystkie niezbędne klasy niezwiązane z rankingiem znadują się w classes.py. Są tam klasy graczy, nadrzędna Player i 2 podrzędne ComputerPlayer oraz HumanPlayer, istotną funkcją tej pierwszej jest metoda meke_decision(), która pozwala komputerowi podjąc decyzję na podstwie wyniku funkcji score(). Funkcja score przypisuje wynik dla podanych kart. Klasa Card reprezentuję karty(kolor, figura). Klasa game tworzy instancje klas HumanPlayer, ComputerPlayer oraz z każdą rundą instancje klasy Table, wyświetla również niezbedne komunikaty w terminalu. Klasa Table jest najbardziej znaczącym elementem ponieważ to w niej odbywa sie cała licytacja oraz wszytkie fazy gry łącznie z decyzją kto wygrał. Znajduję się tam również funkcja create_deck(), ktora tworzy talię kart złożoną z 52 instancji klasy Card(każda karta jest różna). Talia jest potasowana.

W pliku database.py znajduję się klasa Database, w której metody pozwalające na pobranie i zwrócenie rankingu(za pomocą funkcji w pliku ranking_io.py) oraz metodę pozwaljącą dodanie nowego wpisu do rankingu i wypisanie go.

W pliku ranking_io.py zajdują się funkcję umożliwiające zapisy i odczytu pliku.