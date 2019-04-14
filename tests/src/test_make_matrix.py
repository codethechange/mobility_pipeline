# pragma pylint: disable=missing-docstring

from math import sqrt
from hypothesis import given
from hypothesis.strategies import lists, integers
import numpy as np
import pandas as pd
from mobility_pipeline.lib.make_matrix import make_tower_tower_matrix


PANDAS_COLUMNS = ['ORIGIN', 'DESTINATION', 'COUNT']


def test_make_tower_tower_matrix_simple_full():
    raw_mat = [PANDAS_COLUMNS,
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
    raw_mat = [PANDAS_COLUMNS,
               [0, 0, 5],
               [1, 0, 2],
               [1, 1, 0]]
    mobility = pd.DataFrame(raw_mat[1:], columns=raw_mat[0])
    mat = make_tower_tower_matrix(mobility, 2)
    expected_mat = [[5, 0],
                    [2, 0]]
    assert np.all(mat == expected_mat)


@given(lists(integers(min_value=0), min_size=1), integers(min_value=1))
def test_make_tower_tower_matrix_hypothesis(nums, num):
    nums.append(num)
    n_towers = int(sqrt(len(nums)))
    nums = nums[:n_towers ** 2]
    raw_mat = []
    nums_i = 0
    for i in range(n_towers):
        for j in range(n_towers):
            if nums[nums_i] != 0:
                raw_mat.append([i, j, nums[nums_i]])
            nums_i += 1
    mobility = pd.DataFrame(raw_mat, columns=PANDAS_COLUMNS)
    mat = make_tower_tower_matrix(mobility, n_towers)
    expected_mat = np.reshape(np.array(nums), (n_towers, n_towers))

    assert np.all(mat == expected_mat)
