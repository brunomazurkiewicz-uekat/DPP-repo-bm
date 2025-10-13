import pytest
from src.utils.is_prime import is_prime


@pytest.mark.parametrize("n,expected", [
    (2, True),
    (3, True),
    (4, False),
    (0, False),
    (1, False),
    (5, True),
    (97, True),
])
def test_is_prime_required_cases(n, expected):
    assert is_prime(n) == expected


def test_is_prime_type_error():
    with pytest.raises(TypeError):
        is_prime("7")  # type: ignore[arg-type]


def test_is_prime_composite_odd_hits_loop():
    assert is_prime(9) is False  # dzieli się przez 3
