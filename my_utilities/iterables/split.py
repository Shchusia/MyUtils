"""
Module with functions for split iterable objects
"""
# pylint: disable=inconsistent-return-statements
from collections.abc import Generator
from typing import Any, List, Optional, Tuple, Type, Union


def _validate_type(iterable: Union[List[Any], Tuple[Any, ...]]) -> Optional[Type]:
    """
    Validate the type of variable iterable
    :param iterable: Iterable type to variable
    :type iterable: Union[List[Any], Tuple[Any, ...]]
    :return: if correct type variable `iterable` than return type
    :rtype: Optional[Type]
    :raise TypeError: if incorrect type `iterable`
    """
    if not isinstance(iterable, (list, tuple)):
        raise TypeError(
            f"Incorrect type variable `iterable`."
            f" Valid types are [list, tuple] and not {type(iterable)}"
        )
    return type(iterable)


def split(iterable: Union[List[Any], Tuple[Any, ...]], cnt: int) -> Generator:
    """
    Method for splitting into equal cnt parts generator
    :param iterable: object to split
    :type iterable: Union[List[Any], Tuple[Any, ...]]
    :param cnt: cnt partitions
    :type cnt: int
    :return: generator of split iterable object len generator equal cnt variable
    :rtype: Generator
    :raises TypeError: if incorrect type of `iterable` variable
    """
    _validate_type(iterable=iterable)
    k, j = divmod(len(iterable), cnt)  # type: int, int
    for i in range(cnt):
        yield iterable[i * k + min(i, j) : (i + 1) * k + min(i + 1, j)]


def split_as_iterable(
    iterable: Union[List[Any], Tuple[Any, ...]], cnt: int
) -> Union[List[List[Any]], Tuple[Tuple[Any]]]:
    """
    Method for splitting into equal parts
    :param iterable: object to split
    :type iterable: Union[List[Any], Tuple[Any, ...]]
    :param cnt: cnt partitions
    :type cnt: int
    :return: iterable object with partitions
    :rtype: Union[List[Any], Tuple[Any, ...]]
    :raises TypeError: if incorrect type of `iterable` variable
    """
    _current_type = _validate_type(iterable)  # type: Type
    return _current_type(split(iterable=iterable, cnt=cnt))
