"""
Test for module chunk
"""
# mypy: ignore-errors
from types import GeneratorType
from typing import List, Tuple, Union

import pytest

from my_utilities.iterables.chunk import chunks


class TestDict(dict):
    """test class"""

    pass


SIZE_CHUNK = 2
SIZE_ITERABLE_OBJECTS = 11
test_list_range = list(range(SIZE_ITERABLE_OBJECTS))  # type: list[int]
test_tuple_range = tuple(range(SIZE_ITERABLE_OBJECTS))  # type: tuple[int, ...]
test_set_range = set(range(SIZE_ITERABLE_OBJECTS))  # type: set[int]
test_dict_range = {i: i for i in range(SIZE_ITERABLE_OBJECTS)}  # type: dict[int, int]
test_dict_custom_range = TestDict(test_dict_range)  # type: dict[int, int]


def test_chunk() -> None:
    """
    test function for  my_utilities.iterables.chunk.chunks
    :return: nothing
    """

    def validate(val: Union[List, Tuple], size: int) -> None:
        """

        :param val:
        :return:
        """
        for i, chunk in enumerate(val):
            if i != len(val) - 1:
                assert len(chunk) == size
            else:
                assert len(chunk) <= size

    gen_chunk_list = chunks(test_list_range, SIZE_CHUNK)
    assert isinstance(gen_chunk_list, GeneratorType)
    gen_chunk_tuple = chunks(test_tuple_range, SIZE_CHUNK)
    assert isinstance(gen_chunk_tuple, GeneratorType)
    chunk_list = list(gen_chunk_list)
    chunk_tuple = list(gen_chunk_tuple)
    validate(chunk_list, SIZE_CHUNK)
    validate(chunk_tuple, SIZE_CHUNK)

    with pytest.raises(ValueError):
        list(chunks(test_list_range, 0))
    with pytest.raises(ValueError):
        list(chunks(test_list_range, -1))
    with pytest.raises(TypeError):
        list(chunks(test_list_range, 0.5))  # type: ignore

    gen_chunk_list = chunks(test_list_range, SIZE_ITERABLE_OBJECTS)
    assert isinstance(gen_chunk_list, GeneratorType)
    chunk_list = list(gen_chunk_list)
    assert len(chunk_list) == 1
    assert len(chunk_list[0]) == SIZE_ITERABLE_OBJECTS

    with pytest.raises(TypeError):
        list(chunks(test_set_range, SIZE_CHUNK))  # type: ignore
    with pytest.raises(TypeError):
        list(chunks(test_dict_range, SIZE_CHUNK))  # type: ignore
    with pytest.raises(TypeError):
        list(chunks(test_dict_custom_range, SIZE_CHUNK))  # type: ignore
