#!/usr/bin/env python

from __future__ import division
import cgi
import subprocess
import os, tempfile, shutil
import regex

from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

from ref import HPrrnA23S, HPrrnB23S

DEBUG = False

def log(s):
    if DEBUG:
        print(s)

def fuzzyFind(s1, s2, start = 0):
    return regex.search('(?:%s){s<=%d}' % (s2, len(s2)), s1[start:], flags=regex.BESTMATCH)

def main():
    form = cgi.FieldStorage()
    if not form.getvalue('seqfile'):
        print('Content-Type:text/html')
        print('')
        print('<html>')
        print('<head>')
        print('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        print('<title>HPDB - PTNK</title>')
        print('</head>')
        print('<body>')
        print('<h2>Invalid</h2>')
        print('</body>')
        print('</html>')
        return
    
    global DEBUG
    if form.getvalue('debug') == 'on':
        DEBUG = True
    else:
        DEBUG = False
    
    dirpath = tempfile.mkdtemp()
    os.chdir(dirpath)
    
    with open('hp.fasta', 'wb') as f:
        f.write(form['seqfile'].file.read())
    subprocess.call('snippy --outdir output --ref %s/genome/26695_nu.fasta --ctgs hp.fasta'  % os.environ['HPDB_BASE'], shell=True)

    print('Content-type:text/html')
    print('')
    print('<html>')
    print('<head>')
    print('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    print('<title>HPDB - PTNK</title>')
    print('</head>')
    print('<body>')
    print('<h3>Filename: %s</h3>' % form['seqfile'].filename)
    
    record = SeqIO.read("output/snps.consensus.subs.fa", "fasta")
    A23S = fuzzyFind(str(record.seq), HPrrnA23S)
    B23S = fuzzyFind(str(record.seq), HPrrnB23S)
    if A23S.fuzzy_counts[0] > 5 and B23S.fuzzy_counts[0] > 5:
        print ('Khong tim thay')
    elif A23S[0][2141] == 'C' or A23S[0][2141] == 'G' or A23S[0][2142] == 'G' or B23S[0][2141] == 'C' or B23S[0][2141] == 'G' or B23S[0][2142] == 'G':
        print('Dot bien')
    elif A23S[0][2141] == 'A' and A23S[0][2142] == 'C' and B23S[0][2141] == 'A' and B23S[0][2142] == 'C':
        print('Khong dot bien')
    else:
        print('Khong the xac dinh')
    
    shutil.rmtree(dirpath)
    
    print('</body>')
    print('</html>')

if __name__ == "__main__":
    main()