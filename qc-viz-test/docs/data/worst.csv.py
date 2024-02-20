import pandas as pd
import sys
import json

path = "/home/ulli/iql/lpm.qc/results/distance-metrics"

df_iql = pd.read_csv(f"{path}/synthetic-data-iql.csv").sort_values(by="tvd", ascending=True)
df_me = pd.read_csv(f"{path}/max-entropy.csv").sort_values(by="tvd", ascending=True)

result = {"iql":df_iql["column"].tolist()[-3:], "me":df_me["column"].tolist()[-3:]}
pd.DataFrame(result).to_csv(sys.stdout, index=False)
