#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, time, utils, textwrap

def run(configs):
  start_time = time.time()
  utils.runsnippy('ref.fasta', 'input.fasta')
  raw = utils.runblast('blastn', 'snippy/snps.consensus.fa', 'input.fasta', '0.0001', '10 sstart send sseq').splitlines()[0].split(',')
  
  start = int(raw[0])
  end = int(raw[1])
  if start > end:
    start, end = end, start
  length = end - start + 1
  
  with open('result.txt', 'w') as f:
    f.write('Start: %s\n' % str(start))
    f.write('End: %s\n' % str(end))
    f.write('Length: %s\n' % str(length))
    f.write('\n\n')
    f.write(textwrap.fill(raw[2], 60))
  
  configs['exec_time'] = '%.2f' % (time.time() - start_time)
  return configs