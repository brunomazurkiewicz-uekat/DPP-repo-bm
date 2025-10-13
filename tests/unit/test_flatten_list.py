import pytest
from src.utils.flatten_list import flatten_list


@pytest.mark.parametrize("nested,expected", [
    ([1, 2, 3], [1, 2, 3]),
    ([1, [2, 3], [4, [5]]], [1, 2, 3, 4, 5]),
    ([], []),
    ([[[1]]], [1]),
    ([1, [2, [3, [4]]]], [1, 2, 3, 4]),
])
def test_flatten_list_required_cases(nested, expected):
    assert flatten_list(nested) == expected
