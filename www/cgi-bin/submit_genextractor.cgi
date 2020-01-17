#!/usr/bin/env python

import cgi
import os
import time
import yaml
import MySQLdb
import json
import user_management as um
import utils
from shutil import copyfile

db = um.newDBConnection()

def newJob(type, projname, userid, username, upfile, queryseq, seqfileloc = ''):
  jobid = str(int(round(time.time() * 1000)))
  dirpath = um.getUserProjectDir(userid) + jobid
  utils.mkdir(dirpath)
  os.chdir(dirpath)
  
  configs = {}
  configs['jobtype'] = 'gene extractor'
  configs['jobid'] = jobid
  configs['daysubmit'] = time.strftime("%d-%m-%Y")
  configs['projname'] = projname
  configs['userid'] = userid
  configs['username'] = username
  configs['dirpath'] = dirpath
  configs['filename'] = ''
  
  if type == 1:
    configs['filename'] = upfile.filename
    with open('input.fasta', 'wb') as f:
      f.write(upfile.file.read())
  else:
    configs['filename'] = os.path.basename(seqfileloc)
    copyfile(seqfileloc, 'input.fasta')
  
  with open('ref.fasta', 'w') as f:
    f.write(queryseq)
  
  with open('configs.yaml', 'w') as f:
    yaml.dump(configs, f)
  
  with open(os.environ['HPDB_BASE'] + '/queue/' + jobid, 'w') as f:
    f.write(dirpath)
  
  with open('queued', 'w') as f:
    f.write(dirpath)
  
  um.addproject(db, userid, username, jobid)

def main():
  form = cgi.FieldStorage()
  if (not 'seqfile' in form and not 'seqfileloc' in form) or (not 'queryseq' in form and not not 'queryseqfile' in form and not 'queryseqfileloc' in form) or (not 'sid' in form) or (not 'projname' in form):
    print('Content-Type:text/html')
    print('')
    with open(os.environ['HPDB_BASE'] + '/scripts/template/invalid.html', 'r') as f:
      print(f.read())
    return
  
  sid = form.getvalue('sid')
  username = um.sidtouser(db, sid)
  userid = um.usertoid(db, username)
  projname = form.getvalue('projname')
  queryseq = form.getvalue('queryseq')
  
  if queryseq == '':
    if 'queryseqfile' in form:
      upfile = form['queryseqfile']
      if upfile.filename:
        queryseq = upfile.file.read()
  
  if queryseq == '':
    if 'queryseqfileloc' in form:
      queryseqfileloc = um.getUserDir(userid) + form.getvalue('queryseqfileloc')
      if os.path.isfile(queryseqfileloc):
        with open(queryseqfileloc) as f:
          queryseq = f.read()
  
  if queryseq != '':
    if 'seqfile' in form:
      filefield = form['seqfile']
      if not isinstance(filefield, list):
        filefield = [filefield]
      for upfile in filefield:
        if upfile.filename:
          newJob(1, projname, userid, username, upfile, queryseq)
    
    if 'seqfileloc' in form:
      seqfileloc = um.getUserDir(userid) + form.getvalue('seqfileloc')
      if os.path.isfile(seqfileloc):
        newJob(2, projname, userid, username, '', queryseq, seqfileloc)
  
  print('Content-Type:text/plain')
  print('')
  print('Done!')

if __name__ == "__main__":
  main()
  db.close()