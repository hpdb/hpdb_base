#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from Bio import SeqIO
import os
import time
import jinja2
import yaml
import regex
import utils

def analyzecagA(pro):
    res = {}
    
    fuzzyA = utils.fuzzyFind(pro, 'EPIYA[QK]VNKKK[AT]GQ')
    if fuzzyA[0] >= 0.85:
        res['EPIYA-A'] = True
        res['EPIYA-A_seq'] = fuzzyA[1][0]
    else:
        res['EPIYA-A'] = False
    
    fuzzyB = utils.fuzzyFind(pro, 'EPIY[AT]QVAKKVNAKID')
    if fuzzyB[0] >= 0.85:
        res['EPIYA-B'] = True
        res['EPIYA-B_seq'] = fuzzyB[1][0]
    else:
        res['EPIYA-B'] = False
    
    fuzzyC = utils.fuzzyFind(pro, 'EPIYATIDDLGQPFPLK')
    if fuzzyC[0] >= 0.85:
        res['EPIYA-C'] = True
        res['EPIYA-C_seq'] = fuzzyC[1][0]
        fuzzyCC = utils.fuzzyFind(pro, 'EPIYATIDDLGQPFPLK', fuzzyC[1].start() + len('EPIYATIDDLGQPFPLK'))
        if fuzzyCC[0] >= 0.85:
            res['EPIYA-CC'] = True
            res['EPIYA-CC_seq'] = fuzzyCC[1][0]
        else:
            res['EPIYA-CC'] = False
    else:
        res['EPIYA-C'] = False
        res['EPIYA-CC'] = False
    
    fuzzyD = utils.fuzzyFind(pro, 'EPIYATIDFDEANQAG')
    if fuzzyD[0] >= 0.85:
        res['EPIYA-D'] = True
        res['EPIYA-D_seq'] = fuzzyD[1][0]
    else:
        res['EPIYA-D'] = False
    
    if res['EPIYA-A'] and res['EPIYA-B'] and res['EPIYA-C']:
        res['Origin'] = 'Western'
    elif res['EPIYA-A'] and res['EPIYA-B'] and res['EPIYA-D']:
        res['Origin'] = 'East Asian'
    
    return res

def analyzevacA(pro):
    res = {}
    
    # s1/s2
    start = utils.fuzzyFind(pro, 'MEIQQTHRKINRP')
    if start[0] < 0.75:
        res['s1s2'] = 'Khong xac dinh duoc s1/s2'
    else:
        end = utils.fuzzyFind(pro, 'AFFTTVII', start[1].start())
        if end[0] < 0.75:
            res['s1s2'] = 'Khong xac dinh duoc s1/s2'
        else:
            slen = end[1].start() - start[1].start() - len('MEIQQTHRKINRP')
            res['s1s2'] = 's1' if slen <= 25 else 's2'
    
    # m1/m2
    matched = regex.search('LGKAVNL(?:R){s<=1}VDAHT(A[YN]FNGNIYLG){s<=10}', pro)
    if not matched:
        res['m1m2'] = 'm1'
    else:
        percent = 1 - matched.fuzzy_counts[0] / len(matched[0])
        res['m1m2'] = 'm2' if percent >= 0.85 else 'Lai m1/m2'
    
    return res

def formatColor(str, seg, color = 'red'):
    return str.replace(seg, '<b style="color: %s;">%s</b>'.format(color, seg))

