"""Stores the constants and functions to interface with data files

This file is specific to the data files we are using and their format.
"""

import json
from typing import List
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from shapely.geometry import MultiPolygon  # type: ignore
from mobility_pipeline.lib.voronoi import load_cell

# Thanks to abarnert at StackOverflow for how to document constants
# https://stackoverflow.com/a/20227174

DATA_PATH = "data/brazil-towers-voronoi-mobility/"
"""Path to folder containing towers, voronoi, and mobility data"""

TOWERS_PATH = "%stowers_br.csv" % DATA_PATH
"""Relative to :py:const:`DATA_PATH`, path to towers CSV file"""
VORONOI_PATH = "%sbrazil-voronoi.json" % DATA_PATH
"""Relative to :py:const:`DATA_PATH`, path to Voronoi JSON file"""
MOBILITY_PATH = "%smobility_matrix_20150201.csv" % DATA_PATH
"""Relative to :py:const:`DATA_PATH`, path to mobility CSV file"""


def load_cells() -> List[MultiPolygon]:
    """Loads the Voronoi cells from the file at :py:const:`VORONOI_PATH`.

    Returns:
        A list of :py:mod:`shapely.geometry.MultiPolygon` objects, each of which
        describes a cell. If the cell can be described as a single polygon, the
        returned MultiPolygon will contain only 1 polygon.
    """
    with open(VORONOI_PATH, 'r') as f:
        raw_json = json.loads(f.read())
    cells = [load_cell(feature['geometry']) for feature in raw_json['features']]
    return cells


def load_towers() -> np.ndarray:
    """Loads the tower positions from the file at :py:const:`TOWERS_PATH`.

    Returns:
        A matrix of tower coordinates with columns ``[longitude, latitude]`` and
        one tower per row. Row indices match the numeric portions of tower
        names.
    """
    towers_mat = np.genfromtxt(TOWERS_PATH, delimiter=',')
    towers_mat = towers_mat[1:, 1:]
    return towers_mat


def load_mobility() -> pd.DataFrame:
    """Loads mobility data from the file at :py:const:`MOBILITY_PATH`.

    Returns:
        A :py:class:`pandas.DataFrame` with columns ``ORIGIN``, ``DESTINATION``,
        and ``COUNT``. Columns ``ORIGIN`` and ``DESTINATION`` contain numeric
        portions of tower names, represented as :py:class:`numpy.int`. These
        numeric portions strictly increase in ``ORIGIN``-major order, but rows
        may be missing if they would have had a ``COUNT`` value of ``0``.
    """
    df = pd.read_csv(MOBILITY_PATH)
    del df['DATE']
    df['ORIGIN'] = df['ORIGIN'].str[2:].astype(np.int)
    df['DESTINATION'] = df['DESTINATION'].str[2:].astype(np.int)
    return df
