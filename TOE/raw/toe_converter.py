import csv
import json
import sys
import math

file = sys.argv[1]
out = sys.argv[2]

data = []
PAMU = 0
UNIT = 1
TOE = 2
ATS = 3
BASE = 4

with open(file) as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for row in reader:
        if row[UNIT] in [0, '0', 'Sub-total']:
            continue
        if row[PAMU].startswith('OTHER UNIT'):
            row[PAMU] = 'Non-PA'
        try:
            data.append({'pamu': row[PAMU], 
                         'unit': row[UNIT], 
                         'toe': int(math.ceil(float(row[TOE] or 0))), 
                         'ats': int(row[ATS] or 0), 
                         'baseline': int(row[BASE] or 0)})
        except ValueError as e:
            print(f'{e}: toe: {row[TOE]}')


with open(out, 'w') as out_file:
    json.dump(data, out_file, indent=4)


print(f'Rows: {len(data)}')
print(f'Saved result to {out}')
