"""Functions for making tower-tower, tower-admin, and admin-tower matrices

"""

import numpy as np  # type: ignore
import pandas as pd  # type: ignore

from typing import List, Union, cast
from mypy_extensions import TypedDict
import numpy as np  # type: ignore
from shapely.geometry import Polygon, MultiPolygon 
from shapely.strtree import STRtree


from matplotlib import pyplot as plt # FOR TESTING PURPOSES


ADMIN_PATH = "%sbr_admin2.json"


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
    return STRtree(polygons)

def make_tower_admin_matrix() -> np.ndarray:
    admin_cells = load_polygons_from_json(ADMIN_PATH)
    # admin_rtree = generate_rtree(admin_cells)
    tower_cells = load_polygons_from_json(TOWER_PATH)
    tower_rtree = generate_rtree(tower_cells)
    # overlap = admin_rtree.query(tower_cells[index])
    overlap = tower_rtree.query(admin_cells[index])
    plt.ioff()

    fig = plt.figure()
    # (left, bottom, width, height) in units of fractions of figure dimensions
    ax = fig.add_axes((0.1, 0.1, 0.9, 0.9))
    ax.set_aspect(1)
    for a in tower_cells:
        plot_polygon(ax, a, [0.5, 0, 0])
    for p in overlap:
        plot_polygon(ax, p, [0, 0.5, 0])
    plot_polygon(ax, admin_cells[index], [0, 0, 0.5])
    ax.relim()
    ax.autoscale_view()

    plt.show()


