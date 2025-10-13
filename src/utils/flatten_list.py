def flatten_list(nested_list: list) -> list:
    if not isinstance(nested_list, list):
        raise TypeError("Argument musi być typu list")

    flattened = []

    for item in nested_list:
        if isinstance(item, list):
            flattened.extend(flatten_list(item))
        else:
            flattened.append(item)

    return flattened
