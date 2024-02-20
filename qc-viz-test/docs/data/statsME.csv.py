import pandas as pd
import sys
import os

path = "/home/ulli/iql/lpm.qc/results/two-sample-testing/max-entropy.csv"

df = pd.read_csv(path)

df = df[df.significant_after_correction & (~df.problem_with_test)]
df.to_csv(sys.stdout, index=False)
