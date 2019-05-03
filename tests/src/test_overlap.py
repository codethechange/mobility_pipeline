# pragma pylint: disable=missing-docstring


import numpy as np
from shapely.geometry.polygon import Polygon  # type: ignore
from lib.overlap import computeOverlap


def test_compute_overlap_simple():
    polygon1 = Polygon([(-1, -1), (-1, 1), (1, 1), (1, -1)])
    polygon2 = Polygon([(-3, -2), (-3, -1), (-1, -1), (-1, -2)])
    polygon3 = Polygon([(1, 1), (1, 2), (3, 2), (3, 1)])
    polygons = [polygon1, polygon2, polygon3]
    enclosing = Polygon([(-2, -3), (-2, 3), (2, 3), (2, -3)])

    assert np.all(computeOverlap(enclosing, polygons) == [1, 0.5, 0.5])
