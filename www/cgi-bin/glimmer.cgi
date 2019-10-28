#!/usr/bin/env python

import cgi
import subprocess
import os, tempfile, shutil

from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

def glimmer2seq(glimmer_prediction, genome_sequence, outfile):
    glimmerfile = open(glimmer_prediction, "r")
    sequence = open(genome_sequence)
    
    fastafile = SeqIO.parse(sequence, "fasta")
    
    sequences = dict()
    seq_records = list()
    for entry in fastafile:
        sequences[entry.description] = entry
    
    for line in glimmerfile:
        if line.startswith('>'):
            entry = sequences[line[1:].strip()]
        else:
            orf_start = int(line[8:17])
            orf_end = int(line[18:26])
    
            orf_name = line[0:8]
            if orf_start <= orf_end:
                seq_records.append(SeqRecord(entry.seq[orf_start-1 : orf_end].translate(), id = orf_name, description = entry.description))
            else:
                seq_records.append(SeqRecord(entry.seq[orf_end-1 : orf_start].reverse_complement().translate(), id = orf_name, description = entry.description))
    
    SeqIO.write(seq_records, outfile, "fasta")
    glimmerfile.close()
    sequence.close()

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
    
    dirpath = tempfile.mkdtemp()
    os.chdir(dirpath)
    
    with open('hp.fasta', 'wb') as f:
        f.write(form['seqfile'].file.read())
    
    subprocess.call('build-icm output.icm < hp.fasta &> /dev/null', shell=True)
    subprocess.call('glimmer3 hp.fasta output.icm hp &> /dev/null', shell=True)
    glimmer2seq('hp.predict', 'hp.fasta', 'prot.fasta')
    
    subprocess.call('blastp -query /home/baohiep/Data/j99_caga.fasta -subject prot.fasta -outfmt "10 sseqid" -out result.caga', shell=True)
    with open('result.caga') as f:
        cagaid = f.readline().strip()
    
    subprocess.call('blastp -query /home/baohiep/Data/j99_vaca.fasta -subject prot.fasta -outfmt "10 sseqid" -out result.vaca', shell=True)
    with open('result.vaca') as f:
        vacaid = f.readline().strip()
    
    record_dict = SeqIO.index("prot.fasta", "fasta")
    caga_prot = str(record_dict[cagaid].seq).strip('*')
    record_dict.close()
        
    record_dict = SeqIO.index("prot.fasta", "fasta")
    vaca_prot = str(record_dict[vacaid].seq).strip('*')
    record_dict.close()
    
    shutil.rmtree(dirpath)
    
    print('Access-Control-Allow-Origin: *')
    print('Content-Type:text/plain')
    print('')
    
    print('cagA Protein')
    print(caga_prot)
    print('')
    
    print('vacA Protein')
    print(vaca_prot)
    print('')

if __name__ == "__main__":
    main()