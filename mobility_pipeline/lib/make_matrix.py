"""Functions for making tower-tower, tower-admin, and admin-tower matrices

"""

import numpy as np  # type: ignore
import pandas as pd  # type: ignore

from typing import List, Union, cast
from mypy_extensions import TypedDict
import numpy as np  # type: ignore
from shapely.geometry import Polygon, MultiPolygon 
from shapely.strtree import STRtree
from overlap import compute_overlap
# from rtree import index


from matplotlib import pyplot as plt # FOR TESTING PURPOSES

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

def generate_rtree(polygons):
    tree = STRtree(polygons)
    index_mapping = {}
    for i, mpoly in enumerate(polygons):
        index_mapping[tuple([tuple(p.exterior.coords) for p in mpoly])] = i
    return (tree, index_mapping)
    # rtree_idx = index.Index()
    # for i, polygon in enumerate(polygons):
    #     left, top, right, bottom = polygon.bounds
    #     rtree_idx.insert(i, (left, bottom, right, top))
    # return rtree_idx
        


def make_tower_admin_matrix(admin_cells, tower_cells) -> np.ndarray:
    #make zeroed matrix
    mat = np.zeros(len(admin_cells), len(tower_cells))
    #generate tree and mapping
    admin_rtree, tree_index_mapping = generate_rtree(admin_cells)
    for i, tower in enumerate(tower_cells):
        #find overlapping polys using opposing rtree
        overlapping_cells = admin_rtree.query(tower)
        for admin in overlapping_cells:
            #compute true overlap and update corresponding entry in matrix
            coords = tuple([tuple(admin.exterior.coords)])
            mat[tree_index_mapping[coords]][i] = compute_overlap(tower, admin)
    return mat





