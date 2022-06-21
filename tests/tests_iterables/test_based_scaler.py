"""
tests for my_utilities.iterables.based_scaler
"""
import numpy as np

from my_utilities.iterables.based_scaler import based_scaler


def test_based_scaler() -> None:
    """
    test function based_scaler
    :return: nothing
    """
    np_1 = np.array([1, 2])
    np_2 = np.array([3, 4])
    np_3 = np.array([-1, 0])
    assert np.array_equal(based_scaler(np_1, np_2), np.array([2, 4]))
    assert np.array_equal(based_scaler(np_2, np_1), np.array([1.5, 2]))
    assert np.array_equal(based_scaler(np_1, np_1), np_1)
    assert np.array_equal(based_scaler(np_2, np_3), np.array([0, 0]))
    assert list(map(str, based_scaler(np_3, np_2).tolist())) == [
        str(-np.inf),
        str(np.nan),
    ]
