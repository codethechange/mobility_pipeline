# pragma pylint: disable=missing-docstring

import json
from mobility_pipeline.voronoi import load_cell


def test_load_cell():
    voronoi_json = "[[-5, -5], [-5, 0], [5, 0], [5, -5]]"
    polygon = load_cell(json.loads(voronoi_json))
    assert polygon.bounds == (-5.0, -5.0, 5.0, 0.0)  # (minx, miny, maxx, maxy)
    assert polygon.area == 50
