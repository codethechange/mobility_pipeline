# pragma pylint: disable=missing-docstring


from shapely.geometry.polygon import Polygon  # type: ignore
from lib.overlap import compute_overlap


def test_compute_overlap_simple():
    polygon1 = Polygon([(-1, -1), (-1, 1), (1, 1), (1, -1)])
    polygon2 = Polygon([(-3, -2), (-3, -1), (-1, -1), (-1, -2)])
    polygon3 = Polygon([(1, 1), (1, 2), (3, 2), (3, 1)])
    enclosing = Polygon([(-2, -3), (-2, 3), (2, 3), (2, -3)])

    assert compute_overlap(polygon1, enclosing) == 1
    assert compute_overlap(polygon2, enclosing) == 0.5
    assert compute_overlap(polygon3, enclosing) == 0.5
