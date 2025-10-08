import pytest
from src.utils.palindrome import is_palindrome


@pytest.mark.parametrize("text,expected", [
    ("kajak", True),
    ("Kobyła ma mały bok", True),
    ("python", False),
    ("", True),
    ("A", True),
])
def test_is_palindrome(text, expected):
    assert is_palindrome(text) == expected


def test_is_palindrome_type_error_on_non_str():
    for bad in (None, 123, 12.3, True, b"kajak", ["k", "a"]):
        with pytest.raises(TypeError):
            is_palindrome(bad)  # type: ignore[arg-type]
