#!/usr/bin/env python

import cgi
import os
import time
import yaml
import MySQLdb
import json
import user_management as um
from shutil import copyfile

db = um.newDBConnection()

def main():
    form = cgi.FieldStorage()
    if (not 'seqfile' in form and not 'sequence' in form) or (not 'sid' in form) or (not 'projname' in form):
        print('Content-Type:text/html')
        print('')
        with open(os.environ['HPDB_BASE'] + '/scripts/template/invalid.html', 'r') as f:
            print(f.read())
        return
    
    sid = form.getvalue('sid')
    username = um.sidtouser(db, sid)
    userid = um.usertoid(db, username)
    jobid = str(int(round(time.time() * 1000)))
    
    dirpath = um.getUserProjectDir(userid) + configs['jobid']
    os.mkdir(dirpath)
    os.chdir(dirpath)
    
    configs = {}
    configs['jobtype'] = 'clustalo'
    configs['jobid'] = jobid
    configs['daysubmit'] = time.strftime("%d-%m-%Y")
    configs['projname'] = form.getvalue('projname')
    configs['userid'] = userid
    configs['username'] = username
    configs['dirpath'] = dirpath
    configs['filename'] = ''
    configs['stype'] = form.getvalue('stype')
    configs['outfmt'] = form.getvalue('outfmt')
    
    # FIX-ME: check if seq file is valid
    with open('input.fasta', 'wb') as f:
        if form.getvalue('sequence') != '':
            f.write(form.getvalue('sequence'))
        else:
            f.write(form['seqfile'].file.read())
    
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