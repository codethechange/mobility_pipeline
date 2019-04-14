#!/usr/bin/env python3

"""Checks that mobility data is listed in origin-major coordinate order

If this order were perfect, it would make forming the mobility matrix as easy
as reshaping the last column. Unfortunately, this script showed that some
coordinates are missing or out of order, so counts must be inserted manually.
"""

import csv
from typing import List
from data_interface import MOBILITY_PATH


def check_perfect(mobility: List[List[str]]) -> None:
    """Check whether the mobility data file is correctly ordered and full

    The mobility data file is loaded from the file at path
    :py:func:`mobility_pipeline.data_interface.MOBILITY_PATH`. Correctly ordered
    means that the tower names' numeric portions strictly increase in
    origin-major order. Full means that there is a row for every combination of
    origin and destination tower.

    Args:
        mobility: List of mobility CSV data by applying ``list(csv.reader(f))``

    Returns:
        None

    Raises:
        Exception: If an invalid ordering is found
    """
    n_towers = int(mobility_csv[-1][1][2:]) + 1
    i_row = 0

    for i_ori in range(n_towers):
        for i_dst in range(n_towers):
            _, ori, dst, _ = mobility[i_row]
            if ori != 'br{}'.format(i_ori) or dst != 'br{}'.format(i_dst):
                msg = 'INVALID: Row {} is {}, but we expected {}'.format(
                    i_row, mobility[i_row],
                    'date,br{},br{},count'.format(i_ori, i_dst)
                )
                raise Exception(msg)
            i_row += 1


# TODO: Check just that the ordering is strictly increasing, origin-major order


if __name__ == '__main__':
    # pragma pylint: disable=invalid-name
    with open(MOBILITY_PATH, newline='') as f:
        mobility_csv = list(csv.reader(f))[1:]
        check_perfect(mobility_csv)
