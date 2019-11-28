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

def newJob(type, projname, userid, username, find_amr, upfile, seqfileloc = ''):
    jobid = str(int(round(time.time() * 1000)))
    dirpath = um.getUserProjectDir(userid) + jobid
    os.mkdir(dirpath)
    os.chdir(dirpath)
    
    configs = {}
    configs['jobtype'] = 'hpdb'
    configs['jobid'] = jobid
    configs['daysubmit'] = time.strftime("%d-%m-%Y")
    configs['projname'] = projname
    configs['userid'] = userid
    configs['username'] = username
    configs['dirpath'] = dirpath
    configs['filename'] = ''
    configs['find_amr'] = find_amr
    configs['found_caga'] = False
    configs['found_vaca'] = False
    configs['mutant_caga'] = False
    configs['mutant_vaca'] = False
    configs['caga_nu'] = {}
    configs['caga_prot'] = {}
    configs['vaca_nu'] = {}
    configs['vaca_prot'] = {}
    configs['caga_analysis'] = {'EPIYA-A': False, 'EPIYA-B': False, 'EPIYA-C': False, 'EPIYA-D': False}
    configs['vaca_analysis'] = {'s1s2': '', 'm1m2': ''}
    configs['amr_analysis'] = {}
    
    
    if type == 1:
        configs['filename'] = upfile.filename
        with open('input.fasta', 'wb') as f:
            f.write(upfile.file.read())
    else:
        configs['filename'] = os.path.basename(seqfileloc)
        copyfile(seqfileloc, 'input.fasta')
    
    with open('configs.yaml', 'w') as f:
        yaml.dump(configs, f)
    
    with open(os.environ['HPDB_BASE'] + '/queue/' + jobid, 'w') as f:
        f.write(dirpath)
    
    with open('queued', 'w') as f:
        f.write(dirpath)
    
    um.addproject(db, userid, username, jobid)

def main():
    form = cgi.FieldStorage()
    if (not 'seqfile' in form and not 'seqfileloc' in form) or (not 'sid' in form) or (not 'projname' in form):
        print('Content-Type:text/html')
        print('')
        with open(os.environ['HPDB_BASE'] + '/scripts/template/invalid.html', 'r') as f:
            print(f.read())
        return
    
    sid = form.getvalue('sid')
    username = um.sidtouser(db, sid)
    userid = um.usertoid(db, username)
    projname = form.getvalue('projname')
    find_amr = (form.getvalue('find_amr') == 'on')
    
    if 'seqfile' in form:
        filefield = form['seqfile']
        if not isinstance(filefield, list):
            filefield = [filefield]
        for upfile in filefield:
            if upfile.filename != '':
                newJob(1, projname, userid, username, find_amr, upfile)
    
    if 'seqfileloc' in form:
        seqfileloc = um.getUserDir(userid) + form.getvalue('seqfileloc')
        if os.path.isfile(seqfileloc):
            newJob(2, projname, userid, username, find_amr, '', seqfileloc)
    
    print('Access-Control-Allow-Origin: *')
    print('Content-Type:text/plain')
    print('')
    print('Done!')

if __name__ == "__main__":
    main()
    db.close()