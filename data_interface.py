"""Stores the constants and functions to interface with data files

This file is specific to the data files we are using and their format.
"""

import json
import re
import csv
import numpy as np
from typing import List
from shapely.geometry import MultiPolygon
from mobility_pipeline.voronoi import load_cell

DATA_PATH = "data/brazil-towers-voronoi-mobility/"

TOWERS_PATH = "%stowers_br.csv" % DATA_PATH
VORONOI_PATH = "%sbrazil-voronoi.json" % DATA_PATH
MOBILITY_PATH = "%smobility_matrix_20150201.csv" % DATA_PATH


def load_cells() -> List[MultiPolygon]:
    with open(VORONOI_PATH, 'r') as f:
        raw_json = json.loads(f.read())
    cells = [load_cell(feature['geometry']) for feature in raw_json['features']]
    return cells


def load_towers() -> np.ndarray:
    towers_mat = np.genfromtxt(TOWERS_PATH, delimiter=',')
    towers_mat = towers_mat[1:, 1:]
    return towers_mat


def load_mobility() -> np.ndarray:
    num_re = re.compile('[0-9]+')

    def get_int(x):
        return int(num_re.search(x).group(0))

    with open(MOBILITY_PATH, newline='') as f:
        mobility_csv = csv.reader(f)
        next(mobility_csv)  # Skip header line of CSV
        mobility_csv = [[get_int(ori), get_int(dst), count]
                        for date, ori, dst, count in mobility_csv]
    return np.array(mobility_csv)
