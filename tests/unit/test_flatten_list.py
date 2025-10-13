import pytest
from src.utils.flatten_list import flatten_list


@pytest.mark.parametrize("nested,expected", [
    ([1, 2, 3], [1, 2, 3]),  # brak zagnieżdżeń
    ([1, [2, 3], [4, [5]]], [1, 2, 3, 4, 5]),  # wielopoziomowo
    ([], []),  # pusta lista
    ([[[1], 2], 3], [1, 2, 3]),  # głębsze zagnieżdżenie
    ([["a", ["b", ["c"]]]], ["a", "b", "c"]),  # stringi
])
def test_flatten_list_values(nested, expected):
    assert flatten_list(nested) == expected


def test_flatten_list_type_error():
    with pytest.raises(TypeError):
        flatten_list("not a list")  # type: ignore[arg-type]


def test_flatten_list_mixed_types():
    data = [1, ["a", [True, [None]]]]
    result = flatten_list(data)
    assert result == [1, "a", True, None]
