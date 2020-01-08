#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from Bio import SeqIO
import os, regex, yaml, cgi
import user_management as um

db = um.newDBConnection()

def main():
  form = cgi.FieldStorage()
  if not 'sid' in form:
    print('Content-Type:text/html')
    print('')
    with open(os.environ['HPDB_BASE'] + '/scripts/template/invalid.html', 'r') as f:
      print(f.read())
    return
  
  sid = form.getvalue('sid')
  username = um.sidtouser(db, sid)
  userid = um.usertoid(db, username)
  start = form.getvalue('start')
  end = form.getvalue('end')
  
  data_dir = um.getUserProjectDir(userid)
  jobids = sorted(os.listdir(data_dir))
  
  print('Content-type:text/html')
  print('')
  print('<html>')
  print('<head>')
  print('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
  print('<title>HPDB - PTNK</title>')
  print('</head>')
  print('<body>')
  # begin the table
  print('<table border="1">')
  
  # column headers
  print('<tr>')
  print('<th>Filename</th>')
  print('<th>cagA</th>')
  print('<th>vacA</th>')
  print('<th>EPIYA</th>')
  print('<th>s1/s2</th>')
  print('<th>m1/m2</th>')
  print('</tr>')
  
  for id in jobids:
    if (start and int(id) < int(start)) or (end and int(id) > int(end)):
      continue
    if os.path.isfile(data_dir + id + '/running') or os.path.isfile(data_dir + id + '/error'):
      continue
    if not os.path.isfile(data_dir + id + '/configs.yaml'):
      continue
    
    with open(data_dir + id + '/configs.yaml') as f:
      configs = yaml.full_load(f)
    if not os.path.isfile(data_dir + id + '/queued') and configs['jobtype'] == 'caga/vaca':
      cols = []
      cols.append('<b><a href="/cgi-bin/user_getjobreport.cgi?jobid=%s&sid=%s">%s</a></b>' % (id, sid, os.path.basename(configs['filename'])))
      cols.append(u'có' if configs['found_caga'] else (u'đbmđ' if configs['mutant_caga'] else 'ko'))
      cols.append(u'có' if configs['found_vaca'] else (u'đbmđ' if configs['mutant_vaca'] else 'ko'))
      EPIYA = ''
      if configs['found_caga']:
        if configs['caga_analysis']['EPIYA-A']: EPIYA += 'A'
        if configs['caga_analysis']['EPIYA-B']: EPIYA += 'B'
        if configs['caga_analysis']['EPIYA-C']: EPIYA += 'C'
        if configs['caga_analysis']['EPIYA-CC']: EPIYA += 'C'
        if configs['caga_analysis']['EPIYA-D']: EPIYA += 'D'
      cols.append(EPIYA)
      cols.append(configs['vaca_analysis']['s1s2'])
      cols.append(configs['vaca_analysis']['m1m2'])
      
      print('<tr>')
      for col in cols:
        print('<td>%s</td>' % col)
      print('</tr>')
  
  # end the table
  print('</table>')
  print('</body>')
  print('</html>')

if __name__ == "__main__":
  main()
  db.close()