def run(configs):
    start_time = time.time()

    # ----- Run tools -----
    utils.runprodigal('input.fasta', 'prot.fasta', 'nu.fasta')
    caga_ids = utils.runblast('blastp', os.environ['HPDB_BASE'] + '/genome/j99_caga.fasta', 'prot.fasta', '0.0001', '10 sseqid').splitlines()
    vaca_ids = utils.runblast('blastp', os.environ['HPDB_BASE'] + '/genome/j99_vaca.fasta', 'prot.fasta', '0.0001', '10 sseqid').splitlines()
    
    # ----- Find virulence factors -----
    prot_dict = SeqIO.index('prot.fasta', 'fasta')
    nu_dict = SeqIO.index('nu.fasta', 'fasta')
    
    for id in caga_ids:
        caga_prot = str(prot_dict[id].seq).rstrip('*')
        caga_pos = prot_dict[id].description.split('#')
        caga_nu = str(nu_dict[id].seq).strip('*')
        if 'EPIYA' in caga_prot or 'EPIYT' in caga_prot:
            if len(caga_prot) > 800: configs['found_caga'] = True
            else: configs['mutant_caga'] = True
            break
    
    for id in vaca_ids:
        vaca_prot = str(prot_dict[id].seq).rstrip('*')
        vaca_pos = prot_dict[id].description.split('#')
        vaca_nu = str(nu_dict[id].seq).strip('*')
        if utils.fuzzyFind(vaca_prot, 'MELQQTHRKINRPLVSLALVG')[0] >= 0.8:
            if len(vaca_prot) > 800: configs['found_vaca'] = True
            else: configs['mutant_vaca'] = True
            break
    
    prot_dict.close()
    nu_dict.close()
    
    # ----- Analyze data -----
    # cagA
    if configs['found_caga']:
        configs['caga_analysis'] = analyzecagA(caga_prot)
        configs['caga_nu'] = {'name': 'cagA DNA', \
                              'raw': caga_nu, \
                              'formatted': caga_nu, \
                              'len': len(caga_nu), \
                              'start_pos': caga_pos[1].strip(), \
                              'end_pos': caga_pos[2].strip()}
        formatted = caga_prot
        if configs['caga_analysis']['EPIYA-A']:
            formatted = formatColor(formatted, configs['caga_analysis']['EPIYA-A_seq'], 'red')
        if configs['caga_analysis']['EPIYA-B']:
            formatted = formatColor(formatted, configs['caga_analysis']['EPIYA-B_seq'], 'blue')
        if configs['caga_analysis']['EPIYA-C']:
            formatted = formatColor(formatted, configs['caga_analysis']['EPIYA-C_seq'], 'green')
        if configs['caga_analysis']['EPIYA-CC']:
            formatted = formatColor(formatted, configs['caga_analysis']['EPIYA-CC_seq'], 'orange')
        if configs['caga_analysis']['EPIYA-D']:
            formatted = formatColor(formatted, configs['caga_analysis']['EPIYA-D_seq'], 'purple')
        configs['caga_prot'] = {'name': 'cagA Protein', \
                                'raw': caga_prot, \
                                'formatted': formatted, \
                                'len': len(caga_prot), \
                                'start_pos': caga_pos[1].strip(), \
                                'end_pos': caga_pos[2].strip()}
    
    # vacA
    if configs['found_vaca']:
        configs['vaca_analysis'] = analyzevacA(vaca_prot)
        configs['vaca_nu'] = {'name': 'vacA DNA', \
                              'raw': vaca_nu, \
                              'formatted': vaca_nu, \
                              'len': len(vaca_nu), \
                              'start_pos': vaca_pos[1].strip(), \
                              'end_pos': vaca_pos[2].strip()}
        configs['vaca_prot'] = {'name': 'vacA Protein', \
                                'raw': vaca_prot, \
                                'formatted': vaca_prot, \
                                'len': len(vaca_prot), \
                                'start_pos': vaca_pos[1].strip(), \
                                'end_pos': vaca_pos[2].strip()}
        
    configs['exec_time'] = '%.2f' % (time.time() - start_time)
    
    # ----- Output HTML -----
    j2_env = jinja2.Environment(loader = jinja2.FileSystemLoader(os.environ['HPDB_BASE'] + '/scripts/template'), trim_blocks = True)
    j2_temp = j2_env.get_template('vf_report.html')
    with open('report.html', 'w') as f:
        f.write(j2_temp.render(configs).encode('utf8'))
    
    return configs