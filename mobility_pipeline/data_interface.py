"""Stores the constants and functions to interface with data files

This file is specific to the data files we are using and their format.
"""

from os import path
import json
from typing import List
import shapefile # type: ignore
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from shapely.geometry import MultiPolygon  # type: ignore
from lib.voronoi import load_cell

# Thanks to abarnert at StackOverflow for how to document constants
# https://stackoverflow.com/a/20227174

DATA_PATH = "data/brazil-towers-voronoi-mobility/"
"""Path to folder containing towers, voronoi, and mobility data"""

TOWERS_PATH = f"{DATA_PATH}towers_br.csv"
"""Relative to :py:const:`DATA_PATH`, path to towers CSV file"""
VORONOI_PATH = f"{DATA_PATH}brazil-voronoi.json"
"""Relative to :py:const:`DATA_PATH`, path to Voronoi JSON file"""
MOBILITY_PATH = f"{DATA_PATH}mobility_matrix_20150201.csv"
"""Relative to :py:const:`DATA_PATH`, path to mobility CSV file"""
ADMIN_SHAPE_PATH = f"{DATA_PATH}gadm36_BRA_2"
"""Relative to py:const:`DATA_PATH`, path to administrative region shape file"""
ADMIN_PATH = f"{DATA_PATH}%s-shape.json"
"""Relative to :py:const:`DATA_PATH`, path to country shapefile"""
TOWER_PREFIX = 'br'
"""The tower name is the tower index appended to this string"""

TOWER_ADMIN_TEMPLATE = f"{DATA_PATH}/%s-tower-to-admin.csv"
"""Template that uses country identifier to make path to tower_admin matrix"""
ADMIN_TOWER_TEMPLATE = f"{DATA_PATH}/%s-admin-to-tower.csv"
"""Template that uses country identifier to make path to admin_tower matrix"""
ADMIN_ADMIN_TEMPLATE = f"{DATA_PATH}/%s-%s-admin-to-admin.csv"
"""Path to admin-to-admin matrix, accepts substitutions of country_id, day_id"""
ADMIN_GEOJSON_TEMPLATE = f"{DATA_PATH}/%s-shape.json"
"""Path to admin GeoJSON file, accepts substitution of country_id"""


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


def convert_shape_to_json(shapefile_path_prefix: str, country_id: str) -> None:
    """Converts shapefile containing administrative regions to GeoJSON format

    The GeoJSON file is saved at ADMIN_GEOJSON_TEMPLATE % country_id

    Arguments:
        shapefile_path_prefix: Path to the .shp or .dbf shapefile, optionally
            without the file extension. Both the .shp and .dbf files must be
            present in the same directory and with the same name (except file
            extension).
        country_id: Unique identifier for the country and admin level.

    Returns:
        None
    """
    # read the shapefile
    base, extension = path.splitext(shapefile_path_prefix)
    if extension.lower() in [".shp", ".dbf"]:
        shapefile_path_prefix = base
    reader = shapefile.Reader(shapefile_path_prefix)
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    buffer = []
    for shape_record in reader.shapeRecords():
        atr = dict(zip(field_names, shape_record.record))
        geom = shape_record.shape.__geo_interface__
        buffer.append(dict(type="Feature", geometry=geom, properties=atr))
    # write the GeoJSON file
    geojson = open(ADMIN_GEOJSON_TEMPLATE % country_id, "w")
    geojson.write(json.dumps({"type": "FeatureCollection", "features": buffer},
                             indent=2) + "\n")
    geojson.close()


def load_admin_cells(identifier: str) -> List[MultiPolygon]:
    """Loads the administrative region cells

    Data is loaded from :py:const:`ADMIN_PATH` ``% identifier``. This is a
    wrapper function for :py:func:`load_polygons_from_json`.

    Returns:
        A list of the administrative region cells.
    """
    return load_polygons_from_json(ADMIN_PATH % identifier)


