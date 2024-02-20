import pandas as pd
import sys
import os

path = "/home/ulli/iql/lpm.qc/test-data"

df_o = pd.read_csv(f"{path}/real/ignored.csv")
df_o["collection"] =  "observed"
df_iql = pd.read_csv(f"{path}/synthetic/synthetic-data-iql.csv")
df_iql["collection"] =  "iql"
df_b = pd.read_csv(f"{path}/synthetic/max-entropy.csv")
df_b["collection"] =  "baseline"


out = pd.concat([
    df_o,
    df_iql,
    df_b,
    ])
out.to_csv(sys.stdout, index=False)
