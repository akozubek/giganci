import langchain
from langchain_openai import ChatOpenAI

def read_file(path: str) -> str:
    with open(path, 'r') as file:
        contents = file.read()

        return contents

def main() -> None:
    lesson_outline_path = "./data/outline_clean.md"
    lesson_outline_raw = read_file(lesson_outline_path)
    print("File read")

    llm = ChatOpenAI(
        model="gpt-4o",
    )

    prompt = f"""
Jesteś doświadczonym edytorem edukacyjnym i korektorem języka polskiego.
Twoim zadaniem jest przekształcenie poniższego konspektu lekcji w zestaw informacji, które będą wykorzystane przez wirtualnego asystenta pomagającego dziecku (w wieku 10–12 lat) podczas lekcji programowania.

Uwzględnij następujące wytyczne:
- Wyodrębnij tylko te sekcje konspektu, które są potrzebne wirtualnemu asystentowi, czyli:
    - Cel lekcji
    - Spis treści (możesz przerobić na listę kroków)
    - Wstęp (podsekcje: przypomnienie, przedstawienie celu, opis gry, pytania)
    - Część właściwa lekcji: dokładnie opisz kroki rozwiązania
    - Zakończenie lekcji (całość, wszystkie podsekcje)
- Usuń wszystkie inne sekcje, w tym:
    - Rozmowa na luźne tematy
    - Wytyczne dla nauczyciela
    - Formy pracy na lekcji
    - Rekomendacje
    - Przegląd skryptów

- Ważne: Dokładnie opisz kroki rozwiązania, nadając im unikalne identyfikatory w formacie:
    - 1a, 1b, 1c itd. — dla pierwszego głównego etapu
    - 2a, 2b, 2c itd. — dla drugiego głównego etapu
    - itd dla kolejnych etapów rozwiazania
    - Jeśli jest etap rozszerzony, nadaj mu identyfikatory: bonus_a, bonus_b, bonus_c itd.
    - Dokładnie podaj, co dziecko ma zrobić w każdym kroku — nawet jeśli to drobny szczegół.
    - Każdy krok powinien być opisany w sposób prosty i zrozumiały dla dziecka (10–12 lat), jakby tłumaczył go starszy kolega.

Nie dodawaj komentarzy dla nauczyciela ani dodatkowych wyjaśnień technicznych.
Na końcu zwróć tylko gotowy, uporządkowany opis etapów i kroków dla wirtualnego asystenta, bez żadnych dodatkowych komentarzy, podsumowań czy uwag.

Konspekt lekcji poniżej:
{lesson_outline_raw}
"""
    print("Invoking LLM")
    response = llm.invoke(prompt)

    print(response.content)

if __name__ == '__main__':
    main()

    
