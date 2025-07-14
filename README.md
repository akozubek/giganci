# LessonAssistant

## Opis agenta

**LessonAssistant** to agent wspierający ucznia podczas lekcji online, w oparciu o dostarczony konspekt lekcji. Działa w trybie głosowym i tekstowym — odpowiada na pytania, udziela wskazówek oraz zachęca do samodzielnego myślenia i szukania rozwiązań.

W kanale wideo agent potrafi wyświetlać grafiki lub obrazy związane z rozwiązaniem (np. kolejne kroki lub gotową wersję gry). Potencjalnie może też pokazywać inne materiały graficzne lub wideo — na prośbę dziecka albo z własnej inicjatywy, jeśli uzna, że to potrzebne do lepszego zrozumienia lekcji.

Agent zna imię oraz płeć dziecka, dzięki czemu zwraca się do niego we właściwym rodzaju gramatycznym. 

[Film pokazujący działanie agenta](https://www.loom.com/share/0c4bbdbfaf7444fea2b6f74fce8bdbc3?sid=ea41cd36-9aaf-4f45-8fba-e59004f1710c)


## Instrukcja uruchomienia

Instrukcje uruchomienia dla Linuksa. 

W pliku `.env` dodaj klucze:
```
# Klucz API do transkrypcji mowy
DEEPGRAM_API_KEY=your_deepgram_api_key_here
# Klucz API do komunikacji z modelem OpenAI
OPENAI_API_KEY=your_openai_api_key_here
# Klucz API do Cartesia
CARTESIA_API_KEY=your_cartesia_api_key_here
# Klucz API do LiveKit 
LIVEKIT_API_KEY=your_livekit_api_key_here
# Sekretny klucz do LiveKit (do uwierzytelniania)
LIVEKIT_API_SECRET=your_livekit_api_secret_here
# URL serwera LiveKit
LIVEKIT_URL=your_livekit_url_here
```

Stwórz środowisko wirtualne:
```
python -m venv venv
```

Aktywuj środowisko:
```
source venv/bin/activate
```

Zainstaluj zależności:
```
pip install -r requirements.txt
```

Uruchom wersję deweloperską:
```
make dev
```

Uruchom wersję głosową w konsoli.
```
make console
```



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

Nie wszystkie kroki mają przygotowane obrazki — celowo pominęłam część z nich, ponieważ w ramach tego POC chciałam skupić się głównie na przetestowaniu mechanizmu, a nie na kompletności wszystkich grafik (czytaj: nie chciało mi się ;-)).

W tym projekcie świadomie zrezygnowałam z użycia wektorowej bazy danych ze względu na konieczność działania w czasie rzeczywistym, a kontekst z konspektu w zupełności wystarcza.



## Wnioski i uwagi

- Trochę trudno zmusić agenta, żeby mówił naturalnie i nie rozwlekał odpowiedzi. Nadal wypowiedzi są dość formalne i podręcznikowe jak na rozmowę z dzieckiem.
- Głos w języku polskim ma fatalny amerykański akcent. W Cartesii nie ma prawdziwego polskiego głosu. Zdecydowałam się użyć tego, co było dostępne. Trzeba by poszukać, czy w ogóle istnieje polski głos dostępny w czasie rzeczywistym — to jest absolutnie niezbędne do stworzenia dobrej jakości agenta głosowego dla dzieci! 
- W plikach `.sb3` (projektach Scratch) znajduje się plik `project.json`, który zawiera pełną strukturę projektu (np. bloki kodu, sprite’y, zmienne). Można go dodatkowo wykorzystać, żeby agent jeszcze dokładniej podpowiadał dziecku, co zrobić w danym momencie lub jak naprawić błąd. Na potrzeby tego POC nie używałam tych danych, ale w przyszłości można je zintegrować, żeby jeszcze bardziej wzbogacić rozmowę i wsparcie agenta.
- Wszystkie wyzwania języka polskiego (formalność języka, płeć rozmówcy, akcent) będą równie problematyczne w innych językach.
- Koszty: 
  - LLM: w tej chwili agent działa na modelu gpt-4o-mini, który jest tanim modelem
  - STT: w czasie testowania agenta zużyłam $0.50 z kredytów Deepgrama
  - TTS: w Cartesii zużyłam ok. 60 tysięcy tokenów (moim zdaniem dużo). Cennik Cartesii jest następujący:  
    - Plan Startup: 1.25M tokenów na miesiąc: $49/miesiąc
    - Plan Scale: 8M tokenów na miesiąc: $299/miesiąc

