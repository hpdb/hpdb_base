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
    
    files = sorted(os.listdir('input'))
    files = [os.path.splitext(f)[0] for f in files]
    
    utils.mkdir('output')
    utils.mkdir('output/gff')
    
    for f in files:
        utils.runprokka('input/' + f + '.fasta', 'output/' + f, f)
        copyfile('output/' + f + '/' + f + '.gff', 'output/gff/' + f + '.gff')
    
    call('roary -f ./output/roary -e -n ./output/gff/*.gff', shell = True)
    
    configs['exec_time'] = '%.2f' % (time.time() - start_time)
    
    return configs