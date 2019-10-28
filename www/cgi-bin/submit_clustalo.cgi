#!/usr/bin/env python

import cgi
import os
import time
import yaml

def main():
    form = cgi.FieldStorage()
    if not 'seqfile' in form:
        print('Content-Type:text/html')
        print('')
        with open(os.environ['HPDB_BASE'] + '/scripts/template/invalid.html', 'r') as f:
            print(f.read())
        return
    
    filefield = form['seqfile']
    if not isinstance(filefield, list):
        filefield = [filefield]
    
    for upfile in filefield:
        configs = {}
        configs['filename'] = upfile.filename
        configs['jobtype'] = 'clustalo'
        configs['job_id'] = str(int(round(time.time() * 1000)))
        configs['find_amr'] = (form.getvalue('find_amr') == 'on')
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
        
        dirpath = os.environ['HPDB_BASE'] + '/data/project/' + configs['job_id']
        os.mkdir(dirpath)
        os.chdir(dirpath)
        
        with open('input.fasta', 'wb') as f:
            f.write(upfile.file.read())
        
        with open('configs.yaml', 'w') as f:
            yaml.dump(configs, f)
        
        with open(os.environ['HPDB_BASE'] + '/queue/' + configs['job_id'], 'w') as f:
            f.write('just another dumb text')
        
        with open('queued', 'w') as f:
            f.write('yet another dumb text')
        
    print('Access-Control-Allow-Origin: *')
    print('Content-Type:text/plain')
    print('')
    print('Done!')

if __name__ == "__main__":
    main()