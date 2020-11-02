#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from ConfigParser import ConfigParser
from subprocess import call
import os, glob
import time
import utils
import yaml
import RAST_sdk as rast

def check(configs):
  sys_config = ConfigParser()
  sys_config.read(os.environ['HPDB_BASE'] + '/sys.properties')
  rast_username = sys_config._sections['RAST Account']['username']
  rast_password = sys_config._sections['RAST Account']['password']
  res = yaml.safe_load(rast.status_of_RAST_job(rast_username, rast_password, configs['rast_id']).text)
  if not configs['rast_id'] in res:
    return False, configs
  elif not 'status' in res[configs['rast_id']]:
    return False, configs
  elif res[configs['rast_id']]['status'] != 'complete':
    return False, configs
  else: # complete
    os.chdir(configs['dirpath'])
    rast.download_RAST_job(rast_username, rast_password, configs['rast_id'])
    configs['rast_genome_id'] = os.path.splitext(glob.glob("*.txt")[0])[0]
    utils.tsv2csv(configs['rast_genome_id'] + '.txt', configs['rast_genome_id'] + '.csv')

    # prepare JBrowse data
    call('/usr/bin/perl ' + os.environ['HPDB_BASE'] + '/www/JBrowse/bin/prepare-refseqs.pl --fasta input.fasta --out JBrowse', shell = True)
    call('/usr/bin/perl ' + os.environ['HPDB_BASE'] + '/www/JBrowse/bin/flatfile-to-json.pl --gff ' + configs['rast_genome_id'] + '.gff --trackLabel gff --trackType CanvasFeatures --out JBrowse', shell = True)
    return True, configs
