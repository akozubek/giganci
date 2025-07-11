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
Twoim zadaniem jest przekształcenie poniższego konspektu lekcji dla nauczyciela w prosty, przyjazny i zrozumiały skrypt dla ucznia, który będzie używany przez AI w trakcie lekcji.

Uwzględnij następujące wytyczne:

- Zostaw następujące sekcje i nagłówki w skrypcie dla ucznia:
  - Cel lekcji
  - Spis treści (możesz przerobić na listę kroków lub checklistę)
  - Wstęp (część: Wstęp, podsekcje: rozmowa na luźne tematy, przypomnienie, przedstawienie celu, opis gry, pytania)
  - Część właściwa lekcji (całość, wszystkie podsekcje)
  - Zakończenie lekcji (całość, wszystkie podsekcje)

- Usuń wszystkie inne sekcje, w tym:
  - Wytyczne dla lekcji
  - Formy pracy na lekcji
  - Rekomendacje
  - Kamienie milowe (oznaczenia # i komentarze nauczyciela)
  - Przegląd skryptów z lekcji

- Dostosuj język do ucznia (10–12 lat): prosty, motywujący, serdeczny, jakby tłumaczył starszy kolega.
- Usuń wszystkie komentarze organizacyjne dla nauczyciela i notatki techniczne.
- Zmień spis treści na checklistę kroków w prostym języku.
- Użyj lekkiego formatowania Markdown (nagłówki, wypunktowania, pogrubienia) dla przejrzystości i lepszej czytelności.

Na końcu zwróć **wyłącznie gotowy, uporządkowany skrypt dla ucznia**, bez żadnych dodatkowych komentarzy ani opisów.

Konspekt lekcji poniżej:
{lesson_outline_raw}
"""
    print("Invoking LLM")
    response = llm.invoke(prompt)

    print(response.content)

if __name__ == '__main__':
    main()

    
