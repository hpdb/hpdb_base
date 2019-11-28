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
from shutil import copyfile
import utils

def run(configs):
    start_time = time.time()
    
    result = utils.runblast(configs['blastype'], 'query.fasta', 'subject.fasta')
    
    # Save result
    
    
    configs['exec_time'] = '%.2f' % (time.time() - start_time)
    
    return configs