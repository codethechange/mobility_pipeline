#!/usr/bin/env python3

"""Checks that mobility coordinates are in origin-major strict increasing order

"""

import csv
from data_interface import MOBILITY_PATH
from lib.validate import validate_mobility


if __name__ == '__main__':
    # pragma pylint: disable=invalid-name
    with open(MOBILITY_PATH, newline='') as f:
        mobility_csv = list(csv.reader(f))[1:]
    out = validate_mobility(mobility_csv)
    if out:
        raise ValueError(out)
    print("Valid")
