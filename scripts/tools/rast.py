#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from ConfigParser import ConfigParser
import os
import time
import utils
import RAST_sdk as rast

def check(configs):
    config = ConfigParser()
    config.read(os.environ['HPDB_BASE'] + '/sys.properties')
    username = config._sections['RAST Account']['username']
    password = config._sections['RAST Account']['password']
    res = yaml.safe_load(rast.status_of_RAST_job(username, password, configs['rast_id']).text)
    if res[configs['rast_id']]['status'] == 'complete':
        os.chdir(configs['dirpath'])
        rast.download_RAST_job(username, password, configs['rast_id'])
        return True, configs
    else:
        return False, configs