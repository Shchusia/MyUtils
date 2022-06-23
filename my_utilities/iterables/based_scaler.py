"""
module contains methods for bringing two values in the same scale
"""
import numpy as np


def based_scaler(x_to_scale: np.array, x_scaler: np.array) -> np.array:
    """
    Bringing two values in the same scale
    :param x_to_scale: original base values
    :type x_to_scale: np.array
    :param x_scaler: value to scale
    :type x_scaler: np.array
    :return: x_scaler values scaled according to x_to_scale
    :rtype: np.array
    """
    return x_to_scale * (1 - (x_to_scale.max() - x_scaler.max()) / x_to_scale.max())
