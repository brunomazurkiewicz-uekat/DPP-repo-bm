import pytest
from src.utils.count_vowels import count_vowels

@pytest.mark.parametrize("text,expected", [
    ("", 0),  # pusty ciąg
    ("a", 1),  # jedna samogłoska
    ("bcdfg", 0),  # bez samogłosek
    ("Python", 2),  # 'o'
    ("AEIOUY", 6),  # wielkie litery
    ("Kobyła ma mały bok", 7),  # 'o y a a a y o'
    ("Żółw", 0)  # 'ó' nie liczymy (nie w zestawie)
])
def test_count_vowels_values(text, expected):
    assert count_vowels(text) == expected


def test_count_vowels_ignores_case():
    assert count_vowels("AaEeIiOoUuYy") == 12


def test_count_vowels_non_string_type_error():
    with pytest.raises(TypeError):
        count_vowels(123)  # type: ignore[arg-type]
