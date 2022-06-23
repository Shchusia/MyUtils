"""
module with function(s) for replace/remove outliers
"""
# pylint: disable=invalid-name

from typing import Any

import pandas as pd


def remove_outliers(
    df: pd.DataFrame,
    field_name: str,
    replace_value: Any,
    quantile_percent: float = 0.25,
    multiplier: float = 1.5,
) -> pd.DataFrame:
    """
    Replace outliers (indicated following interquartile range methodology).
    Use this function for time series data where you cannot drop outliers.
    Attention!!!
    quantile_percent and multiplier variables are specified by default
     according to the formula. By changing them, you take full responsibility
      for yourself.
    :param pd.DataFrame df: data frame to remove outliers from
    :param str field_name: name field df to remove outlier
    :param float quantile_percent:
    :param Any replace_value:
    :param float multiplier:
    :return: changed df
    :rtype: pd.DataFrame
    :raise ValueError: if field_name not exists in columns df or incorrect percentage
    """
    if field_name not in df.columns:
        raise ValueError
    if not 0 <= quantile_percent <= 1:
        raise ValueError
    # Computing IQR
    q1 = df[field_name].quantile(quantile_percent)
    q3 = df[field_name].quantile(1 - quantile_percent)
    iqr = q3 - q1

    df.loc[
        (df[field_name] <= q1 - multiplier * iqr)
        | (df[field_name] >= q3 + multiplier * iqr),
        field_name,
    ] = replace_value
    return df
