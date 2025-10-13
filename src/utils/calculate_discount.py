def calculate_discount(price: float, discount: float) -> float:
    # Walidacja typów
    if not isinstance(price, (int, float)) or not isinstance(discount, (int, float)):
        raise TypeError("Argumenty muszą być typu int lub float")

    # Walidacja zakresu zniżki
    if not (0 <= discount <= 1):
        raise ValueError("Zniżka musi być w zakresie 0–1")

    # Walidacja ceny
    if price < 0:
        raise ValueError("Cena nie może być ujemna")

    return round(price * (1 - discount), 2)
