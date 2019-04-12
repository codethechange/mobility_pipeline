#!/usr/bin/env python3

"""Generate Mapping from Voronoi Cells to Seeds

Since we are given the Voronoi seeds (cell towers) separately from the
Voronoi cells and without a mapping between them, the script computes
this mapping by finding which cell each seed is contained within. The mapping
is printed so it can be inspected for relationships (e.g. the seed at index i
always is within the cell at index i), and the number of unique keys and values
in the mapping is printed to check whether the provided cells and seeds appear
valid.
"""

import json
import numpy as np
from shapely.geometry import Point
from mobility_pipeline.exploratory import map_cells_to_seeds
from mobility_pipeline.voronoi import load_cell
from data_interface import TOWERS_PATH, VORONOI_PATH

if __name__ == '__main__':
    with open(VORONOI_PATH, 'r') as f:
        raw_json = json.loads(f.read())
    cells = [load_cell(feature['geometry']) for feature in raw_json['features']]

    # Directed to numpy docs by https://stackoverflow.com/a/3519314
    towers_mat = np.genfromtxt(TOWERS_PATH, delimiter=',')
    towers_mat = towers_mat[:, 1:]
    mapping = map_cells_to_seeds(cells, [Point(row[0], row[1])
                                         for row in towers_mat])
    print(mapping)
    print("numUniqKeys numUniqVals: ", len(mapping), len(set(mapping.values())))
