import langchain
from langchain_openai import ChatOpenAI

def read_file(path: str) -> str:
    with open(path, 'r') as file:
        contents = file.read()

        return contents

def main() -> None:
    lesson_outline_extracted_path = "./data/konspekt_extracted.txt"
    lesson_outline_raw = read_file(lesson_outline_extracted_path)
    print("File read")

    llm = ChatOpenAI(
        model="gpt-4o-mini",
    )

    prompt = f"""
Jesteś korektorem i edytorem języka polskiego.  
Poniższy tekst został wczytany automatycznie z pliku PDF i jest nieuporządkowany.  
Twoim zadaniem jest uporządkowanie tekstu, aby był czytelny i spójny.  

- Połącz zdania w jedną linię.  
- Usuń niepotrzebne przerwy i złamania wierszy.  
- Dodaj formatowanie w stylu Markdown:  
  - Użyj `#` jako nagłówków (np. tytuły i główne sekcje).  
  - Użyj `-` do wypunktowań.  
  - Pogrub ważne słowa lub frazy, jeśli to pasuje.  
- Zachowaj logiczny i naturalny podział na akapity.  

Zwróć **wyłącznie** poprawiony tekst — nie dodawaj żadnych dodatkowych informacji ani komentarzy.  

   
Konspekt lekcji poniżej:
{lesson_outline_raw}
"""
    print("Invoking LLM")
    response = llm.invoke(prompt)

    print(response.content)

if __name__ == '__main__':
    main()

    