#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from subprocess import call
from Bio import SeqIO
import os, shutil
import time
import utils

def createRtabPlot():
  call('create_pan_genome_plots.R', shell = True)
  shutil.move('conserved_vs_total_genes.png', '../plots/')
  shutil.move('unique_vs_new_genes.png', '../plots/')
  shutil.move('Rplots.pdf', '../plots/')

def createAccessoryPlot(format = 'png', labels = False):
  '''
  Taken and modified from roary_plots.py
  '''
  import matplotlib
  matplotlib.use('Agg')
  
  import matplotlib.pyplot as plt
  import seaborn as sns
  
  sns.set_style('white')
  
  import os
  import pandas as pd
  import numpy as np
  from Bio import Phylo
  
  t = Phylo.read('accessory_binary_genes.fa.newick', 'newick')
  
  # Max distance to create better plots
  mdist = max([t.distance(t.root, x) for x in t.get_terminals()])
  
  # Load roary
  roary = pd.read_csv('gene_presence_absence.csv', low_memory = False)
  # Set index (group name)
  roary.set_index('Gene', inplace = True)
  # Drop the other info columns
  roary.drop(list(roary.columns[:13]), axis = 1, inplace = True)
  
  # Transform it in a presence/absence matrix (1/0)
  roary.replace('.{2,100}', 1, regex = True, inplace = True)
  roary.replace(np.nan, 0, regex = True, inplace = True)
  
  # Sort the matrix by the sum of strains presence
  idx = roary.sum(axis = 1).sort_values(ascending = False).index
  roary_sorted = roary.loc[idx]
  
  # Pangenome frequency plot
  plt.figure(figsize = (7, 5))
  
  plt.hist(roary.sum(axis = 1), roary.shape[1],
           histtype = "stepfilled", alpha = .7)
  
  plt.xlabel('No. of genomes')
  plt.ylabel('No. of genes')
  
  sns.despine(left = True, bottom = True)
  plt.savefig('pangenome_frequency.%s' % format, dpi = 300)
  plt.clf()
  
  # Sort the matrix according to tip labels in the tree
  roary_sorted = roary_sorted[[x.name for x in t.get_terminals()]]
  
  # Plot presence/absence matrix against the tree
  with sns.axes_style('whitegrid'):
    fig = plt.figure(figsize = (17, 10))
    
    ax1=plt.subplot2grid((1,40), (0, 10), colspan = 30)
    a=ax1.matshow(roary_sorted.T,
                  cmap = plt.cm.Blues,
                  vmin = 0, vmax = 1,
                  aspect = 'auto',
                  interpolation = 'none')
    ax1.set_yticks([])
    ax1.set_xticks([])
    ax1.axis('off')
    
    ax = fig.add_subplot(1,2,1)
    # matplotlib v1/2 workaround
    try:
      ax=plt.subplot2grid((1,40), (0, 0), colspan = 10, facecolor = 'white')
    except AttributeError:
      ax=plt.subplot2grid((1,40), (0, 0), colspan = 10, axisbg = 'white')
    
    fig.subplots_adjust(wspace = 0, hspace = 0)
    
    ax1.set_title('Roary matrix\n(%d gene clusters)' % roary.shape[0])
    
    if labels:
      fsize = 12 - 0.1 * roary.shape[1]
      if fsize < 7:
        fsize = 7
      with plt.rc_context({'font.size': fsize}):
        Phylo.draw(t, axes = ax, 
                   show_confidence = False,
                   label_func = lambda x: str(x)[:10],
                   xticks = ([],), yticks = ([],),
                   ylabel = ('',), xlabel = ('',),
                   xlim = (-mdist * 0.1, mdist + mdist * 0.45 - mdist * roary.shape[1] * 0.001),
                   axis = ('off', ),
                   title = ('Tree\n(%d strains)' % roary.shape[1],), 
                   do_show = False)
    else:
      Phylo.draw(t, axes = ax, 
                 show_confidence = False,
                 label_func = lambda x: None,
                 xticks = ([],), yticks=([],),
                 ylabel = ('',), xlabel=('',),
                 xlim = (-mdist * 0.1, mdist + mdist * 0.1),
                 axis = ('off', ),
                 title = ('Tree\n(%d strains)' % roary.shape[1],),
                 do_show = False)
    plt.savefig('pangenome_matrix.%s' % format, dpi = 300)
    plt.clf()
  
  # Plot the pangenome pie chart
  plt.figure(figsize=(10, 10))
  
  core     = roary[(roary.sum(axis=1) >= roary.shape[1] * 0.99) & (roary.sum(axis=1) <= roary.shape[1]       )].shape[0]
  softcore = roary[(roary.sum(axis=1) >= roary.shape[1] * 0.95) & (roary.sum(axis=1) <  roary.shape[1] * 0.99)].shape[0]
  shell    = roary[(roary.sum(axis=1) >= roary.shape[1] * 0.15) & (roary.sum(axis=1) <  roary.shape[1] * 0.95)].shape[0]
  cloud    = roary[roary.sum(axis=1)  < roary.shape[1]  * 0.15].shape[0]
  
  total = roary.shape[0]
  
  def my_autopct(pct):
    val = int(round(pct * total / 100.0))
    return '{v:d}'.format(v = val)
  
  a = plt.pie([core, softcore, shell, cloud],
      labels = ['core\n(%d <= strains <= %d)' % (roary.shape[1] * .99,roary.shape[1]),
                'soft-core\n(%d <= strains < %d)' % (roary.shape[1] * .95,roary.shape[1] * .99),
                'shell\n(%d <= strains < %d)' % (roary.shape[1] * .15,roary.shape[1] * .95),
                'cloud\n(strains < %d)' % (roary.shape[1] * .15)],
      explode = [0.1, 0.05, 0.02, 0], radius = 0.9,
      colors = [(0, 0, 1, float(x) / total) for x in (core, softcore, shell, cloud)],
      autopct = my_autopct)
  plt.savefig('pangenome_pie.%s' % format, dpi = 300)
  plt.clf()
  
  shutil.move('pangenome_frequency.png', '../plots/')
  shutil.move('pangenome_matrix.png', '../plots/')
  shutil.move('pangenome_pie.png', '../plots/')

