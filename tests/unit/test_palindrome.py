from src.utils.palindrome import is_palindrome
import pytest


@pytest.mark.parametrize("word,expected", [
    ("kajak", True),
    ("Anna", True),
    ("oko", True),
    ("Python", False),
    ("A man a plan a canal Panama", True),
])
def test_is_palindrome(word, expected):
    assert is_palindrome(word) == expected
