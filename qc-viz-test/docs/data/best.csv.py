import pandas as pd
import sys
import json

path = "/home/ulli/iql/lpm.qc/results/distance-metrics"

df_iql = pd.read_csv(f"{path}/synthetic-data-iql.csv").sort_values(by="tvd", ascending=True)
df_me = pd.read_csv(f"{path}/max-entropy.csv").sort_values(by="tvd", ascending=True)

result = {"iql":df_iql["column"].loc[0:3].tolist(), "me":df_me["column"].loc[0:3].tolist()}
pd.DataFrame(result).to_csv(sys.stdout, index=False)
