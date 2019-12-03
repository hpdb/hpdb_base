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
    utils.runsnippy(os.environ['HPDB_BASE'] + '/genome/GCA_000008525.1_ASM852v1_genomic.gbff', 'input.fasta')
    utils.runprodigal('snippy/snps.consensus.subs.fa', 'snp_prot.fasta', 'snp_nu.fasta')
        
    # AMR
    genome = str(SeqIO.read('snippy/snps.consensus.subs.fa', 'fasta').seq)
    record = list(SeqIO.parse('snp_prot.fasta', 'fasta'))
    protein_seqs = [str(x.seq) for x in record]
    for x in AMR:
        if x['type'] == 'nu':
            if x['rev']:
                part = genome[x['end'] : x['start'] : -1]
            else:
                part = genome[x['start'] : x['end']]
        elif x['type'] == 'prot':
            part = utils.fuzzyFindInList(protein_seqs, x['ref'])
    
        configs['amr_analysis'][x['name']] = []
        for y in x['subs']:
            configs['amr_analysis'][x['name']].append(y['orig'] + str(y['pos'] + 1) + part[y['pos']])
        configs['amr_analysis'][x['name']] = utils.formatAMR2HTML(configs['amr_analysis'][x['name']])
    
    configs['exec_time'] = '%.2f' % (time.time() - start_time)
    
    # ----- Output HTML -----
    j2_env = jinja2.Environment(loader = jinja2.FileSystemLoader(os.environ['HPDB_BASE'] + '/scripts/template'), trim_blocks = True)
    j2_temp = j2_env.get_template('amr_report.html')
    with open('report.html', 'w') as f:
        f.write(j2_temp.render(configs).encode('utf8'))
    
    return configs