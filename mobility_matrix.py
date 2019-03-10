#!/usr/bin/env python3

import json
import numpy as np
from os import path
from typing import Dict


def make_admin_dict(admin_json: json) -> Dict[str, int]:
    admins = admin_json['features']
    admins_dict = {}
    for i, admin in enumerate(admins):
        admins_dict[admin['properties']['admin_id']] = i
    return admins_dict


def json_to_matrix(pairs: json, admins: Dict[str, int]) -> np.ndarray:
    # Assume no duplication of admin_id values and no duplicate mobility values
    n_admins = len(admins)
    mat = np.zeros((n_admins, n_admins))
    for pair in pairs:
        origin_i = admins[pair['id_origin']]
        destination_i = admins[pair['id_destination']]
        mat[origin_i][destination_i]: int = pair['people']
    return mat


if __name__ == '__main__':
    admin_path = 'mpio-hdi-pop-threats-violence-zika-hdi_estimated.json'
    mobility_path = path.join('Colombia-base-line-mobility',
                              'movement-day0.json')

    with open(admin_path, 'r') as admin_f:
        admin_json = json.load(admin_f)
    with open(mobility_path, 'r') as mobility_f:
        mobility_json = json.load(mobility_f)

    admin_dict = make_admin_dict(admin_json)
    matrix = json_to_matrix(mobility_json, admin_dict)
