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
    if (not 'queryseq' in form and not 'queryseqfile' in form) or (not 'subseq' in form and not 'subseqfile' in form) or (not 'blastype' in form) or (not 'sid' in form) or (not 'projname' in form):
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
    
    configs = {}
    configs['jobtype'] = 'blast'
    configs['jobid'] = jobid
    configs['daysubmit'] = time.strftime("%d-%m-%Y")
    configs['projname'] = projname
    configs['userid'] = userid
    configs['username'] = username
    configs['dirpath'] = dirpath
    configs['filename'] = ''
    configs['blastype'] = form.getvalue('blastype')
    
    # FIX-ME: check if seq file is valid
    with open('query.fasta', 'wb') as f:
        if form.getvalue('queryseq') != '':
            f.write(form.getvalue('queryseq'))
        else:
            f.write(form['queryseqfile'].file.read())
    with open('subject.fasta', 'wb') as f:
        if form.getvalue('subseq') != '':
            f.write(form.getvalue('subseq'))
        else:
            f.write(form['subseqfile'].file.read())
    
    with open('configs.yaml', 'w') as f:
        yaml.dump(configs, f)
    
    with open(os.environ['HPDB_BASE'] + '/queue/' + jobid, 'w') as f:
        f.write(dirpath)
    
    with open('queued', 'w') as f:
        f.write(dirpath)
    
    um.addproject(db, userid, username, jobid)
    
    print('Access-Control-Allow-Origin: *')
    print('Content-Type:text/plain')
    print('')
    print('Done!')

if __name__ == "__main__":
    main()
    db.close()