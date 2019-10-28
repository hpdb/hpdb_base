#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from Bio import SeqIO
import cgi, subprocess
import os, tempfile, shutil, yaml
import user_management as um

db = um.newDBConnection()

def run(command):
    try:
        result = subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError as exc:
        result = exc.output
    return result

def main():
    form = cgi.FieldStorage()
    if (not 'jobs' in form) or (not 'sid' in form):
        print('Access-Control-Allow-Origin: *')
        print('Content-Type:text/plain')
        print('')
        print('Invalid')
    
    jobs = form.getvalue('jobs').splitlines()
    align_caga = (form.getvalue('caga') == 'on')
    align_vaca = (form.getvalue('vaca') == 'on')
    
    sid = form.getvalue('sid')
    username = um.sidtouser(db, sid)
    userid = um.usertoid(db, username)
    data_dir = um.getUserProjectDir(userid)
    
    dirpath = tempfile.mkdtemp()
    os.chdir(dirpath)
    
    cag = open("hp-cag.fsa", "w")
    vac = open("hp-vac.fsa", "w")
    cnt_cag = 0
    cnt_vac = 0
    
    for job in jobs:
        job = job.split(',')
        if not os.path.isfile(data_dir + job[1] + '/queued'):
            with open(data_dir + job[1] + '/configs.yaml') as f:
                configs = yaml.full_load(f)
        
        if configs['found_caga']:
            cag.write('>' + job[0] +'\n')
            cag.write(configs['caga_prot']['raw'] + '\n')
            cnt_cag += 1
        if configs['found_vaca']:
            vac.write('>' + job[0] +'\n')
            vac.write(configs['vaca_prot']['raw'] + '\n')
            cnt_vac += 1
    
    cag.close()
    vac.close()
    
    print('Access-Control-Allow-Origin: *')
    print('Content-Type:text/plain')
    print('')
    if align_caga and cnt_cag > 1: print(run('clustalo -i hp-cag.fsa --outfmt=clu --resno'))
    elif align_caga: print(u'Không đủ cagA')
    if align_vaca and cnt_vac > 1: print(run('clustalo -i hp-vac.fsa --outfmt=clu --resno'))
    elif align_vaca: print(u'Không đủ vacA')

    shutil.rmtree(dirpath)

if __name__ == "__main__":
    main()
    db.close()