#!/usr/bin/env python

from __future__ import division
from subprocess import call, check_output
from Bio import SeqIO
import regex

def runprodigal(input, prot, nu):
    call('prodigal -a %s -d %s -i %s >/dev/null 2>&1' % (prot, nu, input), shell = True)

def runprokka(input, outdir, prefix):
    call("prokka --kingdom Bacteria --outdir %s --genus 'Helicobacter' --species 'Helicobacter pylori' --prefix %s %s >/dev/null 2>&1" % (outdir, prefix, input), shell = True)

def runblastp(query, subject):
    lines = check_output('blastp -query %s -subject %s -evalue 0.0001 -outfmt "10 sseqid"' % (query, subject), shell = True).splitlines()
    return lines

def runsnippy(ref, ctgs):
    call('snippy --mapqual 0 --outdir snippy --ref %s --ctgs %s >/dev/null 2>&1' % (ref, ctgs), shell = True)

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

def analyzecagA(pro):
    res = {}
    
    fuzzyA = fuzzyFind(pro, 'EPIYA[QK]VNKKK[AT]GQ')
    if fuzzyA[0] >= 0.85:
        res['EPIYA-A'] = True
        res['EPIYA-A_seq'] = fuzzyA[1][0]
    else:
        res['EPIYA-A'] = False
    
    fuzzyB = fuzzyFind(pro, 'EPIY[AT]QVAKKVNAKID')
    if fuzzyB[0] >= 0.85:
        res['EPIYA-B'] = True
        res['EPIYA-B_seq'] = fuzzyB[1][0]
    else:
        res['EPIYA-B'] = False
    
    fuzzyC = fuzzyFind(pro, 'EPIYATIDDLGQPFPLK')
    if fuzzyC[0] >= 0.85:
        res['EPIYA-C'] = True
        res['EPIYA-C_seq'] = fuzzyC[1][0]
        fuzzyCC = fuzzyFind(pro, 'EPIYATIDDLGQPFPLK', fuzzyC[1].start() + len('EPIYATIDDLGQPFPLK'))
        if fuzzyCC[0] >= 0.85:
            res['EPIYA-CC'] = True
            res['EPIYA-CC_seq'] = fuzzyCC[1][0]
        else:
            res['EPIYA-CC'] = False
    else:
        res['EPIYA-C'] = False
        res['EPIYA-CC'] = False
    
    fuzzyD = fuzzyFind(pro, 'EPIYATIDFDEANQAG')
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
    start = fuzzyFind(pro, 'MEIQQTHRKINRP')
    if start[0] < 0.75:
        res['s1s2'] = 'Khong xac dinh duoc s1/s2'
    else:
        end = fuzzyFind(pro, 'AFFTTVII', start[1].start())
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

def formatAMR2HTML(inp):
    out = []
    for x in inp:
        if x[0] != x[-1]:
            out.append('<span style="font-weight:bold; color:red">' + x + '</span>')
        else:
            out.append(x)
    return ' '.join(out)