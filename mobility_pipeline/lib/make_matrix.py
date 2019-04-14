"""Functions for making tower-tower, tower-admin, and admin-tower matrices

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
            ``[ORIGIN, DESTINATION, COUNT]``.
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
