# pragma pylint: disable=missing-docstring

from math import sqrt
from hypothesis import given
from hypothesis.strategies import lists, integers
import numpy as np
import pandas as pd
from shapely.geometry import MultiPolygon, Polygon
from mobility_pipeline.lib.make_matrix import make_tower_tower_matrix, \
    make_admin_admin_matrix, make_admin_to_tower_matrix, \
    make_tower_to_admin_matrix


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


def test_make_matrix_simple():
    a = np.array([[1, 2],
                  [3, 4]])
    b = np.array([[2, 3],
                  [4, 1]])
    c = np.array([[0, 1],
                  [5, 2]])
    e = np.array([[25, 20],
                  [65, 48]])

    assert np.all(make_admin_admin_matrix(b, a, c) == (a @ b) @ c)
    assert np.all((a @ b) @ c == e)


# Polygons for testing overlap calculation
A = MultiPolygon([Polygon([(-6, -2), (2, 6), (2, 2), (-2, -2)])])
B = MultiPolygon([Polygon([(-2, -2), (-2, 2), (2, 2), (2, -2)])])
C = MultiPolygon([Polygon([(0, -4), (0, 0), (4, 0), (4, -4)])])
D = MultiPolygon([Polygon([(2, -6), (2, -2), (4, -2), (4, -6)])])


def test_make_tower_to_admin():
    expected = [[8 / 16, 4 / 16],
                [0, 4 / 8]]
    expected = np.array(expected)

    towers = [A, C]
    admins = [B, D]
    actual = make_tower_to_admin_matrix(towers, admins)

    assert np.all(actual == expected)


def test_make_admin_to_tower():
    expected = [[8 / 24, 0],
                [4 / 16, 4 / 16]]
    expected = np.array(expected)

    towers = [A, C]
    admins = [B, D]
    actual = make_admin_to_tower_matrix(admins, towers)

    assert np.all(actual == expected)
