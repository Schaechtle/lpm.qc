import pandas as pd
import sys

path = "/home/ulli/iql/lpm.qc/test-data"

df = pd.read_csv(f"{path}/synthetic/max-entropy.csv")
columns = pd.read_csv(f"{path}/real/ignored.csv").columns
df[columns].to_csv(sys.stdout, index=False)

