"""Utilities for working with overlapping Polygons and MultiPolygons"""


from typing import Union
from shapely.geometry import Polygon, MultiPolygon # type: ignore


def compute_overlap(polygon_1: Union[Polygon, MultiPolygon],
                    polygon_2: Union[Polygon, MultiPolygon]):
    """Computes the fraction of the first polygon that intersects the second

    The returned fraction is ``(area of intersection) / (area of polygon_1)``.

    Args:
        polygon_1: The first polygon, whose total area will be the denominator
            for the computed fraction
        polygon_2: The second polygon

    Returns:
        The fraction of the first polygon that intersects the second

    """

    intersection = polygon_1.intersection(polygon_2)
    return intersection.area / polygon_1.area
