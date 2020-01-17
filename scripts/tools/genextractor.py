#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, time, utils, textwrap

def run(configs):
  start_time = time.time()
  utils.runsnippy('ref.fasta', 'input.fasta')
  raw = utils.runblast('blastn', 'snippy/snps.consensus.fa', 'input.fasta', '0.0001', '10 sstart send sseq').splitlines()[0].split(',')
  
  with open('result.txt', 'w') as f:
    f.write('Start: %s\n' % raw[0])
    f.write('End: %s\n' % raw[1])
    f.write('Length: %s\n' % str(int(raw[1]) - int(raw[0])))
    f.write('\n\n')
    f.write(textwrap.fill(raw[2], 60))
  
  configs['exec_time'] = '%.2f' % (time.time() - start_time)
  return configs