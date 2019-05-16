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

import numpy as np  # type: ignore
import pandas as pd  # type: ignore


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
