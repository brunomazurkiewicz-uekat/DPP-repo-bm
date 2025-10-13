import pytest
from src.utils.count_vowels import count_vowels


@pytest.mark.parametrize("text,expected", [
    ("Python", 2),
    ("AEIOUY", 6),
    ("bcd", 0),
    ("", 0),
    ("Próba żółwia", 3),
])
def test_count_vowels_required_cases(text, expected):
    assert count_vowels(text) == expected


def test_count_vowels_ignores_case():
    assert count_vowels("AaEeIiOoUuYy") == 12


def test_count_vowels_non_string_type_error():
    with pytest.raises(TypeError):
        count_vowels(123)  # type: ignore[arg-type]
