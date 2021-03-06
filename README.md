# Temperature anomalies in Graz

## Michael Hadwiger - 11814638

This repository includes an installable python module for analyzing of temperature anomalies in Graz. The module was 
developed for an exercise within the course "411.045 Selected Topics in Climate Science 
(Python for climate and environmental scientists)" at the KFU Graz in the winter term 2021/22.

With the package the temperature anomalies for a specified month with respect to the mean values for a 
specified reference timeframe can be calculated and shown in a figure. 

The package provides a shell script `temp_anomalies-graz` with the following required arguments:
- `--start`: Starting year of the reference timeframe.
- `--end`: End year of the reference timeframe.
- `--month`: Month for which the mean values are calculated (1 to 12). If not specified or 0 the mean will be calculated over all months.
- `--comp`: wo integers for the start and end year of timeframe to compare to reference frame

Additional optional arguments:
- `--fig`: show data in figure
- `--trend`: calculate and show trend for timespan specified in `--comp`

For further information please see `temp_anomalies_graz --help`.

Until `v1.0` the calculation was done using only `numpy`. Since then, `pandas` is used. 

## Installation

Use the following command in the base directory to install:

```bash
python -m pip install .
```

For an editable ("developer mode") installation, use the following
instead:

```bash
python -m pip install -e .
```

With this, the installation is actually a link to the original source code,
i.e. each change in the source code is immediately available.

## Prerequisites

You need a working Python environment, and `pip` installed.

E.g., with `conda`:

```bash
conda create --name mynewenv python
conda activate mynewenv
python -m pip install -e .
```

## Requirements

- `numpy >= 1.18`
- `matplotlib`
- `pandas`