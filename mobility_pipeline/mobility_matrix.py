#!/usr/bin/env python3

"""Generates the admin-to-admin mobility matrix from data files

Currently only computes the tower-to-tower matrix.
"""

import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from data_interface import load_mobility, load_towers


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
    mobility = pd.merge(df, mobility, how='left', on=['ORIGIN', 'DESTINATION'])
    mobility = mobility.fillna(0)
    np_array = mobility['COUNT'].values
    return np.reshape(np_array, (n_towers, n_towers))


if __name__ == '__main__':
    # pragma pylint: disable=invalid-name
    mobility_df = load_mobility()
    towers_mat = load_towers()

    tower_tower_mat = make_tower_tower_matrix(mobility_df, len(towers_mat))
