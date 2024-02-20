import pandas as pd
import sys
import os

path = "/home/ulli/iql/lpm.qc/results/distance-metrics"

df_held_out = pd.read_csv(f"{path}/held-out-data.csv").set_index("column")
df_iql = pd.read_csv(f"{path}/synthetic-data-iql.csv").set_index("column")

cols = df_iql.index.tolist()

def get_metric(df, metric):
    """Ensure that order aligns."""
    return [df[metric].loc[c] for c in cols]


out = pd.DataFrame({
    "iql": get_metric(df_iql, "tvd"),
    "held-out": get_metric(df_held_out, "tvd"),
    })
out.to_csv(sys.stdout, index=False)
