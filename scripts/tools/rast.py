#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import os
import time
import utils
import rast_sdk as rast

username = ''
password = ''

def run(configs):
    start_time = time.time()
    configs['rast_id'] = rast.submit_RAST_job(username, password, 'input.fasta', configs['strain'])
    configs['exec_time'] = '%.2f' % (time.time() - start_time)
    return configs

def check(configs):
    x = rast.status_of_RAST_job(username, password, configs['rast_id'])