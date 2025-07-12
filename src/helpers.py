from dataclasses import dataclass
import yaml
from pathlib import Path

"""
Moduł pomocniczy (helpers) zawierający funkcje do wczytywania danych potrzebnych asystentowi.

Obsługa błędów została uproszczona (praktycznie nie istnieje), ponieważ ten projekt ma charakter Proof of Concept.
"""


DATA_DIR = Path("./data")
LESSON_FILE = DATA_DIR / "virtual-assistant-script-1.md"
EXAMPLE_USERS_FILE = Path('./example_users.yaml')
STEP_IMAGES_DIR = DATA_DIR / "step-images"

@dataclass
class User:
    name: str
    gender: str

def get_lesson_outline() -> str:
    """
    Zwraca treść pliku z konspektem lekcji.
    """
    with open(LESSON_FILE, 'r') as f:
        contents = f.read()
        return contents
    
def get_user(name: str) -> User:
    """
    Zwraca obiekt User na podstawie pliku YAML z przykładowymi użytkownikami.

    Args:
        name (str): Klucz użytkownika do odczytania.

    Returns:
        User: Obiekt dataclass z informacjami o użytkowniku.
    """
    users = {}

    with open(EXAMPLE_USERS_FILE, 'r') as f:
        data = yaml.safe_load(f)
        for key, value in data.items():
            user = User(**value)
            users[key] = user
        return users[name]
    
def get_step_image_path(solution_step_identifier: str) -> str:
    """
    Zwraca ścieżkę do obrazu odpowiadającego podanemu identyfikatorowi kroku.

    Args:
        solution_step_identifier (str): Identyfikator kroku rozwiązania (np. '1a').

    Returns:
        str: Ścieżka do pliku obrazu.

    Obsługa błędów została uproszczona (nie istnieje), ponieważ jest to wersja POC.
    """
     
    image_path = STEP_IMAGES_DIR / f"{solution_step_identifier}.png"
    return str(image_path)