#!/usr/bin/env python
import os, csv, json

if __name__ == "__main__":
  strains = []
  with open(os.environ['HPDB_BASE'] + '/database/hpdb_data-master/strains_list.csv') as f:
    reader = csv.reader(f)
    for row in reader:
      if row[0] != 'Name':
        strains.append({'name': row[0], 'ncbi_id': row[1]})
  
  print('Content-Type:text/json')
  print('')
  print(json.dumps(strains))