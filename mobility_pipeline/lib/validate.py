"""Functions for validating data file formats and contents

"""

from typing import List, Optional
from data_interface import TOWER_PREFIX


def all_numeric(string: str) -> bool:
    """Check that a string is composed entirely of digits

    Args:
        string: String to check

    Returns:
        True if and only if the string is composed entirely of digits
    """
    for c in string:
        if not c.isdigit():
            return False
    return True


def validate_mobility(raw: List[List[str]]) -> Optional[str]:
    # pylint: disable=too-many-return-statements
    """Checks that the text from a CSV file is in a valid format for mobility

    The text must consist of a list of rows, where each row is a list of exactly
    4 strings: a date (not checked), an origin tower, a destination tower, and
    a count.

    The origin and destination must be composed of digits following
    :py:const:`data_interface.TOWER_PREFIX`. The count must be composed entirely
    of digits and represent a non-negative integer.

    The origin and destination tower numeric portions must strictly increase in
    origin-major order.

    Args:
        raw: The text to check

    Returns:
        None if the input is valid, a string describing the error otherwise.
    """
    prev_ori = -1
    prev_dst = -1
    for line in raw:
        _, ori_str, dst_str, count_str = line
        ori_str = ori_str[len(TOWER_PREFIX):]
        dst_str = dst_str[len(TOWER_PREFIX):]
        if not all_numeric(ori_str):
            return "Line {} invalid because origin {} non-numeric".\
                format(line, ori_str)
        if not all_numeric(dst_str):
            return "Line {} invalid because destination {} non-numeric".\
                format(line, ori_str)
        if not all_numeric(count_str):
            return "Line {} invalid because count {} non-numeric".\
                format(line, count_str)
        ori = int(ori_str)
        dst = int(dst_str)
        count = int(count_str)
        if ori < prev_ori:
            return "Line {} invalid because previous origin was {}".\
                format(line, prev_ori)
        if ori > prev_ori:
            prev_ori = ori
            prev_dst = -1
        if dst <= prev_dst:
            return "Line {} invalid because previous destination was {}".\
                format(line, prev_dst)
        prev_dst = dst

        if count < 0:
            return "Line {} invalid because count is negative".format(count)
    return None


def validate_mobility_full(mobility: List[List[str]]) -> Optional[str]:
    """Check whether the mobility data file is correctly ordered and full

    The mobility data file is loaded from the file at path
    :py:func:`mobility_pipeline.data_interface.MOBILITY_PATH`. Correctly ordered
    means that the tower names' numeric portions strictly increase in
    origin-major order. Full means that there is a row for every combination of
    origin and destination tower.

    If this order were perfect, it would make forming the mobility matrix as
    easy as reshaping the last column. Unfortunately, this function showed that
    some coordinates are missing or out of order, so counts must be inserted
    manually.

    Args:
        mobility: List of mobility CSV data by applying ``list(csv.reader(f))``

    Returns:
        None if there is no error, otherwise a description of the error.
    """
    n_towers = int(mobility[-1][1][2:]) + 1
    i_row = 0

    for i_ori in range(n_towers):
        for i_dst in range(n_towers):
            _, ori, dst, _ = mobility[i_row]
            if ori != 'br{}'.format(i_ori) or dst != 'br{}'.format(i_dst):
                msg = 'INVALID: Row {} is {}, but we expected {}'.format(
                    i_row, mobility[i_row],
                    'date,br{},br{},count'.format(i_ori, i_dst)
                )
                return msg
            i_row += 1
    return None