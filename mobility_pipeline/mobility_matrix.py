#!/usr/bin/env python3

"""Generates the admin-to-admin mobility matrix from data files

Currently only computes the tower-to-tower matrix.
"""
from matplotlib import pyplot as plt  # type: ignore
from lib.make_matrix import make_tower_tower_matrix, generate_rtree, make_a_to_b_matrix
from data_interface import load_mobility, load_towers, load_polygons_from_json
from shapely.geometry import MultiPolygon  # type: ignore
from descartes import PolygonPatch  # type: ignore
from random import uniform as rand

DATA_PATH = "data/"
ADMIN_PATH = "%sbr_admin2.json" % DATA_PATH
TOWER_PATH = "%sbrazil-towers-voronoi-mobility/brazil-voronoi.json" % DATA_PATH





if __name__ == '__main__':
    # pragma pylint: disable=invalid-name
    # mobility_df = load_mobility()
    # towers_mat = load_towers()

    # tower_tower_mat = make_tower_tower_matrix(mobility_df, len(towers_mat))

    # test_overlap()



