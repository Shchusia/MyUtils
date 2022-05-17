"""
Module with functions for generate chunks
"""
# pylint: disable=inconsistent-return-statements
from collections.abc import Generator
from typing import Any, List, Tuple, Union

from .split import _validate_type


def chunks(
    iterable: Union[List[Any], Tuple[Any, ...]], size_chunk: int, is_yield: bool = True
) -> Generator:
    """
    Method for splitting into many parts with len size_chunk generator
    :param iterable: object to split
    :type iterable: Union[List[Any], Tuple[Any, ...]]
    :param size_chunk: size_chunk
    :type size_chunk: int
    :param is_yield: use yield or not for build generator
    :type is_yield: bool
    :return: generator of split iterable object len generator equal cnt variable
    :rtype: Generator
    :raises TypeError: if incorrect type of `iterable` variable
    """
    _validate_type(iterable=iterable)
    if is_yield:
        for i in range(0, len(iterable), size_chunk):
            yield iterable[i : i + size_chunk]
    else:
        return (
            iterable[i : i + size_chunk] for i in range(0, len(iterable), size_chunk)
        )
