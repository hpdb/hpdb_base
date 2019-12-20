#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Bio import SeqIO
import os, csv, cgi, jinja2, yaml
import RAST_sdk as rast
import user_management as um

db = um.newDBConnection()

def calcGenLen(fasta):
  res = 0
  with open(fasta) as f:
    for rec in SeqIO.parse(f, 'fasta'):
      res += len(rec)
  return res

def process():
  form = cgi.FieldStorage()
  if not 'strains' in form and not 'jobs' in form:
    with open(os.environ['HPDB_BASE'] + '/scripts/template/invalid.html', 'r') as f:
      html = f.read()
    return html
  
  data = {}
  data['keys'] = ['Genome Length', 'GC%', 'Isolation Country', 'Proteins', 'PEG', 'tRNA', 'rRNA', 'Repeat Regions']
  data['strains'] = []
  
  if 'strains' in form:
    strains = form.getvalue('strains')
    if type(strains) == str:
      strains = strains.split(',')
    
    with open(os.environ['HPDB_BASE'] + '/database/hpdb_data-master/strains_list.csv') as f:
      reader = csv.reader(f)
      for row in reader:
        if row[1] in strains:
          data['strains'].append({'name': row[0].replace('Helicobacter pylori', 'H. pylori'),
                                  'Genome Length': row[11],
                                  'GC%': row[10],
                                  'Isolation Country': 'N/A' if row[13] == '' else row[13],
                                  'Proteins': row[12],
                                  'PEG': row[5],
                                  'tRNA': row[8],
                                  'rRNA': row[9],
                                  'Repeat Regions': row[6]})
  
  if 'jobs' in form and 'sid' in form:
    sid = form.getvalue('sid')
    username = um.sidtouser(db, sid)
    userid = um.usertoid(db, username)
    data_dir = um.getUserProjectDir(userid)
    jobs = form.getvalue('jobs').splitlines()
    
    for job in jobs:
      job = job.split(',')
      if not os.path.isfile(data_dir + job[1] + '/queued') and not os.path.isfile(data_dir + job[1] + '/running'):
        with open(data_dir + job[1] + '/configs.yaml') as f:
          configs = yaml.full_load(f)
        
        if configs['jobtype'] == 'rast':
          peg, repeat, rna, tRNA, rRNA = rast.parse_TSV(data_dir + job[1] + '/' + configs['rast_genome_id'] + '.txt')
          data['strains'].append({'name': job[0],
                                  'Genome Length': calcGenLen(data_dir + job[1] + '/input.fasta'),
                                  'GC%': 'N/A',
                                  'Isolation Country': 'N/A',
                                  'Proteins': 'N/A',
                                  'PEG': len(peg),
                                  'tRNA': len(tRNA),
                                  'rRNA': len(rRNA),
                                  'Repeat Regions': len(repeat)})

  j2_env = jinja2.Environment(loader = jinja2.FileSystemLoader(os.environ['HPDB_BASE'] + '/scripts/template'), trim_blocks = True)
  j2_temp = j2_env.get_template('gen_comp_anal.html')
  return j2_temp.render(data).encode('utf8')

if __name__ == "__main__":
  print('Content-type:text/html')
  print('')
  print(process())
  db.close()