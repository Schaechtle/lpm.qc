import argparse
import polars as pl
import numpy as np
import sys
# Import distances from SciPy
from scipy.special import kl_div as kl
from scipy.spatial.distance import jensenshannon as js

# Import helper functions for counting (local utils)
from counting import harmonize_categorical_probabilities
from counting import normalize_count
from counting import p_larger_zero

def tvd(P, Q):
    """
    Compute total variation distance between two probability vectors.

    Parameters:
    - P:  list of probabilities
    - Q:  list of probabilities

    Returns:
        total variation distance.

    Examples:
    >>> tvd([0.5, 0.5], [0.9, 0.1])
        0.4
    """
    assert len(P) == len(Q)

def univariate_distances(column_a, column_b, distance_metrics=[tvd, kl, js]):
    """
    Compute a set of distance metrics for a pair of columns

    Parameters:
    - column_a:  Polars Series
    - column_b:  Polars Series
    - distance_metrics: a list of functions implementing distance metrics.
                        These functions need to take two lists of floats.

    Returns:
        A dict with distance metrics and the columns names

    Examples:
    >>> univariate_distances(
            pl.Series("foo", ["a", "b", "a", "a"]),
            pl.Series("foo", ["a", "b", "b", "b"]),
            distance_metrics=[tvd]
            )
        {"column": "foo", "tvd": 0.5}
    """
    assert column_a.name == column_b.name

def univariate_distances_in_data(df_a, df_b, distance_metrics=[tvd, kl, js]):
    """
    Take two dataframes and compare a distance metrics
    for all categorical_columns.

    Parameters:
    - df_a:  Polars Dataframe
    - df_b:  Polars Dataframe
    - distance_metrics: a list of functions implementing distance metrics.
                        These functions need to take two lists of floats.

    Returns:
        A Polars Dataframe with a column "column" recording columns names
        and one column per distance metrics used.

    Examples:
    >>> univariate_distances_in_data(df_a, df_b)
        ┌────────┬─────┬─────┬─────┐
        │ column ┆ tvd ┆ kl  ┆ js  │
        │ ---    ┆ --- ┆ --- ┆ --- │
        │ str    ┆ f64 ┆ f64 ┆ f64 │
        ╞════════╪═════╪═════╪═════╡
        │ foo    ┆ 0.1 ┆ 0.1 ┆ 0.1 │
        │ bar    ┆ 0.2 ┆ 0.2 ┆ 0.2 │
        │ ...    ┆ ... ┆ ... ┆ ... │
        │ baz    ┆ 0.3 ┆ 0.3 ┆ 0.3 │
        └────────┴─────┴─────┴─────┘
       (Above is using examples values for distance metrics)
    """


def bivariate_distances(column_a_1, column_a_2, column_b_1, column_b_2, distance_metrics=[tvd, kl, js]):
    """
    Compute a set of distance metrics for a pair of columns

    Parameters:
    - column_a_1:  Polars Series
    - column_a_2:  Polars Series
    - column_b_1:  Polars Series
    - column_b_2:  Polars Series
    - distance_metrics: a list of functions implementing distance metrics.
                        These functions need to take two lists of floats.

    Returns:
        A dict with distance metrics and the both columns names

    Examples:
    >>> bivariate_distances(
            pl.Series("foo", ["a", "b", "a", "a"]),
            pl.Series("bar", ["x", "y", "y", "y"]),
            pl.Series("foo", ["a", "b", "a", "a"]),
            pl.Series("bar", ["x", "y", "y", "y"]),
            distance_metrics=[tvd]
            )
        {"column-1:": "foo", "column-2:": "bar", "tvd": 0.5}
    """
    assert column_a_1.name == column_b_1.name
    assert column_a_2.name == column_b_2.name


def bivariate_distances_in_data(df_a, df_b, distance_metrics=[tvd, kl, js]):
    """
    Take two dataframes, create all pairs categorical columns.  For each pair,
    compute a probability vector of all possible events for this pair.
    Compare a distance metrics for the probabilites of these events between
    the two dataframes.

    Parameters:
    - df_a:  Polars Dataframe
    - df_b:  Polars Dataframe
    - distance_metrics: a list of functions implementing distance metrics.
                        These functions need to take two lists of floats.


    Returns:
        A Polars Dataframe with two columns ("column-1", "column-2")
        recording columns names and one column per distance metrics used.

    Examples:
    >>> bivariate_distances_in_data(df_a, df_b)
        ┌──────────┬──────────┬─────┬─────┬─────┐
        │ column-1 ┆ column-2 ┆ tvd ┆ kl  ┆ js  │
        │ ---      ┆ ---      ┆ --- ┆ --- ┆ --- │
        │ str      ┆ str      ┆ f64 ┆ f64 ┆ f64 │
        ╞══════════╪══════════╪═════╪═════╪═════╡
        │ foo      ┆ bar      ┆ 1.0 ┆ 4.0 ┆ 7.0 │
        │ foo      ┆ baz      ┆ 2.0 ┆ 5.0 ┆ 8.0 │
        │ ...      ┆ ...      ┆ ... ┆ ... ┆ ... │
        │ bar      ┆ baz      ┆ 3.0 ┆ 6.0 ┆ 9.0 │
        └──────────┴──────────┴─────┴─────┴─────┘
       (Above is using examples values for distance metrics)
    """

def main():
    """ Main function for computing distances."""
    description = "For each column"
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        "--training", type=argparse.FileType("r"), help="Path to a CSV."
    )
    parser.add_argument(
        "--compare", type=argparse.FileType("r"), help="Path to a CSV."
    )
    parser.add_argument(
        "-o",
        "--output",
        type=argparse.FileType("w+"),
        help="Result",
        default=sys.stdout,
    )
    parser.add_argument(
        "--main-metric",
        type=str,
        help="Main metric to order result by",
        default="TVD", # Default order by total variation distance.
    )

    args = parser.parse_args()

    df_training = pl.read_csv(args.training)
    df_compare =  pl.read_csv(args.compare)

    # [...]
    csv_string = pl.DataFrame(results).sort(args.main_metric).to_csv()
    print(csv_string)

if __name__ == "__main__":
    main()
