"""Functions for validating data file formats and contents

"""

from typing import List, Optional, cast, Union, Iterator
from shapely.geometry import MultiPolygon, Polygon, Point  # type: ignore
from shapely.ops import unary_union  # type: ignore
import numpy as np  # type: ignore
from data_interface import TOWER_PREFIX, load_admin_cells, load_voronoi_cells


AREA_THRESHOLD = 0.0001
"""Allowable deviance, as a fraction of the area of the union,
between the area of the union of polygons and the sum of
the polygons' individual areas. Agreement between these values indicates the
polygons are disjoint and contiguous. Threshold was chosen based on the
deviances in known good Voronoi tessellations."""


def all_numeric(string: str) -> bool:
    """Check that a string is composed entirely of digits

    Args:
        string: String to check

    Returns:
        True if and only if the string is composed entirely of digits
    """
    for c in string:
        if not c.isdigit():
            return False
    return True


def validate_mobility(raw: List[List[str]]) -> Optional[str]:
    # pylint: disable=too-many-return-statements
    """Checks that the text from a CSV file is in a valid format for mobility

    The text must consist of a list of rows, where each row is a list of exactly
    4 strings: a date (not checked), an origin tower, a destination tower, and
    a count.

    The origin and destination must be composed of digits following
    :py:const:`data_interface.TOWER_PREFIX`. The count must be composed entirely
    of digits and represent a non-negative integer.

    The origin and destination tower numeric portions must strictly increase in
    origin-major order.

    Args:
        raw: List of mobility CSV data by applying ``list(csv.reader(f))``

    Returns:
        None if the input is valid, a string describing the error otherwise.
    """
    prev_ori = -1
    prev_dst = -1
    for line in raw:
        _, ori_str, dst_str, count_str = line
        ori_str = ori_str[len(TOWER_PREFIX):]
        dst_str = dst_str[len(TOWER_PREFIX):]
        if not all_numeric(ori_str):
            return "Line {} invalid because origin {} non-numeric".\
                format(line, ori_str)
        if not all_numeric(dst_str):
            return "Line {} invalid because destination {} non-numeric".\
                format(line, ori_str)
        if not all_numeric(count_str):
            return "Line {} invalid because count {} non-numeric".\
                format(line, count_str)
        ori = int(ori_str)
        dst = int(dst_str)
        count = int(count_str)
        if ori < prev_ori:
            return "Line {} invalid because previous origin was {}".\
                format(line, prev_ori)
        if ori > prev_ori:
            prev_ori = ori
            prev_dst = -1
        if dst <= prev_dst:
            return "Line {} invalid because previous destination was {}".\
                format(line, prev_dst)
        prev_dst = dst

        if count < 0:
            return "Line {} invalid because count is negative".format(count)
    return None


def validate_mobility_full(mobility: List[List[str]]) -> Optional[str]:
    """Check whether the mobility data file is correctly ordered and full

    The mobility data file is loaded from the file at path
    :py:func:`mobility_pipeline.data_interface.MOBILITY_PATH`. Correctly ordered
    means that the tower names' numeric portions strictly increase in
    origin-major order. Full means that there is a row for every combination of
    origin and destination tower.

    If this order were perfect, it would make forming the mobility matrix as
    easy as reshaping the last column. Unfortunately, this function showed that
    some coordinates are missing or out of order, so counts must be inserted
    manually.

    Args:
        mobility: List of mobility CSV data by applying ``list(csv.reader(f))``

    Returns:
        None if there is no error, otherwise a description of the error.
    """
    n_towers = int(mobility[-1][1][2:]) + 1
    i_row = 0

    for i_ori in range(n_towers):
        for i_dst in range(n_towers):
            _, ori, dst, _ = mobility[i_row]
            if ori != 'br{}'.format(i_ori) or dst != 'br{}'.format(i_dst):
                msg = 'INVALID: Row {} is {}, but we expected {}'.format(
                    i_row, mobility[i_row],
                    'date,br{},br{},count'.format(i_ori, i_dst)
                )
                return msg
            i_row += 1
    return None


