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
import utils

def run(configs):
    start_time = time.time()
    
    files = sorted(os.listdir('input'))
    files = [os.path.splitext(f)[0] for f in files]
    
    for f in files:
        utils.runprokka('input/' + f + '.fasta', 'output/' + f, f)
    
    return configs