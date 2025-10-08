def is_palindrome(text: str) -> bool:
    if not isinstance(text, str):
        raise TypeError("Argument musi być typu str")
    cleaned = ''.join(ch.lower() for ch in text if ch.isalnum())
    return cleaned == cleaned[::-1]
