#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from Bio import SeqIO
import os, regex, yaml

def main():
  data_dir = os.environ['HPDB_BASE'] + '/data/project/'
  jobids = sorted(os.listdir(data_dir))
  
  print('Content-type:text/plain')
  print('')
  print('Name,cagA,vacA,EPIYA,s1/s2,m1/m2')
  for id in jobids:
    with open(data_dir + id + '/configs.yaml') as f:
      configs = yaml.full_load(f)
    if not os.path.isfile(data_dir + id + '/queued'):
      line = configs['filename']
      line += u',có' if configs['found_caga'] else (u',đbmđ' if configs['mutant_caga'] else ',ko')
      line += u',có' if configs['found_vaca'] else (u',đbmđ' if configs['mutant_vaca'] else ',ko')
      #line += ',' + str(configs['caga_prot']['len'] if configs['found_caga'] else -1)
      #line += ',' + str(configs['vaca_prot']['len'] if configs['found_vaca'] else -1)
      line += ','
      if configs['caga_analysis']['EPIYA-A']: line += 'A'
      if configs['caga_analysis']['EPIYA-B']: line += 'B'
      if configs['caga_analysis']['EPIYA-C']: line += 'C'
      if configs['caga_analysis']['EPIYA-D']: line += 'D'
      line += ',' + configs['vaca_analysis']['s1s2']
      line += ',' + configs['vaca_analysis']['m1m2']
      print(line)

if __name__ == "__main__":
  main()