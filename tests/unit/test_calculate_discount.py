import pytest
from src.utils.calculate_discount import calculate_discount


@pytest.mark.parametrize("price,discount,expected", [
    (100, 0.2, 80.0),
    (50, 0.0, 50.0),
    (200, 1.0, 0.0),
])
def test_calculate_discount_required_values(price, discount, expected):
    assert calculate_discount(price, discount) == expected


@pytest.mark.parametrize("discount", [-0.1, 1.5])
def test_calculate_discount_required_invalid_discount(discount):
    with pytest.raises(ValueError):
        calculate_discount(100, discount)


def test_calculate_discount_negative_price():
    import pytest
    with pytest.raises(ValueError):
        calculate_discount(-100, 0.2)


def test_calculate_discount_type_error():
    import pytest
    with pytest.raises(TypeError):
        calculate_discount("100", 0.2)  # type: ignore[arg-type]
