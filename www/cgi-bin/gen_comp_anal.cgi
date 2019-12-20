#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from Bio import SeqIO
import os, regex, yaml, cgi
import user_management as um

db = um.newDBConnection()

def process():
  form = cgi.FieldStorage()
  if not 'sid' in form or not strains in form:
    with open(os.environ['HPDB_BASE'] + '/scripts/template/invalid.html', 'r') as f:
      html = f.read()
    return html
  
  sid = form.getvalue('sid')
  username = um.sidtouser(db, sid)
  userid = um.usertoid(db, username)
  
  data = {}
  data['keys'] = ['Genome Length', 'GC%', 'Isolation Country', 'Genes', 'Proteins', 'PEG', 'tRNA', 'rRNA', 'Repeat Regions']
  data['strains'] = []
  data['strains'].append({'name': 'H. pylori 26695',
                          'Genome Length': 101,
                          'GC%': 39.5,
                          'Isolation Country': 'Vietnam ze bezt',
                          'Genes': 106,
                          'Proteins': 105,
                          'PEG': 104,
                          'tRNA': 103,
                          'rRNA': 102,
                          'Repeat Regions': 101})
  
  j2_env = jinja2.Environment(loader = jinja2.FileSystemLoader(os.environ['HPDB_BASE'] + '/scripts/template'), trim_blocks = True)
  j2_temp = j2_env.get_template('gen_comp_anal.html')
  return j2_temp.render(data).encode('utf8')

if __name__ == "__main__":
  print('Content-type:text/html')
  print('')
  print(process())
  db.close()