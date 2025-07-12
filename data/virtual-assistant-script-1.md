## Cel lekcji
Na lekcji stworzymy grę w Scratchu, w której steruje się Batyskafem i strzela pociskiem do podwodnych bestii w celu zdobycia punktów. Gra będzie wykorzystywała mechanizmy losowego pojawiania się przeciwników oraz poznamy mechanizm klonowania dysków.

## Spis treści

1. Wstęp
2. Ustawienia początkowe oraz tworzenie sterowania batyskafem
3. Mechanizm strzału - klonowanie
4. Dodanie przeciwników
5. Warunki zwycięstwa oraz przegranej - komunikaty
6. Weryfikacja celu lekcji i efektów uczenia się
7. Zadanie dodatkowe (Opcjonalne)

## Wstęp

### Przypomnienie zagadnień z poprzednich lekcji

1. Poprzednio stworzyliśmy grę Pacman z poruszającymi się po labiryncie postaciami i przeciwnikami reagującymi na ściany dzięki kolorowym kwadratom.
2. Omawialiśmy różne efekty duszków jak duch, rybie oko, które tymczasowo zmieniają wygląd duszka.

### Przedstawienie celu lekcji

Dowiesz się, jak:
- klonować duszki,
- używać komunikatów między duszkami,
- sterować Batyskafem w cztery kierunki.

### Opis gry

Stworzymy podwodną grę z batyskafem, gdzie trzeba będzie pokonać rekiny. Wykorzystamy klonowanie do strzelania pociskami i wysyłanie komunikatów między postaciami.

### Dodatkowe pytania

1. Batyskaf to podwodny statek badawczy. Kojarzy się z eksploracją i odkrywaniem głębin.
2. W projekcie widać batyskaf, rekiny, zmienne punkty i HP, klonowanie pocisków oraz komunikaty.

## Część właściwa lekcji

### Ustawienia początkowe oraz tworzenie sterowania batyskafem

1a. Ustaw początkowe wartości zmiennych Punktów oraz HP.
1b. Ustaw pozycję startową batyskafu na scenie i pokaż statek.
1c. Zastosuj sterowanie lewo-prawo dla batyskafu za pomocą klawiszy strzałek.
1d. Dodaj sterowanie góra-dół wykonując samodzielnie lub przy pomocy trenera.
1e. Dodaj blokadę, by batyskaf nie mógł wypłynąć poza scenę.

### Mechanizm strzału - klonowanie

2a. Ukryj oryginalny duszek-pocisk.
2b. Na naciśnięcie "Spacji", utwórz klona poprzez odpowiedni blok "utwórz klona".
2c. Ustal, jak szybko pojawiają się klony, ustawiając czas w bloku "czekaj".
2d. Zaprogramuj klon, by pojawiał się na pozycji batyskafu i poruszał się po osi x.
2e. Usuń klon, gdy dotknie krawędzi.

### Dodanie przeciwników

3a. Zacznij od klonowania rekinów co określoną ilość czasu.
3b. Każdemu klonowi daj losową pozycję x i stałą wysokość.
3c. Programuj losową wielkość rekina, żeby były różnorodne.
3d. Rekiny poruszają się po osi y w dół aż do krawędzi.
3e. Dodaj warunek: gdy rekin dotknie pocisku, znika; gracz zdobywa punkt. Gdy dotknie batyskafu, batyskaf traci życie.

### Warunki zwycięstwa oraz przegranej - komunikaty

4a. Ustaw początkowe tło gry.
4b. Ustal, kiedy gracze wygrywają lub przegrywają (np. stracone całe HP lub zdobycie określonej liczby punktów).
4c. Wyślij odpowiednie komunikaty między duszkami, by reagowały na wygraną lub przegraną.
4d. Ukryj duszki po zakończeniu gry.

### Weryfikacja celu lekcji i efektów uczenia się

5a. Grają i testują swoje projekty, sprawdź, czy działają poprawnie.
5b. Pytaj uczestników o mechanizmy klonowania, użyte bloki warunkowe i komunikację w grze.

### Zadanie dodatkowe (Opcjonalne)

bonus_a. Dodaj bossa jako przeciwnika, który ma poruszać się od krawędzi do krawędzi.
bonus_b. Ustal zmienne HP Boss i Punkty dla gracza.
bonus_c. Stwórz warunki zwycięstwa uwzględniające pokonanie bossa.
bonus_d. Dodaj efekty kolizji z bossem i pociski z podwozia bossa, które kierują się w stronę batyskafu.

## Zakończenie lekcji

### Podsumowanie lekcji

Podsumuj dzisiejszy projekt, zadania i umiejętności, które zdobyto. Zapytaj o wrażenia z projektu i pomysły na ulepszenie.

### Zapowiedź kolejnej lekcji

Zdradź krótko, że na kolejnych zajęciach stworzycie własną wersję gry T-rex, podobnej do tej w Google Chrome, z mechanizmem skoku i przewijanym tłem.

### Pytania od uczestników

Zapytaj, czy są pytania dotyczące bieżącego projektu lub inne związane z programowaniem.
