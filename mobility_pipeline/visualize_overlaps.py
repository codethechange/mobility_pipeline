#!/usr/bin/env python3

"""Plots one Voronoi cell on top of all the administrative regions. The admins
that intersect the Voronoi cell are colored by index and have the associated
values from the tower-to-admin matrix printed. This lets you check that the
matrix values seem reasonable.
"""

from matplotlib import pyplot as plt  # type: ignore
from lib.make_matrix import make_a_to_b_matrix
from data_interface import load_admin_cells, load_cells
from shapely.geometry import MultiPolygon  # type: ignore
from descartes import PolygonPatch  # type: ignore
from random import uniform as rand


I_TOWER_TO_COLOR = 1
"""Index of Voronoi cell to show."""


def plot_polygon(axes: plt.axes, polygon: MultiPolygon, color, _label="") \
        -> None:
    """Plot a polygon (or multipolygon) with matplotlib

    Args:
        axes: The matplotlib axes to plot on
        polygon: The polygon to plot
        color: Color to use for shading the polygon
        _label: Label for the polygon that will be displayed in the legend

    Returns:
        None
    """
    patch = PolygonPatch(polygon, facecolor=color, edgecolor=[0, 0, 0],
                         alpha=0.3, label=_label)
    axes.add_patch(patch)


if __name__ == '__main__':
    admin_cells = load_admin_cells()
    tower_cells = load_cells()
    mat = make_a_to_b_matrix(tower_cells, admin_cells)
    for i in range(len(mat[:, I_TOWER_TO_COLOR])):
        if mat[i, I_TOWER_TO_COLOR] != 0:
            print(str(i), mat[i, I_TOWER_TO_COLOR])
    plt.ioff()
    fig = plt.figure()
    # (left, bottom, width, height) in units of fractions of figure dimensions
    ax = fig.add_axes((0.1, 0.1, 0.9, 0.9))
    ax.set_aspect(1)

    for i, admin in enumerate(admin_cells):
        if mat[i, I_TOWER_TO_COLOR] != 0:
            plot_polygon(ax, admin, [rand(0, 1), rand(0, 1), rand(0, 1)],
                         str(i))
        else:
            plot_polygon(ax, admin, [0.1, 0, 0])
    plot_polygon(ax, tower_cells[I_TOWER_TO_COLOR], [0, 0, 0])

    ax.relim()
    ax.autoscale_view()
    plt.legend()
    plt.show()
