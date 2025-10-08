def fibonacci(n: int) -> int:
    if not isinstance(n, int):
        raise TypeError("Argument musi być typu int")
    if n < 0:
        raise ValueError("Argument nie może być ujemny")
    if n in (0, 1):
        return n

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
