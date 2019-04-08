"""Tools for working with Voronoi tessellations

Given a 2-dimensional space with a set of points (called seeds), the Voronoi
tessellation is a partitioning of the space such that for every partition, which
is called a cell,
the cell contains exactly one seed, and every point in the cell is
closer to the cell's seed than it is to any other seed. For more
information, see https://en.wikipedia.org/wiki/Voronoi_diagram.
"""


from typing import List, Union, cast
from mypy_extensions import TypedDict
import numpy as np  # type: ignore
from shapely.geometry import Polygon, MultiPolygon  # type: ignore


def json_to_polygon(points_json: List[List[float]]) -> Polygon:
    """Loads a Polygon from a JSON of points

    Loads Polygon from a JSON of the format:

    .. code-block::json

            [
                [latitude, longitude],
                [latitude, longitude],
                ...
                [latitude, longitude]
            ]

    where each latitude-longitude pair describes a point defining the boundary
    of the polygon.

    Args:
        points_json: The points that define the boundary of the polygon

    Returns:
        A polygon
    """
    pts = np.array(points_json)
    return Polygon(pts)


class VoronoiCell(TypedDict):
    """This class describes is for type hinting Voronoi cell JSONs
    """
    type: str
    # Helpful explanation of type Union: https://stackoverflow.com/a/51304069
    coordinates: Union[List[List[List[float]]], List[List[List[List[float]]]]]


def load_cell(cell_json: VoronoiCell) -> MultiPolygon:
    """Loads a Voronoi cell from JSON in ``Polygon`` or ``MultiPolygon`` format

    Loads Voronoi cell from a JSON of the ``Polygon`` format:

    .. code-block::json

        {
            "type": "Polygon",
            "coordinates": [
                [
                    [latitude, longitude],
                    [latitude, longitude],
                    ...
                    [latitude, longitude]
                ]
            ]
        }

    or of the ``MultiPolygon`` format:

    .. code-block::json

        {
            "type": "MultiPolygon",
            "coordinates": [
                [
                    [
                        [latitude, longitude],
                        [latitude, longitude],
                        ...
                        [latitude, longitude]
                    ]
                ],
                [
                    [
                        [latitude, longitude],
                        [latitude, longitude],
                        ...
                        [latitude, longitude]
                    ]
                ],
                ...
                [
                    [
                        [latitude, longitude],
                        [latitude, longitude],
                        ...
                        [latitude, longitude]
                    ]
                ]
            ]
        }

    where each latitude-longitude pair describes a point of the Voronoi
    tessellation. If the JSON is in the ``Polygon`` format, a
    ``shapely.geometry.MultiPolygon`` object will be returned where the
    ``MultiPolygon`` has one member, the described polygon.

    The value of the ``type`` key is used to distinguish ``Polygon`` and
    ``MultiPolygon`` formats.

    Args:
        cell_json: The points that define the boundary of the Voronoi
            cell

    Returns:
        A polygon of the Voronoi cell
    """
    # We typecast because the value of `type` tells us the type of `coordinates`
    if cell_json['type'] == 'Polygon':
        coors = cast(List[List[List[float]]], cell_json['coordinates'])
        pol = json_to_polygon(coors[0])
        return MultiPolygon([pol])
    pols = [json_to_polygon(pol_json[0]) for pol_json in
            cast(List[List[List[List[float]]]], cell_json['coordinates'])]
    return MultiPolygon(pols)
