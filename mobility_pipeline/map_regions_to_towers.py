#!/usr/bin/env python3

"""Generate Mapping from Voronoi Cells to Seeds

Since we are given the Voronoi seeds (cell towers) separately from the
Voronoi cells and without a mapping between them, the script computes
this mapping by finding which cell each seed is contained within. The mapping
is printed so it can be inspected for relationships (e.g. the seed at index i
always is within the cell at index i), and the number of unique keys and values
in the mapping is printed to check whether the provided cells and seeds appear
valid. Indices of cells without towers and coordinates are also printed.
"""

from shapely.geometry import Point
from mobility_pipeline.lib.exploratory import map_cells_to_seeds
from mobility_pipeline.data_interface import load_towers, load_cells

if __name__ == '__main__':
    cells = load_cells()

    # Directed to numpy docs by https://stackoverflow.com/a/3519314
    towers_mat = load_towers()
    mapping = map_cells_to_seeds(cells, [Point(row[0], row[1])
                                         for row in towers_mat])
    unmapped = []
    for i in range(max(mapping) + 1):
        if i not in mapping:
            unmapped.append(i)
    no_coors = []
    for i, cell in enumerate(cells):
        if cell.area == 0:
            no_coors.append(i)
    print(mapping)
    print("numUniqKeys numUniqVals: ", len(mapping), len(set(mapping.values())))
    print("Indices of Cells Not Mapped to Tower: ", unmapped)
    print("Indices of Cells Without Coordinates: ", no_coors)
