#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from Bio import SeqIO
import os, yaml, cgi, jinja2
import user_management as um

db = um.newDBConnection()

def process():
  form = cgi.FieldStorage()
  if not 'sid' in form or not 'strains' in form:
    with open(os.environ['HPDB_BASE'] + '/scripts/template/invalid.html', 'r') as f:
      html = f.read()
    return html
  
  sid = form.getvalue('sid')
  username = um.sidtouser(db, sid)
  userid = um.usertoid(db, username)
  strains = sid = form.getvalue('strains').split(',')
  
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
  db.close()