def run(configs):
  start_time = time.time()
  
  files = sorted(os.listdir('input'))
  #files = [os.path.splitext(f)[0] for f in files]
  
  utils.mkdir('output')
  utils.mkdir('output/gff')
  utils.mkdir('output/plots')
  
  for f in files:
    call('bp_genbank2gff3.pl input/' + f + ' --outdir output/gff', shell = True)
    time.sleep(2)
  
  call('roary -f ./output/roary -i %s -e -n ./output/gff/*.gff' % configs['minidentity'], shell = True)
  
  os.chdir('output/roary')
  accessory_plot_files = ['accessory_binary_genes.fa.newick', 'gene_presence_absence.csv']
  rtab_plot_files = ['number_of_new_genes.Rtab', 'number_of_conserved_genes.Rtab', 'number_of_genes_in_pan_genome.Rtab', 'number_of_unique_genes.Rtab', 'blast_identity_frequency.Rtab']
  if all([os.path.isfile(f) for f in accessory_plot_files]):
    createAccessoryPlot()
  if all([os.path.isfile(f) for f in rtab_plot_files]):
    createRtabPlot()
  os.chdir('../../')
  
  os.chdir('output/plots')
  if os.path.isfile('pangenome_frequency.png'):
    from PIL import Image
    
    image1 = Image.open('pangenome_frequency.png')
    image2 = Image.open('pangenome_matrix.png')
    image3 = Image.open('pangenome_pie.png')
    
    im1 = image1.convert('RGB')
    im2 = image2.convert('RGB')
    im3 = image3.convert('RGB')
    
    im1.save('pangenome.pdf', save_all = True, append_images = [im2, im3])
  
  from PyPDF2 import PdfFileMerger
  pdfs = ['Rplots.pdf']
  if os.path.isfile('pangenome.pdf'):
    pdfs.append('pangenome.pdf')
  
  merger = PdfFileMerger()
  for pdf in pdfs:
    merger.append(pdf)
  merger.write("../../report.pdf")
  merger.close()
  
  os.chdir('../../')
  
  configs['exec_time'] = '%.2f' % (time.time() - start_time)
  
  return configs