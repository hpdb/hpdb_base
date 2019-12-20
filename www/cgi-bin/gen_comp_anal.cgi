#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import os, csv, cgi, jinja2

def process():
  form = cgi.FieldStorage()
  if not 'strains' in form:
    with open(os.environ['HPDB_BASE'] + '/scripts/template/invalid.html', 'r') as f:
      html = f.read()
    return html
  
  strains = sid = form.getvalue('strains')
  if type(strains) == str:
    strains = strains.split(',')
  
  data = {}
  data['keys'] = ['Genome Length', 'GC%', 'Isolation Country', 'Proteins', 'PEG', 'tRNA', 'rRNA', 'Repeat Regions']
  data['strains'] = []
  
  with open(os.environ['HPDB_BASE'] + '/database/hpdb_data-master/strains_list.csv') as f:
    reader = csv.reader(f)
    for row in reader:
      if row[1] in strains:
        data['strains'].append({'name': row[0].replace('Helicobacter pylori', 'H. pylori'),
                                'Genome Length': row[11],
                                'GC%': row[10],
                                'Isolation Country': row[13],
                                'Proteins': row[12],
                                'PEG': row[5],
                                'tRNA': row[8],
                                'rRNA': row[7],
                                'Repeat Regions': row[6]})
  
  j2_env = jinja2.Environment(loader = jinja2.FileSystemLoader(os.environ['HPDB_BASE'] + '/scripts/template'), trim_blocks = True)
  j2_temp = j2_env.get_template('gen_comp_anal.html')
  return j2_temp.render(data).encode('utf8')

if __name__ == "__main__":
  print('Content-type:text/html')
  print('')
  print(process())