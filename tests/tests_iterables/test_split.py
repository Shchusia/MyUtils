"""
Tests for module split
"""
from types import GeneratorType

import pytest

from my_utils.iterables.split import split, split_as_iterable

CNT_CHUNKS = 2
SIZE_ITERABLE_OBJECTS = 10
CNT_CHUNKS_MORE_SIZE_OBJECTS = SIZE_ITERABLE_OBJECTS + 1
test_list_range = list(range(SIZE_ITERABLE_OBJECTS))  # type: list[int]
test_tuple_range = tuple(range(SIZE_ITERABLE_OBJECTS))  # type: tuple[int, ...]
test_set_range = set(range(SIZE_ITERABLE_OBJECTS))  # type: set[int]
test_dict_range = {i: i for i in range(SIZE_ITERABLE_OBJECTS)}  # type: dict[int, int]


def test_split() -> None:
    """
    test method my_utils.iterables.split.split()
    :return: nothing
    """
    gen_split = split(test_list_range, CNT_CHUNKS)
    assert isinstance(gen_split, GeneratorType)
    with pytest.raises(TypeError):
        split(test_set_range, CNT_CHUNKS)  # type: ignore
    with pytest.raises(TypeError):
        split(test_dict_range, CNT_CHUNKS)  # type: ignore

    assert len(list(gen_split)) == CNT_CHUNKS


def test_split_as_iterable() -> None:
    """
    test method my_utils.iterables.split.split_as_iterable()
    :return: nothing
    """
    split_list = split_as_iterable(test_list_range, CNT_CHUNKS)
    split_tuple = split_as_iterable(test_tuple_range, CNT_CHUNKS)
    assert isinstance(split_list, type(test_list_range))
    assert len(split_list[0]) in (
        SIZE_ITERABLE_OBJECTS // 2,
        (SIZE_ITERABLE_OBJECTS // 2) + 1,
    )
    assert isinstance(split_tuple, type(test_tuple_range))
    with pytest.raises(TypeError):
        split_as_iterable(test_set_range, CNT_CHUNKS)
    with pytest.raises(TypeError):
        split_as_iterable(test_dict_range, CNT_CHUNKS)
    split_list = split_as_iterable(test_list_range, CNT_CHUNKS_MORE_SIZE_OBJECTS)
    assert len(split_list[-1]) == 0
