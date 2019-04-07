# pragma pylint: disable=missing-docstring

import json
from mobility_pipeline.voronoi import load_voronoi


def test_load_voronoi():
    voronoi_json = "[[[-5, -5], [-5, 0], [5, 0], [5, -5]]]"
    polygon = load_voronoi(json.loads(voronoi_json))
    assert polygon.bounds == (-5.0, -5.0, 5.0, 0.0)  # (minx, miny, maxx, maxy)
    assert polygon.area == 50
