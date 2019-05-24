#!/usr/bin/env python3

"""Generates the admin-to-admin mobility matrix from data files

Currently only computes the tower-to-tower matrix.
"""
from matplotlib import pyplot as plt
from lib.make_matrix import make_tower_tower_matrix, generate_rtree, make_a_to_b_matrix
from data_interface import load_mobility, load_towers, load_polygons_from_json
from shapely.geometry import MultiPolygon  # type: ignore
from descartes import PolygonPatch  # type: ignore
from random import uniform as rand

DATA_PATH = "data/"
ADMIN_PATH = "%sbr_admin2.json" % DATA_PATH
TOWER_PATH = "%sbrazil-towers-voronoi-mobility/brazil-voronoi.json" % DATA_PATH

def plot_polygon(axes: plt.axes, polygon: MultiPolygon, color, _label="") -> None:
    patch = PolygonPatch(polygon, facecolor=color, edgecolor=[0, 0, 0], alpha=0.3, label=_label)
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

def test_make_matrix():
    admin_cells = load_polygons_from_json(ADMIN_PATH)
    tower_cells = load_polygons_from_json(TOWER_PATH)
    # mat1 = make_tower_admin_matrix(admin_cells, tower_cells)
    print("before")
    mat = make_a_to_b_matrix(tower_cells, admin_cells)
    index = 1
    for i in range(len(mat[index,:])):
        if mat[index, i] != 0:
            print(str(i), mat[index,i])
    plt.ioff()
    fig = plt.figure()
    # (left, bottom, width, height) in units of fractions of figure dimensions
    ax = fig.add_axes((0.1, 0.1, 0.9, 0.9))
    ax.set_aspect(1)

    for i, admin in enumerate(admin_cells):
        if mat[index, i] != 0:
            plot_polygon(ax, admin, [rand(0,1), rand(0,1), rand(0,1)], str(i))
        else:
            plot_polygon(ax, admin, [0.1, 0, 0])
    plot_polygon(ax, tower_cells[index], [0, 0, 0])

    ax.relim()
    ax.autoscale_view()
    plt.legend()
    plt.show()




if __name__ == '__main__':
    # pragma pylint: disable=invalid-name
    # mobility_df = load_mobility()
    # towers_mat = load_towers()

    # tower_tower_mat = make_tower_tower_matrix(mobility_df, len(towers_mat))
    
    # test_overlap()
    test_make_matrix()
    
    

