================
Developer Manual
================

------------------
Technical Concepts
------------------

Matrices
========

We store program data internally as numpy matrices wherever possible so that
we can take advantage of numpy's optimizations. These are the main matrices
the data goes through:

* Tower-to-tower matrix: The raw mobility data between towers
* Tower-to-admin matrix: Stores the fraction of each administrative region
  that is within the range of each tower (covered by each tower's Voronoi
  cell).
* Admin-to-tower matrix: Stores the fraction of each tower's range (Voronoi
  cell) that is within each administrative region.
* Admin-to-admin matrix: The end product, which describes mobility between
  administrative regions.

For details, see :py:mod:`mobility_pipeline.lib.make_matrix`.


----------------------------
Code Layout and Organization
----------------------------

Utilities
=========

The python files outside of ``lib`` are executable script files meant to be run
from the terminal. While they may have functions, those functions are not
meant to be imported into other programs.

Library
=======

The files within ``lib`` form a library of functions that are format-agnostic
and designed to be repurposed in other programs. They are covered by unit tests
and are used by the utilities. They are broadly divided into the following
files:

* :py:mod:`mobility_pipeline.lib.make_matrix`: Functions for making and working
  with the matrices.
* :py:mod:`mobility_pipeline.lib.overlap`: Functions for working with polygon
  overlaps in general.
* :py:mod:`mobility_pipeline.lib.validate`: Functions for validating data
  formats.
* :py:mod:`mobility_pipeline.lib.voronoi`: Functions for working with Voronoi
  tessellations.

---------------------------
General Computation Process
---------------------------

We get the tower-to-tower matrix from the mobility data. Then, we use the
country shapefile and Voronoi tessellation to compute the tower-to-admin and
admin-to-tower matrices. Finally, we compute the admin-to-admin matrix
by multiplying the other three matrices like this:
``(tower-to-admin) * (tower-to-tower) * (admin-to-tower)``