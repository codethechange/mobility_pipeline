"""Script that checks the validity of data files
"""

import csv
from mobility_pipeline.data_interface import TOWERS_PATH, MOBILITY_PATH, \
    load_voronoi_cells, load_towers, VORONOI_PATH, COUNTRY_ID
from mobility_pipeline.lib.validate import validate_mobility, validate_admins, \
    validate_voronoi, validate_tower_cells_aligned, \
    validate_tower_index_name_aligned


def validate_data_files() -> bool:
    # pylint: disable=too-many-return-statements
    # pylint: disable=too-many-branches
    """Check the validity of data files

    Note that these checks are computationally intensive, so they probably
    should not be included in an automated pipeline. Rather, they are for manual
    use.

    Data files validated:

    * Towers file at :py:const:`mobility_pipeline.data_interface.TOWERS_PATH`
    * Voronoi file at :py:const:`mobility_pipeline.data_interface.VORONOI_PATH`
    * Mobility file at
      :py:const:`mobility_pipeline.data_interface.MOBILITY_PATH`

    Returns:
        ``True`` if all files are valid, ``False`` otherwise.
    """

    # Load and validate towers
    f = None
    try:
        f = open(TOWERS_PATH, 'r')
        towers_csv = csv.reader(f)
    except (FileNotFoundError, IOError) as e:
        msg = repr(e)
        print(f'INVALID: error opening towers file at {TOWERS_PATH}: {msg}')
        return False
    else:
        print('SUCCESS: Towers file opened')
        align_error = validate_tower_index_name_aligned(towers_csv)
        if align_error:
            print(f'INVALID tower index alignment: {align_error}')
            return False
        print('SUCCESS: Tower indices aligned')
        towers = load_towers(TOWERS_PATH)
    finally:
        if f:
            f.close()

    # Load and validate Voronoi
    voronoi_errs = validate_voronoi(VORONOI_PATH)
    if voronoi_errs:
        print(f'INVALID Voronoi: {voronoi_errs}')
        return False
    print('SUCCESS: Voronoi valid')
    voronoi = load_voronoi_cells(VORONOI_PATH)

    # Check towers and Voronoi aligned
    tower_voronoi_align_err = validate_tower_cells_aligned(voronoi, towers)
    if tower_voronoi_align_err:
        print(f'INVALID tower-Voronoi alignment: {tower_voronoi_align_err}')
        return False
    print('SUCCESS: Tower and Voronoi indices aligned')

    # Validate mobility data
    try:
        f = open(MOBILITY_PATH, 'r')
        mobility_csv = csv.reader(f)
    except (FileNotFoundError, IOError) as e:
        msg = repr(e)
        print(f'INVALID: error opening mobility file at {MOBILITY_PATH}: {msg}')
        return False
    else:
        print('SUCCESS: Mobility data loaded')
        mobility_err = validate_mobility(list(mobility_csv)[1:])
        if mobility_err:
            print(f'INVALID mobility data: {mobility_err}')
            return False
        print('SUCCESS: Mobility data valid')
    finally:
        if f:
            f.close()

    # Validate Admins
    admin_errs = validate_admins(COUNTRY_ID)
    if admin_errs:
        print(f'INVALID Admins: {admin_errs}')
        return False
    print('SUCCESS: Admins valid')
    return True


if __name__ == '__main__':
    if validate_data_files():
        exit(0)
    else:
        exit(1)
