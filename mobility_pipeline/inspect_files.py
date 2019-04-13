#!/usr/bin/env python3

"""Script for JSON file inspection to determine if it is shape file or Voronoi

"""

import json


COLOMBIA_STATS = 'date/mpio-hdi-pop-threats-violence-zika-hdi_estimated.json'


if __name__ == '__main__':
    # pragma pylint: disable=invalid-name
    with open(COLOMBIA_STATS, 'r') as f:
        data = json.loads(f.read())
    features = data['features']
    found = False
    count = 0
    for f1 in features:
        for f2 in features:
            if f1['properties']['NOMBRE_M'] == f2['properties']['NOMBRE_M'] \
                    and f1['properties']['NOMBRE_D'] == \
                    f2['properties']['NOMBRE_D'] and f1 != f2:
                count += 1
                if not found:
                    print('MATCH FOUND')
                    print(f1)
                    print('-----------')
                    print(f2)
                    found = True
    print('Duplicates Found: ', count / 2)
