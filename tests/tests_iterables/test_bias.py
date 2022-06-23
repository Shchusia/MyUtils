"""
Module with tests for my_utilities.iterables.bias
"""
import numpy as np
import pytest

from my_utilities.iterables.bias import bias


def test_bias():
    """
    test for function bias
    """
    vector_1 = np.array(list(range(0, 10)))
    vector_2 = np.array(list(range(10, 20)))
    vector_3 = np.array(list(range(25, 40)))
    with pytest.raises(ValueError):
        bias(vector_1, vector_3)
    assert 222.221 <= bias(vector_1, vector_2) <= 222.223
    assert 68.96 <= bias(vector_2, vector_1) <= 69
    assert bias(vector_1, vector_1) == 0.0
