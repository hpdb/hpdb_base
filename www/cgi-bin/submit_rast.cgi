#!/usr/bin/env python

import cgi
import os
import time
import yaml
import utils
import user_management as um
import RAST_sdk as rast
from shutil import copyfile
from ConfigParser import ConfigParser

db = um.newDBConnection()    

def process():
    form = cgi.FieldStorage()
    if not 'sid' in form:
        return 'You are not logged in!'
    if not 'projname' in form:
        return 'Please specify project name!'
    if not 'strain' in form:
        return 'Please specify strain!'
    if (not 'seqfile' in form and not 'seqfileloc' in form):
        return 'No sequence file found'
    
    sid = form.getvalue('sid')
    username = um.sidtouser(db, sid)
    userid = um.usertoid(db, username)
    projname = form.getvalue('projname')
    strain = form.getvalue('strain')
    jobid = str(int(round(time.time() * 1000)))
    
    dirpath = um.getUserProjectDir(userid) + jobid
    utils.mkdir(dirpath)
    os.chdir(dirpath)
    
    ok = False
    if 'seqfile' in form:
        upfile = form['seqfile']
        if upfile.filename != '':
            ok = True
            with open('input.fasta', 'wb') as f:
                f.write(upfile.file.read())
    if not ok and 'seqfileloc' in form:
        seqfileloc = um.getUserDir(userid) + form.getvalue('seqfileloc')
        if os.path.isfile(seqfileloc):
            ok = True
            copyfile(seqfileloc, 'input.fasta')
    
    if not ok:
        return 'No sequence file found'
    
    config = ConfigParser()
    config.read(os.environ['HPDB_BASE'] + '/sys.properties')
    rast_username = config._sections['RAST Account']['username']
    rast_password = config._sections['RAST Account']['password']

    configs = {}
    configs['jobtype'] = 'rast'
    configs['jobid'] = jobid
    configs['daysubmit'] = time.strftime("%d-%m-%Y")
    configs['projname'] = projname
    configs['userid'] = userid
    configs['username'] = username
    configs['dirpath'] = dirpath
    configs['filename'] = ''
    configs['strain'] = strain
    configs['rast_id'] = rast.submit_RAST_job(rast_username, rast_password, 'input.fasta', configs['strain'])
    #configs['exec_time'] = '%.2f' % (time.time() - start_time)
    
    with open('configs.yaml', 'w') as f:
        yaml.dump(configs, f)
    
    with open(os.environ['HPDB_BASE'] + '/queue/external/' + jobid, 'w') as f:
        f.write(dirpath)
    
    with open('queued', 'w') as f:
        f.write(dirpath)
    
    with open('running', 'w') as f:
        f.write('dumb file')
    
    um.addproject(db, userid, username, jobid)
    
    return 'Done!'

if __name__ == "__main__":
    print('Content-Type:text/plain')
    print('')
    print(process())
    db.close()