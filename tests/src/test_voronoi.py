# pragma pylint: disable=missing-docstring

import json
from shapely.geometry import Point
from mobility_pipeline.voronoi import load_cell


def test_load_cell_polygon():
    voronoi_json = """
    {
        "type": "Polygon",
        "coordinates": [
            [
                [-5, -5],
                [-5, 0],
                [5, 0],
                [5, -5]
            ]
        ]
    }
    """
    polygon = load_cell(json.loads(voronoi_json))
    assert polygon.bounds == (-5.0, -5.0, 5.0, 0.0)  # (minx, miny, maxx, maxy)
    assert polygon.area == 50


def test_load_cell_multipolygon():
    voronoi_json = """
    {
        "type": "MultiPolygon",
        "coordinates": [
            [
                [
                    [-5, -5],
                    [-5, 0],
                    [5, 0],
                    [5, -5]
                ]
            ],
            [
                [
                    [5, 0],
                    [10, 0],
                    [10, 5],
                    [5, 5]
                ]
            ]
        ]
    }
    """
    polygon = load_cell(json.loads(voronoi_json))
    print(len(polygon.geoms))
    assert polygon.bounds == (-5.0, -5.0, 10.0, 5.0)  # (minx, miny, maxx, maxy)
    assert polygon.area == 50 + 25
    assert polygon.contains(Point(0, -2))
    assert polygon.contains(Point(7, 3))
    assert not polygon.contains(Point(0, 0))  # Boundaries are not contained
    assert not polygon.contains(Point(5, 0))
    assert not polygon.contains(Point(0, 5))
