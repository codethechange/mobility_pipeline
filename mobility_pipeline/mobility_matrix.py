#!/usr/bin/env python3

"""Generates the admin-to-admin mobility matrix from data files

Currently only computes the tower-to-tower matrix.
"""
from matplotlib import pyplot as plt
from lib.make_matrix import make_tower_tower_matrix, generate_rtree
from data_interface import load_mobility, load_towers, load_polygons_from_json
from shapely.geometry import MultiPolygon  # type: ignore
from descartes import PolygonPatch  # type: ignore

DATA_PATH = "data/"
ADMIN_PATH = "%sbr_admin2.json" % DATA_PATH
TOWER_PATH = "%sbrazil-towers-voronoi-mobility/brazil-voronoi.json" % DATA_PATH

def plot_polygon(axes: plt.axes, polygon: MultiPolygon, color) -> None:
    patch = PolygonPatch(polygon, facecolor=color, edgecolor=[0, 0, 0], alpha=0.3)
    axes.add_patch(patch)

def test_overlap():
    index = 25
    admin_cells = load_polygons_from_json(ADMIN_PATH)
    admin_rtree, tree_index_mapping = generate_rtree(admin_cells)
    tower_cells = load_polygons_from_json(TOWER_PATH)
    tower_rtree, tree_index_mapping = generate_rtree(tower_cells)
    overlap = admin_rtree.query(tower_cells[index])
    # left, top, right, bottom = admin_cells[index].bounds

    # overlap = list(tower_rtree.intersection((left, bottom, right, top)))
    plt.ioff()

    fig = plt.figure()
    # (left, bottom, width, height) in units of fractions of figure dimensions
    ax = fig.add_axes((0.1, 0.1, 0.9, 0.9))
    ax.set_aspect(1)
    for a in admin_cells:
        plot_polygon(ax, a, [0.5, 0, 0])
    for p in overlap:
        plot_polygon(ax, p, [0, 0.5, 0])
    plot_polygon(ax, tower_cells[index], [0, 0, 0.5])
    ax.relim()
    ax.autoscale_view()

    plt.show()

if __name__ == '__main__':
    # pragma pylint: disable=invalid-name
    # mobility_df = load_mobility()
    # towers_mat = load_towers()

    # tower_tower_mat = make_tower_tower_matrix(mobility_df, len(towers_mat))
    
    test_overlap()
    
    

