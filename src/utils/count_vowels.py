def count_vowels(text: str) -> int:
    if not isinstance(text, str):
        raise TypeError('Argument musi byc typu string')

    vowels = set("aeiouy")
    return sum(1 for ch in text.lower() if ch in vowels)
