#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import os
import time
import utils

def run(configs):
    start_time = time.time()
    
    utils.runclustalo('input.fasta', configs['stype'], configs['outfmt'], 'output.txt')
        
    configs['exec_time'] = '%.2f' % (time.time() - start_time)
    
    return configs