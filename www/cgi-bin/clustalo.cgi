#!/usr/bin/env python

from __future__ import division
import cgi
import json
import requests
import subprocess
import os, tempfile, shutil

def getPredictResult(id):
    return requests.get('http://www.mgc.ac.cn/cgi-bin/VFs/v5/v5/v5_predictJsondata.pl?ID={}'.format(id)).text

def findPredictionIndex(raw):
    region = raw.index('renderPredictedGene')
    start = raw.index('"dataIndex":"', region - 200) + len('"dataIndex":"')
    end = raw.index('",', start)
    return raw[start:end]

def findGeneID(raw, gene, ind):
    region = raw.index('"related_genes":"<i>{}</i>"'.format(gene))
    start = raw.index('{', region - 200)
    end = raw.index('}', start) + 1
    return json.loads(raw[start:end])[ind].split(',')

def downloadGene(id):
    response = requests.get('http://www.mgc.ac.cn/cgi-bin/VFs/v5/v5/v5_predictGeneWin.pl?VFGID={}&folder={}'.format(*id))
    raw = response.text
    
    start_dna = raw.index('<input type="hidden" name="seq" value="') + len('<input type="hidden" name="seq" value="')
    end_dna = raw.index('" />', start_dna)
    
    start_pro = raw.index('<input type="hidden" name="seq" value="', end_dna) + len('<input type="hidden" name="seq" value="')
    end_pro = raw.index('" />', start_pro)
    return [raw[start_dna:end_dna], raw[start_pro:end_pro]]

def exe(command):
    try:
        result = subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError as exc:
        result = exc.output
    return result

def main():
    form = cgi.FieldStorage()
    jobs = form.getvalue('jobs').splitlines()

    dirpath = tempfile.mkdtemp()
    os.chdir(dirpath)
    
    cag = open("hp-cag.fsa", "w")
    vac = open("hp-vac.fsa", "w")
    
    for job in jobs:
        job = job.split(',')
        
        raw = getPredictResult(job[0])
        if raw == '0' or raw == '1' or raw == '2':
            continue
        
        ind = findPredictionIndex(raw)
        cagaid = findGeneID(raw, 'cagA', ind)
        vacaid = findGeneID(raw, 'vacA', ind)
        
        caga = downloadGene(cagaid)
        cag.write('>' + job[1] +'\n')
        cag.write(caga[1] + '\n')
        
        vaca = downloadGene(vacaid)
        vac.write('>' + job[1] + '\n')
        vac.write(vaca[1] + '\n')
    
    cag.close()
    vac.close()
    
    print('Access-Control-Allow-Origin: *')
    print('Content-Type:text/plain')
    print('')
    print(exe('clustalo -i hp-cag.fsa --outfmt=clu --resno'))
    print(exe('clustalo -i hp-vac.fsa --outfmt=clu --resno'))

    shutil.rmtree(dirpath)

if __name__ == "__main__":
    main()