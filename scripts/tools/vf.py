#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from subprocess import call
from Bio import SeqIO
import os
import time
import jinja2
import yaml
import commands
from ref_AMR import AMR
import utils

def run(configs):
    start_time = time.time()

    # ----- Run tools -----
    utils.runprodigal('input.fasta', 'prot.fasta', 'nu.fasta')
    caga_ids = utils.runblast('blastp', os.environ['HPDB_BASE'] + '/genome/j99_caga.fasta', 'prot.fasta', '0.0001', '10 sseqid').splitlines()
    vaca_ids = utils.runblast('blastp', os.environ['HPDB_BASE'] + '/genome/j99_vaca.fasta', 'prot.fasta', '0.0001', '10 sseqid').splitlines()
    
    # ----- Find virulence factors -----
    prot_dict = SeqIO.index('prot.fasta', 'fasta')
    nu_dict = SeqIO.index('nu.fasta', 'fasta')
    
    for id in caga_ids:
        caga_prot = str(prot_dict[id].seq).rstrip('*')
        caga_pos = prot_dict[id].description.split('#')
        caga_nu = str(nu_dict[id].seq).strip('*')
        if 'EPIYA' in caga_prot or 'EPIYT' in caga_prot:
            if len(caga_prot) > 800: configs['found_caga'] = True
            else: configs['mutant_caga'] = True
            break
    
    for id in vaca_ids:
        vaca_prot = str(prot_dict[id].seq).rstrip('*')
        vaca_pos = prot_dict[id].description.split('#')
        vaca_nu = str(nu_dict[id].seq).strip('*')
        if utils.fuzzyFind(vaca_prot, 'MELQQTHRKINRPLVSLALVG')[0] >= 0.8:
            if len(vaca_prot) > 800: configs['found_vaca'] = True
            else: configs['mutant_vaca'] = True
            break
    
    prot_dict.close()
    nu_dict.close()
    
    # ----- Analyze data -----
    # cagA
    if configs['found_caga']:
        configs['caga_analysis'] = utils.analyzecagA(caga_prot)
        configs['caga_nu'] = {'name': 'cagA DNA', \
                              'raw': caga_nu, \
                              'len': len(caga_nu), \
                              'start_pos': caga_pos[1].strip(), \
                              'end_pos': caga_pos[2].strip()}
        configs['caga_prot'] = {'name': 'cagA Protein', \
                                'raw': caga_prot, \
                                'len': len(caga_prot), \
                                'start_pos': caga_pos[1].strip(), \
                                'end_pos': caga_pos[2].strip()}
    
    # vacA
    if configs['found_vaca']:
        configs['vaca_analysis'] = utils.analyzevacA(vaca_prot)
        configs['vaca_nu'] = {'name': 'vacA DNA', \
                              'raw': vaca_nu, \
                              'len': len(vaca_nu), \
                              'start_pos': vaca_pos[1].strip(), \
                              'end_pos': vaca_pos[2].strip()}
        configs['vaca_prot'] = {'name': 'vacA Protein', \
                                'raw': vaca_prot, \
                                'len': len(vaca_prot), \
                                'start_pos': vaca_pos[1].strip(), \
                                'end_pos': vaca_pos[2].strip()}
        
    configs['exec_time'] = '%.2f' % (time.time() - start_time)
    
    # ----- Output HTML -----
    j2_env = jinja2.Environment(loader = jinja2.FileSystemLoader(os.environ['HPDB_BASE'] + '/scripts/template'), trim_blocks = True)
    j2_temp = j2_env.get_template('vf_report.html')
    with open('report.html', 'w') as f:
        f.write(j2_temp.render(configs).encode('utf8'))
    
    return configs