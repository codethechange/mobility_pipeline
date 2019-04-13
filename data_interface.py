"""Stores the constants and functions to interface with data files

This file is specific to the data files we are using and their format.
"""

import json
import numpy as np
import pandas as pd
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


def load_mobility() -> pd.DataFrame:
    df = pd.read_csv(MOBILITY_PATH)
    del df['DATE']
    df['ORIGIN'] = df['ORIGIN'].str[2:].astype(np.int)
    df['DESTINATION'] = df['DESTINATION'].str[2:].astype(np.int)
    return df
