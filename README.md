# lpm.qc

## Overview over fidelity component

![schematic](images/fidelity-schematic.png)

## Usage

### Fidelity CLI

:warning: this currently only works with categorical CSV files.

```shell
assess-distance --data-1 foo.csv --data-2 bar.csv
```

```shell
assess-distance --data-1 foo.csv --data-2 bar.csv --bivariate
```

```shell
assess-statistics --data-1 foo.csv --data-2 bar.csv 
```

### Using fidelity as a Python library

```python
# Get dependencies.
import polars as pl

from syn_data_fidelity.distances import bivariate_distances_in_data
from syn_data_fidelity.distances import univariate_distances_in_data
from syn_data_fidelity.two_sample_testing import univariate_two_sample_testing_in_data

# Read in two csv files.
df_foo = pl.read_csv("foo.csv")
df_bar = pl.read_csv("bar.csv")

# Compute univariate distance.
df_univariate_distance = univariate_distances_in_data(df_foo, df_bar, distance_metric="tvd")

# Compute bivariate distance.
df_bivariate_distance = bivariate_distances_in_data(df_foo, df_bar, distance_metric="tvd")

# Compute univariate two-sample hypothesis tests (currently only Chi^2).
df_univariate_two_sample_test = univariate_two_sample_testing_in_data(df_foo, df_bar)
```

## Test

Tests are automatically run through the flakes file. For development,
users can run
```shell
python -m pip install --upgrade --force-reinstall  . && pytest tests/ -vvv
```
This worflow depends on pip and pytest being available.
