#!/usr/bin/env python
import os, csv, json

if __name__ == "__main__":
  strains = []
  with open(os.environ['HPDB_BASE'] + '/database/hpdb_data-master/strains_list.csv') as f:
    reader = csv.reader(f)
    for row in reader:
      if row[0] != 'Name':
        cur = {}
        cur['id'] = row[1]
        cur['title'] = row[0]
        cur['subs'] = []
        cur['subs'].append({'id': 10 * int(row[1]) + 1, 'title': 'Genome file (FASTA)'})
        cur['subs'].append({'id': 10 * int(row[1]) + 2, 'title': 'GenBank file (GBK)'})
  
  print('Content-Type:text/json')
  print('')
  print(json.dumps(strains))