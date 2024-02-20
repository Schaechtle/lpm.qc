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

```shell
python -m pip install --upgrade --force-reinstall  . && pytest tests/ -vvv
```
