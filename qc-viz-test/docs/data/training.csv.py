import pandas as pd
import sys

path = "/home/ulli/iql/lpm.qc/test-data"

df = pd.read_csv(f"{path}/real/ignored.csv")
df.to_csv(sys.stdout, index=False)

