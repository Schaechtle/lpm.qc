import polars as pl

def normalize_count(column):
    """
    Count occurences of categories. This works on Polars'columns
    i.e. Polars Series.

    Parameters:
    - column (Polars Series): A column in a dataframe.

    Returns:
    - dict: A Python dictionary, where keys are categories and values are the
      normalized ([0,1]) counts.


    Examples:
    >>> normalize_count(pl.Series("foo", ["a", "b", "a", "a"]))
        {"a": 0.75, "b" 0.25}
    """

def normalize_count_bivariate(column_1, column_2):
    """
    Count occurences of events between two categorical columns.
    This works on Polars'columns i.e. Polars Series.

    Parameters:
    - column_1 (Polars Series):  A column in a dataframe.
    - column_2 (Polars Series):  Another column in a dataframe.

    Returns:
    - dict: A Python dictionary, where keys are categories and values are the
      normalized ([0,1]) counts.


    Examples:
    >>> normalize_count_bivariate(
            pl.Series("foo", ["a", "b", "a", "a"])
            pl.Series("foo", ["x", "y", "x", "y"]))

    {"a-x": 0.5, "a-y" 0.25, "b-y" 0.25}
    """
    assert column_1.name != column_2.name


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

def p_larger_zero(ps, constant=10**(-10)):
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

def contingency_table(column_a, column_b):
    """
    Compute the contigency table for two columns in a Polars dataframe.

    Parameters:
    - column_a (Polars Series):  A column in a dataframe.
    - column_b (Polars Series):  The same column from another dataframe.

    Returns:
    - contingency table (np.arrray): a 2-d Numpy array couting the contigencies.
    """
