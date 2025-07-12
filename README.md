# LessonAssistant

## Opis agenta

Agent (LessonAssistant) został stworzony jako rozwiązanie zadania rekrutacyjnego. Jego celem jest wspieranie dziecka podczas lekcji online, w oparciu o dostarczony konspekt lekcji.

Agent działa zarówno w trybie głosowym, jak i tekstowym — odpowiada na pytania dziecka, udziela wskazówek i zachęca do samodzielnego myślenia.

W kanale wideo agent potrafi wyświetlać grafiki lub obrazy związane z rozwiązaniem (np. kolejne kroki lub gotową wersję gry). Potencjalnie może też pokazywać inne materiały graficzne lub wideo — na prośbę dziecka albo z własnej inicjatywy, jeśli uzna, że to potrzebne do lepszego zrozumienia lekcji.

Dzięki personalizacji (imię, płeć, pełny konspekt) agent prowadzi rozmowę w sposób przyjazny i dopasowany do uczestnika.

## Struktura kodu

- `data/` — wszystkie dane potrzebne do działania agenta: różne wersje konspektu lekcji (w formatach PDF, Markdown, TXT), przygotowane na potrzeby testów i eksperymentów. Dodatkowo zawiera obrazy kroków do wyświetlania podczas lekcji oraz projekty Scratch w wersji szablonowej i finalnej.
- `docs/` — dodatkowe materiały (np. zadanie rekrutacyjne).
- `example_users.yaml` — przykładowi użytkownicy (imię, płeć).
- `src/` — główny kod agenta:
    - `lesson_agent.py` — główna logika agenta.
    - `prompts.py` — teksty promptów.
    - `helpers.py` — funkcje pomocnicze (wczytywanie danych, ścieżki).
    - `image_streamer.py` — obsługa strumienia obrazu.    
- `tools/preprocessing/` — pomocnicze skrypty do przygotowania danych.
- `requirements.txt`  — zależności projektu.
- `requirements-tools.txt` — zależności dla skryptów w katalogu `tools`.
- `Makefile` — plik Makefile.
- `README.md` — plik README.

## Przygotowanie danych

Chciałam przygotować w pełni automatyczny pipeline do przetwarzania danych, ale na ten moment proces jest częściowo automatyczny, a częściowo ręczny.

Nie czytam danych bezpośrednio z pliku PDF ani z wyekstrahowanych danych PDF. Zamiast tego zdecydowałam się przetworzyć skrypt dla nauczyciela na dedykowany skrypt dla wirtualnego agenta. Dodatkowo testowałam różne warianty skryptów przygotowanych specjalnie dla dziecka (różne wersje można zobaczyć w katalogu `data/`).

Nie jest to dokładnie to, o co prosiliście w zadaniu, ale w praktyce daje dużo lepsze wyniki w kontekście naturalnej rozmowy z dzieckiem niż bezpośrednie czytanie z PDF.

Obrazki kroków przygotowałam ręcznie. Uważam jednak, że można stworzyć automatyczny proces przygotowania takich danych (przetworzony konspekt + obrazy) bezpośrednio ze źródłowych plików, na podstawie których wygenerowano PDF (zakładam, że macie dostęp do tych materiałów). Nie było to jednak głównym celem zadania, dlatego zdecydowałam się odpuścić pełną automatyzację.

W tym projekcie świadomie zrezygnowałam z użycia wektorowej bazy danych ze względu na konieczność działania w czasie rzeczywistym (kontekst z konspektu w zupełności wystarcza).

i jeszcze można jsony użyć

## Wnioski i uwagi

- Trochę trudno zmusić agenta, żeby mówił naturalnie i nie rozwlekał odpowiedzi. Nadal wypowiedzi są dość formalne i podręcznikowe jak na rozmowę z dzieckiem.
- Głos w języku polskim ma fatalny amerykański akcent. W Cartesii nie ma prawdziwego polskiego głosu. Zdecydowałam się użyć tego, co było dostępne. Trzeba by poszukać, czy w ogóle istnieje polski głos dostępny w czasie rzeczywistym — to jest absolutnie niezbędne do stworzenia dobrej jakości agenta głosowego dla dzieci! (To będzie też wyzwanie w innych językach).