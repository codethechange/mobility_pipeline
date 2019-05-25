"""Functions for making tower-tower, tower-admin, and admin-tower matrices

Matrices:

* tower-tower: The raw mobility data between cell towers. The value at row ``i``
  and column ``j`` is the number of people who move on that day from the
  region served by tower ``i`` to the region served by tower ``j``. Note that
  really, this is the number of cell phones that connect to tower ``i`` in the
  morning and tower ``j`` in the evening, which we assume represents a person
  moving. This matrix has row indices of the origin towers and column indices
  of the destination towers.
* tower-admin: Computed from the Voronoi tessellation and the country shapefile,
  this matrix represents the percent of each admin that is covered by each
  tower. For any ``x`` in the matrix at row ``i`` and column ``j``, we know
  that a fraction ``x`` of the admin with index ``i`` is covered by the tower
  with index ``j``. This means that the matrix has row indices of admin
  indices and column indices of tower indices.
* admin-tower: Computed from the Voronoi tessellation and the country shapefile,
  this matrix represents the percent of each tower's range that is within each
  admin. For any ``x`` in the matrix at row ``i`` and column ``j``, we know
  that a fraction ``x`` of the Voronoi cell for the tower with index ``i`` is
  within the admin
  with index ``j``. This means that the matrix has row indices of tower
  indices and column indices of admin indices.
* admin-admin: This is the final mobility matrix, which represents the number
  of people who move between admins each day. The value at row ``i`` and
  column ``j`` is the number of people who move on that day from the admin
  with index ``i`` to the admin with index ``j``. This is, of course, being
  estimated from cell phone data and the overlaps as computed in the other
  matrices.

This strategy is explained by Mike Fabrikant at UNICEF:
https://medium.com/@mikefabrikant/cell-towers-chiefdoms-and-anonymized-call-detail-records-a-guide-to-creating-a-mobility-matrix-d2d5c1bafb68
"""

from collections.abc import Sequence
from typing import Tuple, Dict, List
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from shapely.strtree import STRtree  # type: ignore
from shapely.geometry import MultiPolygon  # type: ignore
from lib.overlap import compute_overlap


def make_tower_tower_matrix(mobility: pd.DataFrame, n_towers: int) \
        -> np.ndarray:
    """Make tower-to-tower mobility matrix

    Thank you to Tomas Bencomo (https://github.com/tjbencomo) for writing the
    initial version of this function.

    Args:
        mobility: DataFrame of mobility data with columns
            ``[ORIGIN, DESTINATION, COUNT]``. All values should be numeric.
        n_towers: Number of towers, which defines the length of each matrix
            dimension

    Returns:
        The tower-to-tower matrix, which has shape ``(n_towers, n_towers)`` and
        where the value at row ``i`` and column ``j`` is the mobility count for
        origin ``i`` and destination ``j``.

    """
    ori_indices = np.array([np.repeat(i, n_towers)
                            for i in np.arange(0, n_towers)]).flatten()
    dst_indices = np.tile(np.arange(0, n_towers), n_towers)
    df = pd.DataFrame({'ORIGIN': ori_indices, 'DESTINATION': dst_indices})
    mobility = df.merge(mobility, how='left', on=['ORIGIN', 'DESTINATION'])
    mobility = mobility.fillna(0)
    np_array = mobility['COUNT'].values
    return np.reshape(np_array, (n_towers, n_towers))


def generate_rtree(polygons: Sequence) -> Tuple[STRtree,
                                                Dict[Tuple[tuple, ...], int]]:
    """Helper function that builds an RTree from MultiPolygons

    The Rtree is built from MultiPolygons using
    :py:class:`shapely.strtree.STRtree`. Since the RTree returns the overlapping
    MultiPolygons, we need a way to retrieve the polygon's index. We do this
    with a dictionary from the exterior coordinates (`Polygon.exterior.coords`)
    of every Polygon in the MultiPolygon to the MultiPolygon's index in the
    provided Sequence.

    Specifically, you can generate the key for a given MultiPolygon ``mpoly``
    like so:

    .. code-block:: python

        key = tuple([tuple(p.exterior.coords) for p in mpoly])

    Args:
        polygons: A Sequence of MultiPolygons. Must be iterable and able to be
            passed to the ``STRtree`` constructor. Iteration must be
            deterministic.

    Returns:
        A tuple of the RTree and the index mapping dictionary.

    """
    tree = STRtree(polygons)
    index_mapping = {}
    for i, mpoly in enumerate(polygons):
        index_mapping[tuple([tuple(p.exterior.coords) for p in mpoly])] = i
    return tree, index_mapping


