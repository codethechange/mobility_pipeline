.. UNICEF Mobility Pipeline documentation master file, created by
   sphinx-quickstart on Fri Apr 12 20:27:24 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to UNICEF Mobility Pipeline's documentation!
====================================================

.. image:: https://travis-ci.com/codethechange/mobility_pipeline.svg?branch=master
    :target: https://travis-ci.com/codethechange/mobility_pipeline

.. image:: https://codecov.io/gh/codethechange/mobility_pipeline/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/codethechange/mobility_pipeline

.. image:: https://readthedocs.org/projects/unicef-mobility-pipeline/badge/?version=latest
   :target: https://unicef-mobility-pipeline.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   Getting Started <generated/GETTING_STARTED>
   Contributing <generated/CONTRIBUTING>
   Code Documentation <modules>

To get started, see our `getting started guide <generated/GETTING_STARTED.html>`_.
If you would like to contribute, see our
`contributing guide <generated/CONTRIBUTING.html>`_.

This project is hosted on GitHub at
https://github.com/codethechange/mobility_pipeline

Program Overview
--------
Using the administrative region coverage of cell towers in Brazil as a guiding metric,
this program aims to model the migratory movement of humans from one cell tower region
to another.

Code Layout and Organization
------
The program is decomposed such that separate functions handle the following tasks:
- Mapping from the Voronoi seeds (the cell towers) to their corresponding cells (locations)
- Constructing the admin-to-admin mobility matrix
- Visualizing the data

Technical Paradigm
------


Datasets: Brazil Administrative Areas
------
The Brazil .shp file was downloaded via GADM (Database of Global Administrative Areas)
at the following URL: https://gadm.org/download_country_v3.html

The .shp file was converted to GeoJSON via the command line ogr2ogr tool. The first step
was to install GDAL. Then, we ran the following line:

ogr2ogr -f GeoJSON -t_srs crs:84 [name].geojson [name].shp

Legal
-----

This project was created by
`Stanford Code the Change <http://codethechange.stanford.edu>`_ for UNICEF.
It is available under the license in
`LICENSE.txt <https://github.com/codethechange/mobility_pipeline/blob/master/LICENSE.txt>`_

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
