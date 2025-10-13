import re
from collections import Counter

def word_frequencies(text: str) -> dict[str, int]:
    if not isinstance(text, str):
        raise TypeError("Argument musi być typu str")

    # Zamień na małe litery i wyciągnij słowa (bez interpunkcji)
    words = re.findall(r"[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+", text.lower())

    # Counter automatycznie policzy wystąpienia
    return dict(Counter(words))
