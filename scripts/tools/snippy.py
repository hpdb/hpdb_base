#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import os
import time
import utils

def run(configs):
    start_time = time.time()
    
    utils.runsnippy(os.environ['HPDB_BASE'] + '/genome/GCA_000008525.1_ASM852v1_genomic.gbff', 'input.fasta')
    
    configs['exec_time'] = '%.2f' % (time.time() - start_time)
    
    return configs