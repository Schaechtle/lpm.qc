#!/usr/bin/env python

#import edn_format
import scipy.stats as stats
import itertools
import pandas as pd
import numpy as np
import argparse
import json
import sppl.compilers.spe_to_dict as spe_to_dict
import sys

from scipy.spatial import distance
from sppl.transforms import Identity as I

# Small constant to keep calc sound.
CONSTANT = 0.1**10

def tvd(P, Q):
    return 0.5 * sum([np.abs(p-q) for p,q in zip(P,Q)])

def empirical_probability(training_col, test_col):
        emp_p_df_training = training_col.value_counts(normalize=True)
        emp_p_df_compare =  test_col.value_counts(normalize=True)
        p_compare = []
        for c in emp_p_df_training.index:
            if c in emp_p_df_compare.index:
                p_compare.append(emp_p_df_compare.loc[c])
            else:
                p_compare.append(CONSTANT)
        return emp_p_df_training.tolist(), p_compare


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

    # XXX: code for dealing with categoricals only
    #schema = edn_format.loads(args.schema.read(), write_ply_tables=False)
    #cols = [c for c,primitive_dist in schema.items() if primitive_dist =="categorical"]


    results = []
    for c in df_training.columns:
        p_training, p_compare = empirical_probability(df_training[c], df_compare[c])
        result = {
            "column":c,
            "tvd":tvd(p_training, p_compare),
            "js":distance.jensenshannon(p_training, p_compare),
        }
        results.append(result)
    pd.DataFrame(results).sort_values(by=["tvd"]).to_csv(args.output, index=False)

if __name__ == "__main__":
    main()
