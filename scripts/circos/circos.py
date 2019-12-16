import glob, os
from subprocess import call

def karyotype_file_from_fasta(fasta_fname, out_fname, chr2color = None):
  outfile = open(out_fname, 'w')
  l      = 0 # counter for the sequence length
  cindex = 1 # counter for the chromosomes 
  cid    = ''
  color  = 'grey'
  for line in open(fasta_fname).readlines():
    if line[0] == '>':
      if l > 0:
        outfile.write('chr - ' + cid + ' ' + str(cindex) + ' 0 ' + ' ' + str(l) + ' ' + color + '\n')
        l = 0
        cindex += 1
      cid = line[1:].strip().split()[0]
      if chr2color != None and cid in chr2color:
        color = chr2color[cid]
      print(cid, cindex)
        
    else:
      l += len(line.strip())
  # last one
  if l > 0:
    outfile.write('chr - ' + cid + ' ' + str(cindex) + ' 0 ' + ' ' + str(l) + ' ' + color + '\n')
  
  outfile.close()

def coords_to_links(coords_fname, links_fname, chr2color = None, min_length = 0):
  linksfile = open(links_fname, 'w')
  lines     = open(coords_fname).readlines()
  type      = lines[1].strip()
  lines     = lines[5:] #skip header
  for line in lines:
    columns = line.strip().split()
    if type == 'PROMER':
      chrA  = columns[15]
      chrB  = columns[16]
      fromA = columns[0]
      toA   = columns[1]
      fromB = columns[3]
      toB   = columns[4]
      lenA  = int(columns[6])
      lenB  = int(columns[7])
    elif type == 'NUCMER':
      chrA  = columns[11]
      chrB  = columns[12]
      fromA = columns[0]
      toA   = columns[1]
      fromB = columns[3]
      toB   = columns[4]
      lenA  = int(columns[6])
      lenB  = int(columns[7])
    else:
      print('Unexpected fileformat, can not continue!')
    
    if lenA >= min_length and lenB >= min_length: 
      out = chrA + ' ' + fromA + ' ' + toA + ' ' + chrB + ' ' + fromB + ' ' + toB
      
      if chr2color != None:
        if chrA in chr2color:
          linksfile.write(out + ' color=' + chr2color[chrA] + '\n')
        elif chrB in chr2color:
          linksfile.write(out + ' color=' + chr2color[chrB] + '\n')
      else:
        linksfile.write(out + '\n')
  linksfile.close()

call("promer -p promer_out genomes/26695.fna genomes/j99.fna >& promer.log", shell = True)
call("show-coords -r promer_out.delta > promer_out.coords", shell = True)

filenames = []
filenames.extend(glob.glob('genomes/*.fna'))
filenames.extend(glob.glob('genomes/*.fasta'))

chr2color = {}
chr2color['NC_000915.1'] = 'blue'
chr2color['NC_000921.1'] = 'yellow'

for i, fasta_fname in enumerate(filenames):
  out_fname = 'karyotypes/' + os.path.splitext(os.path.basename(fasta_fname))[0] + '.txt'
  karyotype_file_from_fasta(fasta_fname, out_fname, chr2color = chr2color)

coords_fname = 'promer_out.coords'
links_fname  = 'links/links.txt'
coords_to_links(coords_fname, links_fname, chr2color = chr2color, min_length = 1000)

call("circos -conf circos.conf", shell = True)