def validate_tower_cells_aligned(cells: List[MultiPolygon],
                                 towers: np.ndarray) -> Optional[str]:
    """Check that each tower's index matches the cell at the same index

    For any cell ``c`` at index ``i``, an error is found if ``c`` has nonzero
    area and the tower at index ``i`` is not within ``c``.

    Args:
        cells: List of the cells (multi) polygons, in order
        towers: List of the towers' coordinates (latitude, longitude), in order

    Returns:
        A description of a found error, or ``None`` if no error found.
    """
    for i, cell in enumerate(cells):
        tower = Point(*towers[i])
        if cell.area != 0 and not cell.contains(tower):
            return "Tower at index {} not within cell at same index".format(i)
    return None


def validate_tower_index_name_aligned(csv_reader: Iterator)\
        -> Optional[str]:
    """Check that in the towers data file, the tower names match their indices

    Indices are zero-indexed from the second row in the file (to skip the
    header). An error is considered found if any tower name is not exactly
    :py:const:`TOWER_PREFIX` appended with the tower's index.

    Args:
        csv_reader: CSV reader from calling ``csv.reader(f)`` on the open data
            file ``f``

    Returns:
        A description of a found error, or ``None`` if no error found.
    """
    next(csv_reader)  # read past header
    for i, row in enumerate(csv_reader):
        lst = cast(List[str], row)  # TODO: Why is this needed?
        if lst[0] != TOWER_PREFIX + str(i):
            return 'Tower {} invalid because should have name {}{}'.\
                format(lst, TOWER_PREFIX, i)
    return None


def validate_contiguous_disjoint_cells(
        cells: List[Union[MultiPolygon, Polygon]]):
    """Check that cells are contiguous and disjoint and that they exist

    Checks:

    * That the cells are contiguous and disjoint. This is checked by comparing
      the sum of areas of each polygon and the area of their union. These two
      should be equal. The allowable deviation is specified by
      :py:const:`AREA_THRESHOLD`
    * That at least one cell is loaded.

    Returns:
        A description of a found error, or ``None`` if no error found.
    """

    if not cells:
        return 'No cells loaded (admins list empty)'

    area_sum = 0
    for mpol in cells:
        area_sum += mpol.area
    cell_union = unary_union(cells)
    union_area = cell_union.area
    diff = union_area - area_sum
    frac = diff / union_area
    if frac > AREA_THRESHOLD:
        return f'Cells not contiguous: ' \
            f'sum of areas {area_sum} < area of union {union_area}'
    if frac < - AREA_THRESHOLD:
        return f'Cells not disjoint: ' \
            f'sum of areas {area_sum} > area of union {union_area}'
    return None


def validate_admins() -> Optional[str]:
    """Check that the admins defined in the shapefile are reasonable

    Checks:

    * That the cells can be loaded by :py:mod:`load_admin_cells`.
    * That the cells are contiguous and disjoint. This is checked by comparing
      the sum of areas of each polygon and the area of their union. These two
      should be equal.
    * That at least one cell is loaded.

    Returns:
        A description of a found error, or ``None`` if no error found.
    """

    try:
        admins = load_admin_cells()
    except (FileNotFoundError, IOError) as e:
        msg = repr(e)
        return f'Loading admins failed with error: {msg}'

    error = validate_contiguous_disjoint_cells(admins)
    if error:
        return f'Invalid admin cells: {error}'
    return None


def validate_voronoi() -> Optional[str]:
    """Check that the Voronoi cells are reasonable

    Checks:

    * That the cells can be loaded by :py:mod:`load_cells`.
    * That the cells are contiguous and disjoint. This is checked by comparing
      the sum of areas of each polygon and the area of their union. These two
      should be equal.
    * That at least one cell is loaded.

    Returns:
        A description of a found error, or ``None`` if no error found.
    """
    try:
        cells = load_voronoi_cells()
    except (FileNotFoundError, IOError) as e:
        msg = repr(e)
        return f'Loading Voronoi cells failed with error: {msg}'
    error = validate_contiguous_disjoint_cells(cells)
    if error:
        return f'Invalid Voronoi cells: {error}'
    return None
