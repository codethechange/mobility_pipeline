"""Tools for working with Voronoi tessellations

Given a 2-dimensional space with a set of points (called seeds), the Voronoi
tessellation is a partitioning of the space such that for every partition, which
is called a cell,
the cell contains exactly one seed, and every point in the cell is
closer to the cell's seed than it is to any other seed. For more
information, see https://en.wikipedia.org/wiki/Voronoi_diagram.

"""

from typing import List
import numpy as np  # type: ignore
from shapely.geometry import Polygon  # type: ignore


def load_voronoi(voronoi_json: List[List[List[float]]]) -> Polygon:
    """

    Loads Voronoi from JSON of the format:

    .. code-block::json

        [
            [
                [latitude, longitude],
                [latitude, longitude],
                ...
                [latitude, longitude]
            ]
        ]

    where each latitude-longitude pair describes a point of the Voronoi
    tessellation.

    Args:
        voronoi_json: The points that define the boundary of the Voronoi
            partition

    Returns:
        A polygon of the Voronoi partition

    """
    voronoi_points = np.array(voronoi_json[0])
    return Polygon(voronoi_points)
