"""Stores the constants and functions to interface with data files

This file is specific to the data files we are using and their format.
"""

import json
from typing import List
import shapefile # type: ignore
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from shapely.geometry import MultiPolygon  # type: ignore
from lib.voronoi import load_cell

# Thanks to abarnert at StackOverflow for how to document constants
# https://stackoverflow.com/a/20227174

DATA_PATH = "../data/brazil-towers-voronoi-mobility/"
"""Path to folder containing towers, voronoi, and mobility data"""

TOWERS_PATH = "%stowers_br.csv" % DATA_PATH
"""Relative to :py:const:`DATA_PATH`, path to towers CSV file"""
VORONOI_PATH = "%sbrazil-voronoi.json" % DATA_PATH
"""Relative to :py:const:`DATA_PATH`, path to Voronoi JSON file"""
MOBILITY_PATH = "%smobility_matrix_20150201.csv" % DATA_PATH
"""Relative to :py:const:`DATA_PATH`, path to mobility CSV file"""
ADMIN_SHAPE_PATH = "%sgadm36_BRA_2" % DATA_PATH
"""Relative to py:const:`DATA_PATH`, path to administrative region shape files"""
ADMIN_PATH = "%sbr_admin2.json" % DATA_PATH
"""Relative to :py:const:`DATA_PATH`, path to country shapefile"""
TOWER_PREFIX = 'br'
"""The tower name is the tower index appended to this string"""


def load_polygons_from_json(filepath) -> List[MultiPolygon]:
    """Loads cells from given filepath to JSON.

    Returns:
        A list of :py:mod:`shapely.geometry.MultiPolygon` objects, each of which
        describes a cell. If the cell can be described as a single polygon, the
        returned MultiPolygon will contain only 1 polygon.
    """
    with open(filepath, 'r') as f:
        raw_json = json.loads(f.read())
    cells = [load_cell(feature['geometry']) for feature in raw_json['features']]
    return cells

def convert_shape_to_json() -> None:
    """Converts shapefile containing administrative regions to GeoJSON format
    """
    # read the shapefile
    reader = shapefile.Reader(ADMIN_SHAPE_PATH)
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    buffer = []
    for shape_record in reader.shapeRecords():
        atr = dict(zip(field_names, shape_record.record))
        geom = shape_record.shape.__geo_interface__
        buffer.append(dict(type="Feature", geometry=geom, properties=atr))
    # write the GeoJSON file
    geojson = open(ADMIN_PATH, "w")
    geojson.write(json.dumps({"type": "FeatureCollection", "features": buffer}, indent=2) + "\n")
    geojson.close()

def load_admin_cells() -> List[MultiPolygon]:
    """Loads the administrative region cells

    Data is loaded from :py:const:`ADMIN_PATH`. This is a wrapper function for
    :py:func:`load_polygons_from_json`.

    Returns:
        A list of the administrative region cells.
    """
    return load_polygons_from_json(ADMIN_PATH)


def load_voronoi_cells() -> List[MultiPolygon]:
    """Loads cells from the file at :py:const:`VORONOI_PATH`

    Returns:
        See :py:mod:`load_polygons_from_json`. Each returned object represents
        a Voronoi cell.
    """
    return load_polygons_from_json(VORONOI_PATH)


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
