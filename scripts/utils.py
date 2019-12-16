#!/usr/bin/env python

from __future__ import division
from subprocess import call, check_output
from Bio import SeqIO
import regex, errno, os, zipfile, csv

def zip(path, output):
  zipf = zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED)
  for root, dirs, files in os.walk(path):
    for file in files:
      if file != 'running' and file != 'queued':
        zipf.write(os.path.join(root, file))
  zipf.close()

def mkdir(path):
  try:
    os.makedirs(path)
  except OSError as exc:
    if exc.errno == errno.EEXIST and os.path.isdir(path):
      pass
    else:
      raise

def runprodigal(input, prot, nu):
  call('prodigal -a %s -d %s -i %s >/dev/null 2>&1' % (prot, nu, input), shell = True)

def runclustalo(input, stype, outfmt, output):
  if outfmt == 'clustal_num':
    call('clustalo -i %s --seqtype=%s --outfmt=clu --resno -o %s' % (input, stype, output), shell = True)
  else:
    call('clustalo -i %s --seqtype=%s --outfmt=%s -o %s' % (input, stype, outfmt, output), shell = True)

def runprokka(input, outdir, prefix):
  call("prokka --kingdom Bacteria --outdir %s --genus 'Helicobacter' --species 'Helicobacter pylori' --prefix %s %s >/dev/null 2>&1" % (outdir, prefix, input), shell = True)

def runblast(prog, query, subject, evalue = '10', outfmt = '0'):
  return check_output('%s -query %s -subject %s -evalue %s -outfmt "%s"' % (prog, query, subject, evalue, outfmt), shell = True)

def runsnippy(ref, ctgs, outdir = 'snippy'):
  call('snippy --mapqual 0 --outdir %s --ref %s --ctgs %s >/dev/null 2>&1' % (outdir, ref, ctgs), shell = True)

def fuzzyFind(s1, s2, start = 0):
  fuzzy = regex.search('(?:%s){s<=%d}' % (s2, len(s2)), s1[start:], flags=regex.BESTMATCH)
  return [1 - fuzzy.fuzzy_counts[0] / len(fuzzy[0]), fuzzy]

def fuzzyFindInList(list, s2):
  best = 999999
  for s1 in list:
    fuzzy = regex.search('(?:%s){s<=%d}' % (s2, len(s2)), s1, flags=regex.BESTMATCH)
    if fuzzy is not None and fuzzy.fuzzy_counts[0] < best:
      best = fuzzy.fuzzy_counts[0]
      matched = fuzzy[0]
  return matched

def tsv2csv(input, output):
  with open(input, 'r') as fin:
    cr = csv.reader(fin, dialect = 'excel-tab')
    filecontents = [line for line in cr]
  
  # write comma-delimited file (comma is the default delimiter)
  with open(output, 'wb') as fou:
    cw = csv.writer(fou)
    cw.writerows(filecontents)