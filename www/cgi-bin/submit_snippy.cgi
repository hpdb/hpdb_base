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

def newJob(type, projname, userid, username, upfile, form, seqfileloc = ''):
  jobid = str(int(round(time.time() * 1000)))
  dirpath = um.getUserProjectDir(userid) + jobid
  utils.mkdir(dirpath)
  os.chdir(dirpath)
  
  configs = {}
  configs['jobtype'] = 'snippy'
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
  
  ok = False
  if 'refseqfile' in form:
    upfile = form['refseqfile']
    if upfile.filename:
      ok = True
      with open('ref.fasta', 'wb') as f:
        f.write(upfile.file.read())
  if not ok and 'refseqfileloc' in form:
    refseqfileloc = um.getUserDir(userid) + form.getvalue('refseqfileloc')
    if os.path.isfile(refseqfileloc):
      ok = True
      copyfile(refseqfileloc, 'ref.fasta')
  
  if not ok:
    return
  
  with open('configs.yaml', 'w') as f:
    yaml.dump(configs, f)
  
  with open(os.environ['HPDB_BASE'] + '/queue/' + jobid, 'w') as f:
    f.write(dirpath)
  
  with open('queued', 'w') as f:
    f.write(dirpath)
  
  um.addproject(db, userid, username, jobid)

def main():
  form = cgi.FieldStorage()
  if (not 'seqfile' in form and not 'seqfileloc' in form) or (not 'refseqfile' in form and not 'refseqfileloc' in form) or (not 'sid' in form) or (not 'projname' in form):
    print('Content-Type:text/html')
    print('')
    with open(os.environ['HPDB_BASE'] + '/scripts/template/invalid.html', 'r') as f:
      print(f.read())
    return
  
  sid = form.getvalue('sid')
  username = um.sidtouser(db, sid)
  userid = um.usertoid(db, username)
  projname = form.getvalue('projname')
  jobid = str(int(round(time.time() * 1000)))
  
  dirpath = um.getUserProjectDir(userid) + jobid
  utils.mkdir(dirpath)
  os.chdir(dirpath)
  
  if 'seqfile' in form:
    filefield = form['seqfile']
    if not isinstance(filefield, list):
      filefield = [filefield]
    for upfile in filefield:
      if upfile.filename:
        newJob(1, projname, userid, username, upfile, form)
  
  if 'seqfileloc' in form:
    seqfileloc = um.getUserDir(userid) + form.getvalue('seqfileloc')
    if os.path.isfile(seqfileloc):
      newJob(2, projname, userid, username, '', form, seqfileloc)
  
  print('Content-Type:text/plain')
  print('')
  print('Done!')

if __name__ == "__main__":
  main()
  db.close()