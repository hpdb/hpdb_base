#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import os
import time
import utils

def run(configs):
  start_time = time.time()
  utils.runsnippy('ref.fasta', 'input.fasta')
  
  with open('snippy/snps.consensus.fa') as f:
    lines = f.readlines()[1:]
  
  with open('result.txt', 'w') as f:
    f.writelines(lines)
  
  configs['exec_time'] = '%.2f' % (time.time() - start_time)
  return configs