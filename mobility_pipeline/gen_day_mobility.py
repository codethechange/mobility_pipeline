#!/usr/bin/env python3

"""Generate admin-to-admin mobility matrix for a single day"""

from argparse import ArgumentParser
from os import path

from data_interface import (
    load_mobility,
    load_admin_tower,
    load_tower_admin,
    save_admin_admin,
    DATA_PATH,
)
from lib.make_matrix import (
    make_tower_tower_matrix,
    make_admin_admin_matrix,
)


DESCRIPTION = f"""Compute the admin-to-admin matrix for one day's data

Meant to be run once for each day you want mobility data for.

Produces the admin-to-admin mobility matrix as
DATA_PATH/[country_id]-[day_id]-admin-to-admin.csv. where
DATA_PATH = '{path.abspath(DATA_PATH)}'.

The following files must be present under the directory at DATA_PATH:
* [identifier]-shape.json: JSON form of country shapefile
* [identifier]-tower-to-admin.csv: Tower-to-admin matrix
* [identifier]-admin-to-tower.csv: Admin-to-tower matrix"""


def main():
    """Called when script run"""
    parser = ArgumentParser(
        description=DESCRIPTION,
        epilog="""https://github.com/codethechange/mobility_pipeline""",
    )
    parser.add_argument("country_id", action="store",
                        help="Uniquely identifies country data in DATA_PATH")
    parser.add_argument("day_id", action="store",
                        help="Uniquely identifies the day to process data for")
    parser.add_argument("mobility_path", action="store",
                        help="Path to the mobility data to use")
    args = parser.parse_args()

    print("Loading Mobility Data")
    mobility_df = load_mobility(args.mobility_path)

    print("Loading Tower-to-Admin and Admin-to-Tower Matrices")
    tower_admin_mat = load_tower_admin(args.country_id)
    admin_tower_mat = load_admin_tower(args.country_id)

    print("Computing Admin-to-Admin Matrix")
    tower_tower_mat = make_tower_tower_matrix(mobility_df, len(admin_tower_mat))

    admin_admin_mat = make_admin_admin_matrix(tower_tower_mat, tower_admin_mat,
                                              admin_tower_mat)
    print("Saving admin-to-admin matrix")
    mat_path = save_admin_admin(args.country_id, args.day_id, admin_admin_mat)
    print(f"Admin-to-Admin Matrix saved as {mat_path}")


if __name__ == "__main__":
    main()
