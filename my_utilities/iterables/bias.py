"""
Module with calculation bias
"""
from typing import Union

import numpy as np
import pandas as pd


def bias(
    vector_true: Union[pd.Series, np.array], vector_pred: Union[pd.Series, np.array]
) -> float:
    """
    Function for calculation bias.
    :param vector_true: vector with true labels of target variable
    :type vector_true: Union[pd.Series, np.array]
    :param vector_pred: vector with predicts labels of target variable
    :param vector_pred: Union[pd.Series, np.array]
    :return: metric value
    :rtype: float
    """
    if vector_pred.size != vector_true.size:
        raise ValueError(
            f"Operands must be the same length and not "
            f"[{vector_true.size},] [{vector_pred.size},]"
        )
    return np.abs(np.sum(vector_pred - vector_true) / np.sum(vector_true) * 100)
