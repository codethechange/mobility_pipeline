#!/usr/bin/env python3

"""Tool for plotting the Voronoi tessellation described by the provided data

Note that the seeds of the tessellation are based on the provided towers file,
not computed from the cells. The tool also prints to the console the number
of towers and number of cells.
"""

from matplotlib import pyplot as plt
from shapely.geometry.polygon import Polygon
from descartes import PolygonPatch
from data_interface import load_cells, load_towers


def plot_polygon(axes: plt.axes, polygon: Polygon) -> None:
    """Add a polygon to an axes

    Args:
        axes: The axes to add the polygon to
        polygon: The polygon to add

    Returns:
        None
    """
    patch = PolygonPatch(polygon, facecolor=[0, 0, 0.5], edgecolor=[0, 0, 0],
                         alpha=0.5)
    axes.add_patch(patch)


if __name__ == '__main__':
    cells = load_cells()
    towers = load_towers()
    print('Number of Cells: ', len(cells), 'Number of Towers: ', len(towers))

    # Learned how to plot from:
    # https://chrishavlin.com/2016/11/28/shapefiles-in-python-polygons/
    plt.ioff()

    fig = plt.figure()
    # (left, bottom, width, height) in units of fractions of figure dimensions
    ax = fig.add_axes((0.1, 0.1, 0.9, 0.9))
    ax.set_aspect(1)

    for cell in cells:
        plot_polygon(ax, cell)
    for lat, lng in towers:
        ax.plot(lat, lng, color='red', marker='o', markersize=2)

    # Showed how to auto-resize axes: https://stackoverflow.com/a/11039268
    ax.relim()
    ax.autoscale_view()

    plt.show()
