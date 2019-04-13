#!/usr/bin/env python3

"""Checks that mobility data is listed in origin-major coordinate order

If this order were perfect, it would make forming the mobility matrix as easy
as reshaping the last column. Unfortunately, this script showed that some
coordinates are missing or out of order, so counts must be inserted manually.
"""

import csv
from data_interface import MOBILITY_PATH

if __name__ == '__main__':

    with open(MOBILITY_PATH, newline='') as f:
        mobility_csv = list(csv.reader(f))[1:]

        n_towers = int(mobility_csv[-1][1][2:]) + 1
        i_row = 0

        for i_ori in range(n_towers):
            for i_dst in range(n_towers):
                date, ori, dst, count = mobility_csv[i_row]
                if ori != 'br{}'.format(i_ori) or dst != 'br{}'.format(i_dst):
                    msg = 'INVALID: Row {} is {}, but we expected {}'.format(
                        i_row, mobility_csv[i_row],
                        'date,br{},br{},count'.format(i_ori, i_dst)
                    )
                    raise Exception(msg)
                i_row += 1
