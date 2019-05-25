#!/usr/bin/env python3

"""Generates the admin-to-admin mobility matrix from data files

The data is loaded using the functions in :py:mod:`data_interface`, and the
matrices are computed using the functions in :py:mod:`make_matrix`.
"""
import numpy as np  # type: ignore
from lib.make_matrix import make_tower_tower_matrix, \
    make_tower_to_admin_matrix, make_admin_to_tower_matrix, \
    make_admin_admin_matrix
from data_interface import load_mobility, load_towers, load_voronoi_cells, \
    load_admin_cells


if __name__ == '__main__':
    # pragma pylint: disable=invalid-name
    mobility_df = load_mobility()
    towers_mat = load_towers()
    tower_cells = load_voronoi_cells()
    admin_cells = load_admin_cells()

    tower_tower_mat = make_tower_tower_matrix(mobility_df, len(towers_mat))
    tower_admin_mat = make_tower_to_admin_matrix(tower_cells, admin_cells)
    admin_tower_mat = make_admin_to_tower_matrix(admin_cells, tower_cells)

    admin_admin_mat = make_admin_admin_matrix(tower_tower_mat, tower_admin_mat,
                                              admin_tower_mat)
    np.savetxt('admin_admin_mat.csv', admin_admin_mat, delimiter=',')
