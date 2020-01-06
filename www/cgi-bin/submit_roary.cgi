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

def main():
  form = cgi.FieldStorage()
  if (not 'gbkfile' in form and not 'gbkfileloc' in form) or (not 'sid' in form) or (not 'projname' in form) or (not 'minidentity' in form):
    print('Content-Type:text/html')
    print('')
    with open(os.environ['HPDB_BASE'] + '/scripts/template/invalid.html', 'r') as f:
      print(f.read())
    return
  
  sid = form.getvalue('sid')
  username = um.sidtouser(db, sid)
  userid = um.usertoid(db, username)
  projname = form.getvalue('projname')
  minidentity = form.getvalue('minidentity')
  
  cnt = 0
  if 'gbkfile' in form:
    filefield = form['gbkfile']
    if not isinstance(filefield, list):
      filefield = [filefield]
    for upfile in filefield:
      if upfile.filename != '':
        cnt += 1
  if 'gbkfileloc' in form:
    gbkfileloc = um.getUserDir(userid) + form.getvalue('gbkfileloc')
    if os.path.isfile(gbkfileloc):
      cnt += 1
  
  if cnt < 2:
    print('Content-Type:text/html')
    print('')
    with open(os.environ['HPDB_BASE'] + '/scripts/template/invalid.html', 'r') as f:
      print(f.read())
    return
  
  jobid = str(int(round(time.time() * 1000)))
  
  dirpath = um.getUserProjectDir(userid) + jobid
  inputdir = dirpath + '/input'
  utils.mkdir(dirpath)
  utils.mkdir(inputdir)
  os.chdir(dirpath)
  
  cnt = 0
  
  if 'gbkfile' in form:
    filefield = form['gbkfile']
    if not isinstance(filefield, list):
      filefield = [filefield]
    for upfile in filefield:
      if upfile.filename:
        with open('input/' + os.path.splitext(upfile.filename)[0] + '.gbk', 'wb') as f:
          f.write(upfile.file.read())
  
  if 'gbkfileloc' in form:
    gbkfileloc = um.getUserDir(userid) + form.getvalue('gbkfileloc')
    if os.path.isfile(gbkfileloc):
      copyfile(gbkfileloc, 'input/' + os.path.splitext(os.path.basename(gbkfileloc))[0] + '.gbk')
  
  configs = {}
  configs['jobtype'] = 'roary'
  configs['jobid'] = jobid
  configs['daysubmit'] = time.strftime("%d-%m-%Y")
  configs['projname'] = projname
  configs['userid'] = userid
  configs['username'] = username
  configs['dirpath'] = dirpath
  configs['filename'] = ''
  configs['minidentity'] = minidentity

  with open('configs.yaml', 'w') as f:
    yaml.dump(configs, f)
  
  with open(os.environ['HPDB_BASE'] + '/queue/' + jobid, 'w') as f:
    f.write(dirpath)
  
  with open('queued', 'w') as f:
    f.write(dirpath)
  
  um.addproject(db, userid, username, jobid)
  
  print('Content-Type:text/plain')
  print('')
  print('Done!')

if __name__ == "__main__":
  main()
  db.close()