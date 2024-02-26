# lpm.qc

## Overview over fidelity component

![schematic](images/fidelity-schematic.png)

## Usage


```shell
python bin/dist.py --data-1 foo.csv --data-2 bar.csv
```

```shell
python bin/dist.py --data-1 foo.csv --data-2 bar.csv --bivariate
```

```shell
python bin/two_sample_testing.py --data-1 foo.csv --data-2 bar.csv 
```

## Test

Tests are automatically run through the flakes file. For development,
users can run
```shell
python -m pip install --upgrade --force-reinstall  . && pytest tests/ -vvv
```
This worflow depends on pip and pytest being available.