def make_a_to_b_matrix(a_cells: List[MultiPolygon],
                       b_cells: List[MultiPolygon]) -> np.ndarray:
    """Create an overlap matrix from sequence A to B

    Computes for every pair of MultiPolygons between A and B, the fraction of
    the MultiPolygon in B that is covered by the one in A. We use an RTree to
    reduce the number of overlaps we have to compute by only computing overlaps
    between MultiPolygons that have overlapping bounding boxes.

    Args:
        a_cells: Sequence A of MultiPolygons
        b_cells: Sequence B of MultiPolygons

    Returns:
        A matrix with row indices that correspond to the indices of B and column
        indices that correspond to the indices of A. Every element at row
        ``i`` and column ``j`` in the matrix represents the fraction of the
        MultiPolygon in B at index ``i`` that overlaps with the MultiPolygon in
        A at index ``j``.
    """
    mat = np.zeros((len(a_cells), len(b_cells)))
    a_rtree, tree_index_mapping = generate_rtree(a_cells)
    for i, bcell in enumerate(b_cells):
        overlapping_cells = a_rtree.query(bcell)
        for acell in overlapping_cells:
            # compute true overlap and update corresponding entry in matrix
            coords = tuple([tuple(pol.exterior.coords) for pol in acell])
            mat[tree_index_mapping[coords]][i] = compute_overlap(bcell, acell)
    return mat


def make_tower_to_admin_matrix(admin_cells: List[MultiPolygon],
                               tower_cells: List[MultiPolygon])\
        -> np.ndarray:
    """Compute the tower-to-admin matrix.

    This is a wrapper function for :py:meth:`make_a_to_b_matrix`, with matrices
    A and B as denoted for each argument.

    Args:
        admin_cells: Sequence of administrative regions; used as matrix A.
        tower_cells: Sequence of Voronoi cells; used as matrix B.

    Returns:
        The tower-admin matrix.
    """
    return make_a_to_b_matrix(tower_cells, admin_cells)


def make_admin_to_tower_matrix(tower_cells: List[MultiPolygon],
                               admin_cells: List[MultiPolygon]) \
        -> np.ndarray:
    """Compute the admin-to-tower matrix.

    This is a wrapper function for :py:meth:`make_a_to_b_matrix`, with matrices
    A and B as denoted for each argument.

    Args:
        tower_cells: Sequence of Voronoi cells; used as matrix A.
        admin_cells: Sequence of administrative regions; used as matrix B.

    Returns:
        The admin-tower matrix.
    """
    return make_a_to_b_matrix(admin_cells, tower_cells)


def make_admin_admin_matrix(tower_tower: np.ndarray, tower_admin: np.ndarray,
                            admin_tower: np.ndarray) -> np.ndarray:
    """Compute the admin-to-admin matrix

    Computed by multiplying the three provided matrices like so:
    (tower_admin) * (tower_tower) * (admin_tower)

    Args:
        tower_tower: The tower-to-tower mobility data
        tower_admin: Stores the fraction of each admin that is covered by each
            cell tower
        admin_tower: Stores the fraction of each cell tower's range that is
            within each admin

    Returns:
        An admin-to-admin mobility matrix such that each value with row index
        ``i`` and column index ``j`` is the estimated number of people who moved
        that day from the admin with index ``i`` to the admin with index ``j``.
    """
    return (tower_admin @ tower_tower) @ admin_tower
