#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import os
import time
import utils

def run(configs):
    start_time = time.time()
    
    result = utils.runblast(configs['blastype'], 'query.fasta', 'subject.fasta')
    
    # Save result
    with open('output.txt', 'w') as f:
        f.write(result)
    
    configs['exec_time'] = '%.2f' % (time.time() - start_time)
    
    return configs