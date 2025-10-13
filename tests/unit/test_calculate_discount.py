import pytest
from src.utils.calculate_discount import calculate_discount

@pytest.mark.parametrize("price,discount,expected", [
    (100, 0.2, 80.0),  # typowy przypadek
    (50, 0.0, 50.0),  # brak zniżki
    (200, 1.0, 0.0),  # 100% zniżki
    (99.99, 0.15, 84.99),  # wynik zaokrąglony
])
def test_calculate_discount_values(price, discount, expected):
    assert calculate_discount(price, discount) == expected


@pytest.mark.parametrize("discount", [-0.1, 1.5, 2, -5])
def test_calculate_discount_invalid_discount(discount):
    with pytest.raises(ValueError):
        calculate_discount(100, discount)


def test_calculate_discount_negative_price():
    with pytest.raises(ValueError):
        calculate_discount(-100, 0.2)


@pytest.mark.parametrize("price,discount", [
    ("100", 0.2),
    (100, "0.2"),
    (None, 0.2),
])
def test_calculate_discount_type_error(price, discount):
    with pytest.raises(TypeError):
        calculate_discount(price, discount)
