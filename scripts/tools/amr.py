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
  out = []
  for x in inp:
    if x[0] != x[-1]:
      out.append('<span style="font-weight:bold; color:red">' + x + '</span>')
    else:
      out.append(x)
  return ' '.join(out)

def run(configs):
  start_time = time.time()
  
  # ----- Run tools -----
  utils.runsnippy(os.environ['HPDB_BASE'] + '/genome/26695.A23S.fasta',
                  'input.fasta',
                  'snippy_A23S')
  utils.runsnippy(os.environ['HPDB_BASE'] + '/genome/GCA_000008525.1_ASM852v1_genomic.gbff',
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
    
    configs['amr_analysis'][x['name']] = []
    for y in x['subs']:
      configs['amr_analysis'][x['name']].append(y['orig'] + str(y['pos'] + 1) + part[y['pos']])
    #configs['amr_analysis'][x['name']] = formatAMR2HTML(configs['amr_analysis'][x['name']]) + '    ' + part[x['subs'][0]['pos'] : x['subs'][0]['pos'] + 20] # Uncomment this to output 20 characters at that pos
  
  configs['exec_time'] = '%.2f' % (time.time() - start_time)
  
  # ----- Output HTML -----
  j2_env = jinja2.Environment(loader = jinja2.FileSystemLoader(os.environ['HPDB_BASE'] + '/scripts/template'), trim_blocks = True)
  j2_temp = j2_env.get_template('amr_report.html')
  with open('report.html', 'w') as f:
    f.write(j2_temp.render(configs).encode('utf8'))
  
  return configs