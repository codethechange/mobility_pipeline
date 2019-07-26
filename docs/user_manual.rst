
=======================
Using mobility_pipeline
=======================

-----
Setup
-----

Getting Shapefiles
==================

Download the shapefile (``.shp``) from
`GADM <https://gadm.org/download_country_v3.html>`_
(Database of Global Administrative Areas). After unpacking the zip file, be sure
to choose the ``.shp`` file that corresponds to the level of admin you want
(e.g. states versus counties in the United States).

Next, conver the ``.shp`` file into a GeoJSON format via the command line tool
``ogr2ogr``, available by installing
`GDAL <https://www.gdal.org/>`_. Then, do the conversion with this command:

.. code-block:: console

    ogr2ogr -f GeoJSON -t_srs crs:84 [name].geojson [name].shp

replacing ``[name]`` to match your ``.shp`` file.

Configuration
=============

Regardless of what you want to use mobility_pipeline for, you will need to
tell it how to find your data. You can do so by adjusting the constants
in :py:mod:`mobility_pipeline.data_interface`. These constants are:

* :py:const:`mobility_pipeline.data_interface.DATA_PATH`: The path to the folder
  holding your data.
* :py:const:`mobility_pipeline.data_interface.TOWERS_PATH`: This is a CSV file
  containing the coordinates of
  each cell tower.
* :py:const:`mobility_pipeline.data_interface.VORONOI_PATH`: This is a JSON file
  that describes the cells of a
  `Voronoi Tessellation <https://en.wikipedia.org/wiki/Voronoi_diagram>`_ whose
  seeds are the cell towers.
* :py:const:`mobility_pipeline.data_interface.MOBILITY_PATH`: This is a CSV file
  holding the mobility data.
* :py:const:`mobility_pipeline.data_interface.TOWER_PREFIX`: This is a string
  that prefixes tower indices in the
  tower name. For example, Brazil towers might be named ``br0``, ``br1``, etc.
  with ``br`` being the prefix.

For details on the required formats of these files, see the documentation for
:py:mod:`data_interface`.

-------------------
Running the Program
-------------------

There are 2 scripts:
* ``gen_country_matrices.py``: run once for each admin level / country you want
  data for. It will generate the admin-to-tower and tower-to-admin matrices.
* ``gen_day_mobility.py``: run for each day's worth of data. It will compute
  the admin-to-admin mobility data.

For both scripts, run with ``--help`` for more usage information. Both scripts
also run independently of the path constants in ``data_interface.py``. Instead,
they accept command-line arguments that define their operation.

-----------------
Running Utilities
-----------------

This program also comes with utilities. These utilities use the constants in
``data_interface.py`` for the most part.

Plot Voronoi
============

To get a sense for what the Voronoi tessellation looks like, you can plot it by
running ``plot_voronoi.py``. This will display a plot of all the Voronoi
cells with the tower positions overlayed. For details, see the documentation
for :py:mod:`mobility_pipeline.plot_voronoi`.

Visualize Overlaps
==================

To see what the overlaps look like, you can see a plot of the shapefile with
one Voronoi cell and the admin regions it might overlap with color-coded. The
script also prints out the values that would go in the tower-to-admin matrix so
you can see what the numbers represent visually. To see the plot, run
``visualize_overlaps.py``. For details, see
:py:mod:`mobility_pipeline.visualize_overlaps`.

Validate Data File Formats
==========================

You can run some checks to provide some assurance that a set of data files are
formatted as the program expects. After configuring the data paths as described
above, you can run these checks by executing ``check_validation.py``. You can
also look at the code in this file to see what format the program expects. For
details, see :py:mod:`mobility_pipeline.check_validation`.