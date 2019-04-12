"""Stores the constants and functions to interface with data files

This file is specific to the data files we are using and their format.
"""

import json
import numpy as np
from typing import List
from shapely.geometry import MultiPolygon
from mobility_pipeline.voronoi import load_cell

DATA_PATH = "data/"

TOWERS_PATH = "%sbrazil-towers-voronoi-mobility/towers_br.csv" % DATA_PATH
VORONOI_PATH = "%sbrazil-towers-voronoi-mobility/brazil-voronoi.json" % DATA_PATH


def load_cells() -> List[MultiPolygon]:
    with open(VORONOI_PATH, 'r') as f:
        raw_json = json.loads(f.read())
    cells = [load_cell(feature['geometry']) for feature in raw_json['features']]
    return cells


def load_towers() -> np.ndarray:
    towers_mat = np.genfromtxt(TOWERS_PATH, delimiter=',')
    towers_mat = towers_mat[1:, 1:]
    return towers_mat
