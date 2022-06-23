"""
Module with tests for my_utilities.iterables.remove_outliers
"""
# pylint: disable=invalid-name
from copy import deepcopy
from random import randint

import pandas as pd
import pytest

from my_utilities.iterables.remove_outliers import remove_outliers

COUNT_ROWS = randint(5, 15)

MIN_VALUE_A = randint(5, 25)
MIN_VALUE_B = randint(5, 25)
VALUE_TO_REPLACE = -50


def test_remove_outliers():
    """
    test for function remove_outliers
    """
    index_outliers_a_column = randint(0, COUNT_ROWS - 1)
    index_outliers_b_column = randint(0, COUNT_ROWS - 1)
    print(index_outliers_a_column, index_outliers_b_column)
    data_a_column = list(range(MIN_VALUE_A, MIN_VALUE_A + COUNT_ROWS))
    data_b_column = list(range(MIN_VALUE_B, MIN_VALUE_B + COUNT_ROWS))
    data_a_column[index_outliers_a_column] = MIN_VALUE_A * 15
    data_b_column[index_outliers_b_column] = MIN_VALUE_B * 15
    df = pd.DataFrame({"A": data_a_column, "B": data_b_column})
    with pytest.raises(ValueError):
        remove_outliers(df, "C", VALUE_TO_REPLACE)
    with pytest.raises(ValueError):
        remove_outliers(df, None, VALUE_TO_REPLACE)
    with pytest.raises(ValueError):
        remove_outliers(df, "A", VALUE_TO_REPLACE, percent=-0.0001)
    with pytest.raises(ValueError):
        remove_outliers(df, "A", VALUE_TO_REPLACE, percent=-0.1)
    with pytest.raises(ValueError):
        remove_outliers(df, "A", VALUE_TO_REPLACE, percent=1.001)

    replaced_df = remove_outliers(deepcopy(df), "A", VALUE_TO_REPLACE)
    assert replaced_df["A"].tolist()[index_outliers_a_column] == VALUE_TO_REPLACE
    replaced_df = remove_outliers(deepcopy(df), "B", VALUE_TO_REPLACE)
    assert replaced_df["B"].tolist()[index_outliers_b_column] == VALUE_TO_REPLACE
