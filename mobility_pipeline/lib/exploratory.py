"""Various functions used to explore the data but not for the pipeline itself

"""


from typing import List, Dict
from shapely.geometry import MultiPolygon, Point  # type: ignore


def map_cells_to_seeds(cells: List[MultiPolygon], seeds: List[Point]) \
        -> Dict[int, int]:
    """Generates a mapping from Voronoi tessellation cells to seed coordinates

    Each seed should reside in exactly one cell, and each cell should contain
    exactly one seed. This function finds which seed belongs to which cell and
    produces a mapping from cells to the seeds they contain.

    Args:
        cells: The cells of the Voronoi tessellation
        seeds: The seeds of the Voronoi tessellation

    Returns:
        A dictionary whose keys are indices of ``cells`` and whose values are
        indices of ``seed_coors``.

    """

    mapping: Dict[int, int] = {}

    for i_cell, cell in enumerate(cells):
        for i_seed, seed in enumerate(seeds):
            if cell.contains(seed):
                mapping[i_cell] = i_seed

    return mapping
