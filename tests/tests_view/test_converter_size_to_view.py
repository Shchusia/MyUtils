"""
Tests for module `my_utils.view.converter_size_to_view`
"""
# pylint: disable=too-few-public-methods
from typing import Dict, List, Optional, Tuple, Type, TypeVar, Union

import pytest
from pydantic import BaseModel

from my_utils.view.converter_size_to_pretty_view import size

_E = TypeVar("_E", bound=Type[BaseException])  # noqa


class FunctionSizeArgs(BaseModel):
    """
    Class for arguments size function
    """

    bytes_value: int
    system: str = "traditional"
    round_to: int = 2


class TestCase(BaseModel):
    """
    class for test case
    """

    args: FunctionSizeArgs
    result: str
    is_raises: bool = False
    is_equal: bool = True
    raises: Optional[Union[Tuple[_E], _E]] = None  # type: ignore

    class Config:
        """
        config model
        """

        arbitrary_types_allowed = True


CORRECT_VALUES = {
    "petabytes": [
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**5 * 3 + 1, system="traditional", round_to=2
            ),
            result="3P",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**5 * 3 + 1, system="alternative", round_to=2
            ),
            result="3PB",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**5 * 3 + 1, system="verbose", round_to=2
            ),
            result="3 petabytes",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**5 + 1, system="verbose", round_to=2
            ),
            result="1 petabyte",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**5 * 3 + 1, system="iec", round_to=2
            ),
            result="3Pi",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**5 * 3 + 1, system="si", round_to=2
            ),
            result="3.38P",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**5 * 3 + 1, system="si", round_to=2
            ),
            result="3P",
            is_equal=False,
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**5 * 3 + 1, system="sis", round_to=2
            ),
            result="3P",
            is_raises=True,
            raises=(ValueError,),
        ),
    ],
    "terabytes": [
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**4 * 3 + 1, system="traditional", round_to=2
            ),
            result="3T",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**4 * 3 + 1, system="alternative", round_to=2
            ),
            result="3TB",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**4 * 3 + 1, system="verbose", round_to=2
            ),
            result="3 terabytes",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**4 + 1, system="verbose", round_to=2
            ),
            result="1 terabyte",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**4 * 3 + 1, system="iec", round_to=2
            ),
            result="3Ti",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**4 * 3 + 1, system="si", round_to=2
            ),
            result="3.3T",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**4 * 3 + 1, system="si", round_to=1
            ),
            result="3.3T",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**4 * 3 + 1, system="si", round_to=2
            ),
            result="3T",
            is_equal=False,
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**4 * 3 + 1, system="sis", round_to=2
            ),
            result="3T",
            is_raises=True,
            raises=(ValueError,),
        ),
    ],
    "gigabytes": [
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**3 * 3 + 1, system="traditional", round_to=2
            ),
            result="3G",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**3 * 3 + 1, system="alternative", round_to=2
            ),
            result="3GB",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**3 * 3 + 1, system="verbose", round_to=2
            ),
            result="3 gigabytes",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**3 + 1, system="verbose", round_to=2
            ),
            result="1 gigabyte",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**3 * 3 + 1, system="iec", round_to=2
            ),
            result="3Gi",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**3 * 3 + 1, system="si", round_to=2
            ),
            result="3.22G",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**3 * 3 + 1, system="si", round_to=2
            ),
            result="3G",
            is_equal=False,
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**3 * 3 + 1, system="sis", round_to=2
            ),
            result="3G",
            is_raises=True,
            raises=(ValueError,),
        ),
    ],
    "megabytes": [
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**2 * 3 + 1, system="traditional", round_to=2
            ),
            result="3M",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**2 * 3 + 1, system="alternative", round_to=2
            ),
            result="3MB",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**2 * 3 + 1, system="verbose", round_to=2
            ),
            result="3 megabytes",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**2 + 1, system="verbose", round_to=2
            ),
            result="1 megabyte",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**2 * 3 + 1, system="iec", round_to=2
            ),
            result="3Mi",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**2 * 3 + 1, system="si", round_to=2
            ),
            result="3.15M",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**2 * 3 + 1, system="si", round_to=1
            ),
            result="3.1M",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**2 * 3 + 1, system="si", round_to=2
            ),
            result="3M",
            is_equal=False,
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**2 * 3 + 1, system="sis", round_to=2
            ),
            result="3M",
            is_raises=True,
            raises=(ValueError,),
        ),
    ],
    "kilobytes": [
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**1 * 3 + 1, system="traditional", round_to=2
            ),
            result="3K",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**1 * 3 + 1, system="alternative", round_to=2
            ),
            result="3KB",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**1 * 3 + 1, system="verbose", round_to=2
            ),
            result="3 kilobytes",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**1 + 1, system="verbose", round_to=2
            ),
            result="1 kilobyte",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**1 * 3 + 1, system="iec", round_to=2
            ),
            result="3Ki",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**1 * 3 + 1, system="si", round_to=2
            ),
            result="3.07K",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**1 * 3 + 1, system="si", round_to=1
            ),
            result="3.1K",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**1 * 3 + 1, system="si", round_to=2
            ),
            result="3K",
            is_equal=False,
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**1 * 3 + 1, system="sis", round_to=2
            ),
            result="3K",
            is_raises=True,
            raises=(ValueError,),
        ),
    ],
    "bytes": [
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**0 * 3 + 1, system="traditional", round_to=2
            ),
            result="4B",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**0 * 3 + 1, system="alternative", round_to=2
            ),
            result="4 bytes",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**0 + 1, system="alternative", round_to=2
            ),
            result="2 bytes",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**0 * 3 + 1, system="verbose", round_to=2
            ),
            result="4 bytes",
        ),
        TestCase(
            args=FunctionSizeArgs(bytes_value=1024**0, system="verbose", round_to=2),
            result="1 byte",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**0 * 3 + 1, system="iec", round_to=2
            ),
            result="4",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**0 * 3 + 1, system="si", round_to=2
            ),
            result="4B",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**0 * 3 + 1, system="si", round_to=1
            ),
            result="4B",
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**0 * 3 + 1, system="si", round_to=2
            ),
            result="3B",
            is_equal=False,
        ),
        TestCase(
            args=FunctionSizeArgs(
                bytes_value=1024**0 * 3 + 1, system="sis", round_to=2
            ),
            result="4B",
            is_raises=True,
            raises=(ValueError,),
        ),
    ],
}  # type: Dict[str, List[TestCase]]


def test_size() -> None:
    """
    test function for function my_utils.view.converter_size_to_view.size()
    :return: nothing
    """
    for val in CORRECT_VALUES.values():
        for test_case in val:
            if test_case.is_raises:
                with pytest.raises(test_case.raises):
                    size(**test_case.args.dict())
            else:
                if test_case.is_equal:
                    assert test_case.result == size(**test_case.args.dict())
                else:
                    assert test_case.result != size(**test_case.args.dict())
