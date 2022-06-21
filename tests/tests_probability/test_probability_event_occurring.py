"""
tests for module `my_utilities.probability.probability_event_occurring.py`
"""
from decimal import Decimal

import pytest

from my_utilities.probability.probability_event_occurring import is_fate_in_awe


def test_is_fate_in_awe() -> None:
    """
    Tests for function is_fate_in_awe
    :return: nothing
    """
    with pytest.raises(ValueError):
        is_fate_in_awe(-1)
    with pytest.raises(ValueError):
        is_fate_in_awe(-0.0001)
    with pytest.raises(ValueError):
        is_fate_in_awe(1.0001)
    with pytest.raises(ValueError):
        is_fate_in_awe(2.0001)
    with pytest.raises(ValueError):
        is_fate_in_awe(2)
    with pytest.raises(ValueError):
        is_fate_in_awe(Decimal(2))
    with pytest.raises(TypeError):

        class TestClass(ValueError):
            """test class"""

        is_fate_in_awe(TestClass(1.1))  # type: ignore
    with pytest.raises(TypeError):
        is_fate_in_awe("1.0001")  # type: ignore
    with pytest.raises(TypeError):
        is_fate_in_awe([1.0001])  # type: ignore

    percents = [0.1, 0.01, 0.001, 0.25, 0.35, 0.49, 0.5, 0.51, 0.8, 0.99, 1]
    count_iterations = 100000
    for percent in percents:
        error_for_percent = percent * 0.25
        cnt_true = 0
        for _ in range(count_iterations):
            if is_fate_in_awe(percent):
                cnt_true += 1
        percent_true = cnt_true / count_iterations
        assert (
            percent - error_for_percent <= percent_true <= percent + error_for_percent
        )
