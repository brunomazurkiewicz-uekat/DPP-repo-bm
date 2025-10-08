import pytest
from src.utils.fibonacci import fibonacci


@pytest.mark.parametrize("n,expected", [
    (0, 0),
    (1, 1),
    (5, 5),
    (10, 55),
])
def test_fibonacci_values(n, expected):
    assert fibonacci(n) == expected


def test_fibonacci_negative():
    with pytest.raises(ValueError):
        fibonacci(-1)


def test_fibonacci_type_error():
    with pytest.raises(TypeError):
        fibonacci("tekst")  # nieprawidłowy typ
