#!/usr/bin/env python

import argparse
import polars as pl
import sys

from syn_data_fidelity.two_sample_testing import univariate_two_sample_testing_in_data


def main():
    description = "Run a univariate statistical test"
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("-a", "--data-1", type=str, help="Path to a CSV.")
    parser.add_argument("-b", "--data-2", type=str, help="Path to a CSV.")
    parser.add_argument(
        "-o",
        "--output",
        type=argparse.FileType("w+"),
        help="Result",
        default=sys.stdout,
    )

    args = parser.parse_args()

    df_a = pl.read_csv(args.data_1)
    df_b = pl.read_csv(args.data_2)

    result = univariate_two_sample_testing_in_data(df_a, df_b)
    result.write_csv(args.output)


if __name__ == "__main__":
    main()
