import pytest
from src.utils.word_frequencies import word_frequencies


@pytest.mark.parametrize("text,expected", [
    ("To be or not to be", {"to": 2, "be": 2, "or": 1, "not": 1}),
    ("Hello, hello!", {"hello": 2}),
    ("", {}),
    ("Python Python python", {"python": 3}),
    ("Ala ma kota, a kot ma Ale.", {"ala": 1, "ma": 2, "kota": 1, "a": 1, "kot": 1, "ale": 1}),
])
def test_word_frequencies_basic_cases(text, expected):
    assert word_frequencies(text) == expected


def test_word_frequencies_ignores_case_and_punctuation():
    text = "Cześć, CZEŚĆ! cześć?"
    result = word_frequencies(text)
    assert result == {"cześć": 3}


def test_word_frequencies_type_error():
    with pytest.raises(TypeError):
        word_frequencies(12345)  # type: ignore[arg-type]
