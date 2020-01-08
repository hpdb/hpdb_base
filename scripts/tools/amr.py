#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from subprocess import call
from Bio import SeqIO
import os
import time
import jinja2
import yaml
from ref_AMR import AMR
import utils

def formatAMR2HTML(inp):
  mutant = False
  out = []
  for x in inp:
    if x[0] != x[-1]:
      out.append('<span style="font-weight:bold; color:red">' + x + '</span>')
      mutant = True
    else:
      out.append(x)
  return ' '.join(out), mutant

def run(configs):
  start_time = time.time()
  
  # ----- Run tools -----
  utils.runsnippy(os.environ['HPDB_BASE'] + '/genome/26695.A23S.fasta',
                  'input.fasta',
                  'snippy_A23S')
  utils.runsnippy(os.environ['HPDB_BASE'] + '/genome/GCA_000008525.1_ASM852v1_genomic.fna',
                  'input.fasta',
                  'snippy_whole_genome')
  utils.runprodigal('snippy_whole_genome/snps.consensus.subs.fa',
                    'snippy_whole_genome/snp_prot.fasta',
                    'snippy_whole_genome/snp_nu.fasta')
  
  # AMR
  genome = str(SeqIO.read('snippy_A23S/snps.consensus.subs.fa', 'fasta').seq)
  record = list(SeqIO.parse('snippy_whole_genome/snp_prot.fasta', 'fasta'))
  protein_seqs = [str(x.seq) for x in record]
  for x in AMR:
    if x['type'] == 'nu':
      part = genome[x['start'] : x['end']]
    elif x['type'] == 'prot':
      part = utils.fuzzyFindInList(protein_seqs, x['ref'])
    
    tmp = {}
    tmp['antibiotic'] = x['antibiotic']
    tmp['typing method'] = x['typing method']
    tmp['resistance gene'] = x['resistance gene']
    tmp['mutations'] = []
    
    for y in x['subs']:
      tmp['mutations'].append(y['orig'] + str(y['pos'] + 1) + part[y['pos']])
    
    tmp['mutations'], mutant = formatAMR2HTML(tmp['mutations'])
    # + '    ' + part[x['subs'][0]['pos'] : x['subs'][0]['pos'] + 20]
    
    if mutant:
      tmp['resistant phenotype'] = 'Resistant'
    else:
      tmp['resistant phenotype'] = 'Susceptible'
    
    configs['amr_analysis'].append(tmp)
  
  configs['exec_time'] = '%.2f' % (time.time() - start_time)
  
  # ----- Output HTML -----
  j2_env = jinja2.Environment(loader = jinja2.FileSystemLoader(os.environ['HPDB_BASE'] + '/scripts/template'), trim_blocks = True)
  j2_temp = j2_env.get_template('amr_report.html')
  with open('report.html', 'w') as f:
    f.write(j2_temp.render(configs).encode('utf8'))
  
  return configs