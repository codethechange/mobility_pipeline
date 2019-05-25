#!/usr/bin/env python3

from matplotlib import pyplot as plt  # type: ignore
from lib.make_matrix import make_a_to_b_matrix
from data_interface import load_admin_cells, load_cells
from shapely.geometry import MultiPolygon  # type: ignore
from descartes import PolygonPatch  # type: ignore
from random import uniform as rand


def plot_polygon(axes: plt.axes, polygon: MultiPolygon, color, _label="") -> None:
    patch = PolygonPatch(polygon, facecolor=color, edgecolor=[0, 0, 0], alpha=0.3, label=_label)
    axes.add_patch(patch)


def test_make_matrix():
    admin_cells = load_admin_cells()
    tower_cells = load_cells()
    # mat1 = make_tower_admin_matrix(admin_cells, tower_cells)
    print("before")
    mat = make_a_to_b_matrix(tower_cells, admin_cells)
    index = 1
    for i in range(len(mat[:, index])):
        if mat[i, index] != 0:
            print(str(i), mat[i, index])
    plt.ioff()
    fig = plt.figure()
    # (left, bottom, width, height) in units of fractions of figure dimensions
    ax = fig.add_axes((0.1, 0.1, 0.9, 0.9))
    ax.set_aspect(1)

    for i, admin in enumerate(admin_cells):
        if mat[i, index] != 0:
            plot_polygon(ax, admin, [rand(0,1), rand(0,1), rand(0,1)], str(i))
        else:
            plot_polygon(ax, admin, [0.1, 0, 0])
    plot_polygon(ax, tower_cells[index], [0, 0, 0])

    ax.relim()
    ax.autoscale_view()
    plt.legend()
    plt.show()


if __name__ == '__main__':
    test_make_matrix()
