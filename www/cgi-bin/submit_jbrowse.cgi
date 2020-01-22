#!/usr/bin/env python

import cgi
import os
import time
import yaml
import utils
import time
from subprocess import call
import user_management as um
from shutil import copyfile

db = um.newDBConnection()

def process():
  start_time = time.time()
  
  form = cgi.FieldStorage()
  if not 'sid' in form:
    return 'You are not logged in!'
  if not 'projname' in form:
    return 'Please specify project name!'
  if (not 'seqfile' in form and not 'seqfileloc' in form):
    return 'No sequence file found'
  
  sid = form.getvalue('sid')
  username = um.sidtouser(db, sid)
  userid = um.usertoid(db, username)
  projname = form.getvalue('projname')
  jobid = str(int(round(time.time() * 1000)))
  
  dirpath = um.getUserProjectDir(userid) + jobid
  utils.mkdir(dirpath)
  os.chdir(dirpath)
  
  ok = False
  if 'seqfile' in form:
    upfile = form['seqfile']
    if upfile.filename:
      ok = True
      filename = upfile.filename
      ext = os.path.splitext(filename)[1][1:]
      with open('input.' + ext, 'wb') as f:
        f.write(upfile.file.read())
  if not ok and 'seqfileloc' in form:
    seqfileloc = um.getUserDir(userid) + form.getvalue('seqfileloc')
    if os.path.isfile(seqfileloc):
      ok = True
      filename = os.path.basename(seqfileloc)
      ext = os.path.splitext(filename)[1][1:]
      copyfile(seqfileloc, 'input.' + ext)
  
  if not ok:
    return 'No sequence file found'
  
  configs = {}
  configs['jobtype'] = 'jbrowse'
  configs['jobid'] = jobid
  configs['daysubmit'] = time.strftime("%d-%m-%Y")
  configs['projname'] = projname
  configs['userid'] = userid
  configs['username'] = username
  configs['dirpath'] = dirpath
  configs['filename'] = filename
  
  # prepare JBrowse data
  if ext in ['.fasta', '.fa', '.fna', '.ffn', '.faa', '.frn']:
    call('/usr/bin/perl ' + os.environ['HPDB_BASE'] + '/www/JBrowse/bin/prepare-refseqs.pl --fasta input.%s --out JBrowse >/dev/null 2>&1' % ext, shell = True)
  elif ext == 'gbk':
    call('bp_genbank2gff3 input.gbk >/dev/null 2>&1', shell = True)
    call('/usr/bin/perl ' + os.environ['HPDB_BASE'] + '/scripts/gbk2fasta.pl input.gbk input.fasta >/dev/null 2>&1', shell = True)
    call('/usr/bin/perl ' + os.environ['HPDB_BASE'] + '/www/JBrowse/bin/prepare-refseqs.pl --fasta input.fasta --out JBrowse >/dev/null 2>&1', shell = True)
    call('/usr/bin/perl ' + os.environ['HPDB_BASE'] + '/www/JBrowse/bin/flatfile-to-json.pl --gff input.gbk.gff --trackLabel gff --trackType CanvasFeatures --out JBrowse >/dev/null 2>&1', shell = True)
  
  configs['exec_time'] = '%.2f' % (time.time() - start_time)
  
  with open('configs.yaml', 'w') as f:
    yaml.dump(configs, f)
  
  um.addproject(db, userid, username, jobid)
  
  return 'Done!'

if __name__ == "__main__":
  print('Content-Type:text/plain')
  print('')
  print(process())
  db.close()