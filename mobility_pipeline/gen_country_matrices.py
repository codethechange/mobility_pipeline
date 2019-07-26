#!/usr/bin/env python3

"""Generate admin-to-tower and tower-to-admin matries for a country"""

from argparse import ArgumentParser
from os import path

from data_interface import (
    load_voronoi_cells,
    convert_shape_to_json,
    load_admin_cells,
    save_admin_tower,
    save_tower_admin,
    DATA_PATH,
)
from lib.make_matrix import (
    make_tower_to_admin_matrix,
    make_admin_to_tower_matrix,
)


DESC = f"""Compute the admin-to-tower and tower-to-admin matrices for a country.

Meant to be run once for each shapefile (country and admin level).

Produces the admin-to-tower and tower-to-admin matrices as
DATA_PATH/[country_id]-admin-to-tower.json and
DATA_PATH/[country_id]-tower-to-admin.json where
DATA_PATH = '{path.abspath(DATA_PATH)}'. If shapefiles are used (i.e. if the
JSON is not found), the JSON will be generated at
DATA_PATH/[country-id]-shape.json.

If no shapefiles are specified, then the parsed Shapefiles as JSON must exist
as [country_id]-shape.json under DATA_PATH."""


def main():
    """Main function called when script run"""
    parser = ArgumentParser(
        description=DESC,
        epilog="""https://github.com/codethechange/mobility_pipeline""",
    )
    parser.add_argument("country_id", action="store",
                        help="Uniquely identifies country data in DATA_PATH")
    parser.add_argument("-s", "--shapefile_path_prefix", action="store",
                        help="Path, without file extension, to shapefiles")
    parser.add_argument("voronoi_path", action="store",
                        help="Path to the computed Voronoi tessellation")
    args = parser.parse_args()

    if args.shapefile_path_prefix:
        print("Converting Shapefiles to GeoJSON")
        convert_shape_to_json(args.shapefile_path_prefix, args.country_id)
    else:
        print("Assuming GeoJSON file already exists.")
    print("Loading admin and Voronoi cells")
    tower_cells = load_voronoi_cells(args.voronoi_path)
    admin_cells = load_admin_cells(args.country_id)

    print("Generating tower-to-admin matrix")
    tower_admin_mat = make_tower_to_admin_matrix(tower_cells, admin_cells)
    print("Generating admin-to-tower matrix")
    admin_tower_mat = make_admin_to_tower_matrix(admin_cells, tower_cells)

    print("Saving matrices")
    save_tower_admin(args.country_id, tower_admin_mat)
    save_admin_tower(args.country_id, admin_tower_mat)


if __name__ == "__main__":
    main()
