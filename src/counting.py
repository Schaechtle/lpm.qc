import polars as pl
from collections import Counter
import sys
import numpy as np


def _is_not_none_or_nan(value):
    if value is None:
        return False
    # Try checking if value is np.nan, catching TypeError for non-numeric values
    try:
        if np.isnan(value):
            return False
    except TypeError:
        pass
    # Value is neither None nor np.nan
    return True


def _is_not_none_or_nan_bivariate(values):
    return _is_not_none_or_nan(values[0]) and _is_not_none_or_nan(values[1])


def normalize_count(column):
    """
    Count occurences of categories. This works on Polars'columns
    i.e. Polars Series.

    Parameters:
    - column (List or Polars Series): A column in a dataframe.

    Returns:
    - dict: A Python dictionary, where keys are categories and values are the
      normalized ([0,1]) counts.


    Examples:
    >>> normalize_count(pl.Series("foo", ["a", "b", "a", "a"]))
        {"a": 0.75, "b" 0.25}
    >>> normalize_count(["a", "b", "a", "a"])
        {"a": 0.75, "b" 0.25}
    """
    column = list(filter(_is_not_none_or_nan, column))
    assert len(column) > 0
    return {k: v / len(column) for k, v in pl.Series(column).value_counts().rows()}


def normalize_count_bivariate(column_1, column_2):
    """
    Count occurences of events between two categorical columns.
    This works on Polars'columns i.e. Polars Series.

    Parameters:
    - column_1 (List or Polars Series):  A column in a dataframe.
    - column_2 (List or Polars Series):  Another column in a dataframe.

    Returns:
    - dict: A Python dictionary, where keys are typles of categories from the
      two columns and values are the normalized ([0,1]) counts.


    Examples:
    >>> normalize_count_bivariate(
            pl.Series("foo", ["a", "b", "a", "a"])
            pl.Series("foo", ["x", "y", "x", "y"]))

    {("a", "x",): 0.5, ("a", "y",): 0.25, ("b, "y",): 0.25}
    """
    assert len(column_1) == len(column_2)
    assert len(column_1) > 0
    assert len(column_2) > 0

    column_values = list(filter(_is_not_none_or_nan_bivariate, zip(column_1, column_2)))
    assert len(column_values) > 0, "no overlap"
    counter = Counter(column_values)
    # Note that Polars doesn't like to count tuples.
    return {k: v / len(column_values) for k, v in dict(counter).items()}


def harmonize_categorical_probabilities(ps_a, ps_b):
    """
    Harmonize two categorical distributions. Ensure they have the same set of
    keys.

    Parameters:
    - ps_a (dict): A dict encoding a categorical probability distribution.
    - ps_b (dict): A dict encoding a categorical probability distribution.

    Returns:
    - ps_a_harmonzied (dict): A dict encoding a categorical
                              probability distribution.
    - ps_b_harmonzied (dict): A dict encoding a categorical
                              probability distribution.


    Examples:
        >>> harmonize_categorical_probabilities({"a": 0.1, "b": 0.9}, {"a": 1.0})
            {"a": 0.1, "b": 0.9}, {"a": 1.0, "b" 0.0}
        >>> harmonize_categorical_probabilities({"a": 1.0}, {"a": 0.1, "b": 0.9})
            {"a": 1.0, "b" 0.0}, {"a": 0.1, "b": 0.9}
    """
    # Get the union of keys from both dictionaries
    assert (len(ps_a) > 0) or (len(ps_b) > 0)
    all_keys = set(ps_a) | set(ps_b)
    # Update both dictionaries to contain all keys, setting default values to None for missing keys
    return {key: ps_a.get(key, 0.0) for key in all_keys}, {
        key: ps_b.get(key, 0.0) for key in all_keys
    }


def _probabilities_safe_as_denominator(ps, constant=sys.float_info.min):
    """
    Ensure all values in a categorical are larger than 0. Some distance metrics,
    like SciPy's JS distance require this.

    The Constant should be chosen so small that it does not affect any results.
    Other state-of-the-art-libraries do similar things,
    .e.g. here: https://github.com/gregversteeg/NPEET/blob/master/npeet/entropy_estimators.py#L273

    Parameters:
    - ps (dict): A dict encoding a categorical probability distribution.
    - constant (float): constant to be added to zero values.

    Returns:
    - ps_larger_zero (dict): A dict encoding a categorical probability
      distribution. All values are larger than zero.


    Examples:
        >>> p_larger_zero({"a": 1.0, "b": 0.0}, constant=0.00000001)
            {"a": 1.0, "b" 0.00000001}
    """

    def _add_constant_if_zero(v):
        if v == 0.0:
            return v + constant
        return v

    return {k: _add_constant_if_zero(v) for k, v in ps.items()}


def contingency_table(column_a, column_b):
    """
    Compute the contigency table for two columns in a Polars dataframe.

    Parameters:
    - column_a (List or Polars Series):  A column in a dataframe.
    - column_b (List or Polars Series):  The same column from another dataframe.

    Returns:
    - contingency table (np.arrray): a 2-d Numpy array couting the contigencies.
    """
    # Sorting unique values here so it's testable. Otherwise, the set/filter
    # combinations causes for stochatic orderings.
    assert len(column_a) > 0
    assert len(column_b) > 0
    # Ensure columns are list:
    column_a = [v for v in column_a]
    column_b = [v for v in column_b]
    unique_values = sorted(
        set(
            list(filter(_is_not_none_or_nan, column_a))
            + list(filter(_is_not_none_or_nan, column_b))
        )
    )
    contingency_table = np.zeros((len(unique_values), 2))
    for i, value in enumerate(unique_values):
        contingency_table[i, 0] = column_a.count(value)
        contingency_table[i, 1] = column_b.count(value)
    return contingency_table
