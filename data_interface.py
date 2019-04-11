"""Stores the constants and functions to interface with data files

This file is specific to the data files we are using and their format.
"""

import json
import numpy as np
from mobility_pipeline.voronoi import load_cell

DATA_PATH = "data/"

TOWERS_PATH = "%sbrazil-mobility/towers_br.csv" % DATA_PATH
VORONOI_PATH = "%sbrazil-mobility/voronoi_br.json" % DATA_PATH


def load_cells():
    with open(VORONOI_PATH, 'r') as f:
        raw_json = json.loads(f.read())
    cells = [load_cell(feature['geometry']) for feature in raw_json['features']]
    return cells


def load_towers():
    towers_mat = np.genfromtxt(TOWERS_PATH, delimiter=',')
    towers_mat = towers_mat[1:, 1:]
    return towers_mat