def load_voronoi_cells(voronoi_path: str) -> List[MultiPolygon]:
    """Loads cells

    Arguments:
        voronoi_path: Path to file to load cells from

    Returns:
        See :py:mod:`load_polygons_from_json`. Each returned object represents
        a Voronoi cell.
    """
    return load_polygons_from_json(voronoi_path)


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


def load_mobility(mobility_path: str) -> pd.DataFrame:
    """Loads mobility data from the file at ``mobility_path``.

    Returns:
        A :py:class:`pandas.DataFrame` with columns ``ORIGIN``, ``DESTINATION``,
        and ``COUNT``. Columns ``ORIGIN`` and ``DESTINATION`` contain numeric
        portions of tower names, represented as :py:class:`numpy.int`. These
        numeric portions strictly increase in ``ORIGIN``-major order, but rows
        may be missing if they would have had a ``COUNT`` value of ``0``.
    """
    df = pd.read_csv(mobility_path)
    del df['DATE']
    df['ORIGIN'] = df['ORIGIN'].str[2:].astype(np.int)
    df['DESTINATION'] = df['DESTINATION'].str[2:].astype(np.int)
    return df


def load_tower_admin(country_id: str) -> np.ndarray:
    """Load tower-to-admin matrix

    Data loaded from :py:const:`TOWER_ADMIN_TEMPLATE` ``% country_id``.

    Args:
        country_id: Country identifier

    Returns:
        The tower-to-admin matrix
    """
    file_path = TOWER_ADMIN_TEMPLATE % country_id
    return deserialize_mat(file_path)


def load_admin_tower(country_id: str) -> np.ndarray:
    """Load admin-to-tower matrix

    Data loaded from :py:const:`ADMIN_TOWER_TEMPLATE` ``% country_id``.

    Args:
        country_id: Country identifier

    Returns:
        The admin-to-tower matrix
    """
    mat_path = ADMIN_TOWER_TEMPLATE % country_id
    return deserialize_mat(mat_path)


def save_admin_admin(country_id: str, day_id: str,
                     admin_admin: np.ndarray) -> str:
    """Save admin-to-admin matrix

    Saved to :py:const:`ADMIN_ADMIN_TEMPLATE` ``% (country_id, day_id)``.

    Args:
        country_id: Country identifier
        day_id: Day identifier
        admin_admin: Admin-to-admin matrix to save

    Returns:
        Path at which matrix was saved
    """
    file_path = ADMIN_ADMIN_TEMPLATE % (country_id, day_id)
    serialize_mat(admin_admin, file_path)
    return file_path


def save_tower_admin(country_id: str, mat: np.ndarray) -> None:
    """Save tower-to-admin matrix

    Saved to :py:const:`TOWER_ADMIN_TEMPLATE` ``% country_id``.

    Args:
        country_id: Country identifier
        mat: Matrix to save

    Returns:
        None
    """
    file_path = TOWER_ADMIN_TEMPLATE % country_id
    serialize_mat(mat, file_path)


def save_admin_tower(country_id: str, mat: np.ndarray) -> None:
    """Save admin-to-tower matrix

    Saved to :py:const:`ADMIN_TOWER_TEMPLATE` ``% country_id``.

    Args:
        country_id: Country identifier
        mat: Matrix to save

    Returns:
        None
    """
    file_path = ADMIN_TOWER_TEMPLATE % country_id
    serialize_mat(mat, file_path)


def serialize_mat(mat: np.ndarray, mat_path: str) -> None:
    """Save a matrix to a file

    Matrix is saved such that it can be recovered by :py:func:`deserialize_mat`.

    Args:
        mat: Matrix to save
        mat_path: File to save matrix to

    Returns:
        None
    """
    np.savetxt(mat_path, mat, delimiter=',')


def deserialize_mat(mat_path: str) -> np.ndarray:
    """Deserialize a matrix from a file

    File must have been created by :py:func:`serialize_mat`.

    Args:
        mat_path: Path of matrix file

    Returns:
        Deserialized matrix
    """
    return np.genfromtxt(mat_path, delimiter=',')
