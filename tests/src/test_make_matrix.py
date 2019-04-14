# pragma pylint: disable=missing-docstring

import numpy as np
import pandas as pd
from mobility_pipeline.lib.make_matrix import make_tower_tower_matrix


def test_make_tower_tower_matrix_simple_full():
    raw_mat = [['ORIGIN', 'DESTINATION', 'COUNT'],
               [0, 0, 5],
               [0, 1, 3],
               [1, 0, 2],
               [1, 1, 0]]
    mobility = pd.DataFrame(raw_mat[1:], columns=raw_mat[0])
    mat = make_tower_tower_matrix(mobility, 2)
    expected_mat = [[5, 3],
                    [2, 0]]
    assert np.all(mat == expected_mat)


def test_make_tower_tower_matrix_simple_missing_rows():
    raw_mat = [['ORIGIN', 'DESTINATION', 'COUNT'],
               [0, 0, 5],
               [1, 0, 2],
               [1, 1, 0]]
    mobility = pd.DataFrame(raw_mat[1:], columns=raw_mat[0])
    mat = make_tower_tower_matrix(mobility, 2)
    expected_mat = [[5, 0],
                    [2, 0]]
    assert np.all(mat == expected_mat)
