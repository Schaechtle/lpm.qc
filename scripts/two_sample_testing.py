#!/usr/bin/env python

import argparse
import pandas as pd
import numpy as np
import sys
from scipy.stats import chi2_contingency

def only_strings(vector):
    return [v for v in vector if isinstance(v, str)]

def chi_squared(vector1_in, vector2_in):
    # Create a contingency table
    vector1 = only_strings(vector1_in)
    vector2 = only_strings(vector2_in)
    unique_strings = list(set(vector1 + vector2))
    contingency_table = np.zeros((len(unique_strings), 2))

    for i, string in enumerate(unique_strings):
        contingency_table[i, 0] = vector1.count(string)
        contingency_table[i, 1] = vector2.count(string)

    # Perform the chi-squared test
    chi2, p, dof, expected = chi2_contingency(contingency_table)
    # For now, only return p.
    return p, chi2


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

    df_training = pd.read_csv(args.training)
    df_compare =  pd.read_csv(args.compare)

    results = []
    num_tests = df_compare.shape[1]
    for c in df_training.columns:
        p, chi2 = chi_squared(df_training[c].tolist(), df_compare[c].tolist())
        result = {
            "column":c,
            "p":p,
            "test_statistic":chi2,
            "significant_after_correction": (p < (0.01/(num_tests*3)))
        }
        results.append(result)
    pd.DataFrame(results).to_csv(args.output, index=False)

if __name__ == "__main__":
    main()
