import argparse
import polars as p
import sys
from scipy.stats import chi2_contingency

def chi_squared(column_a, column_b):
    """
    Compute the Chi^2 contigency table-based two samples test.
    First, create a sound contingency tables. Then compute the test.
    Finally, record any problems.

    Parameters:
    - column_a (Polars Series): A column in a dataframe.
    - column_b (Polars Series): The same in another a dataframe.

    Returns:
    - p (float):  A p-value assessing the null hypothesis that the columns record the same distribution.
    - chi2 (float): Chi^2 test statistic.
    - problem (boolean): Recording a problems with the test, e.g. when not
      enough data was recorded in one of the columns.


    Examples:
    >>> chi_squared(
            pl.Series("foo", ["a", "b", "a", "a",...]),
            pl.Series("foo", ["a", "b", "b", "a",...])
            )
        0.08, 42., false
    """
    assert column_a.name == coluumn_b.name


def main():
    description = "Run a univariate statistical test"
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
    args = parser.parse_args()

    df_training = pl.read_csv(args.training)
    df_compare =  pl.read_csv(args.compare)
    # ....
    pd.DataFrame(results).to_csv(args.output, index=False)

if __name__ == "__main__":
    main()
