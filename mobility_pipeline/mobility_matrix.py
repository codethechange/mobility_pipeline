#!/usr/bin/env python3

"""Generates the admin-to-admin mobility matrix from data files

Currently only computes the tower-to-tower matrix.
"""

from lib.make_matrix import make_tower_tower_matrix
from data_interface import load_mobility, load_towers


if __name__ == '__main__':
    # pragma pylint: disable=invalid-name
    mobility_df = load_mobility()
    towers_mat = load_towers()

    tower_tower_mat = make_tower_tower_matrix(mobility_df, len(towers_mat))
