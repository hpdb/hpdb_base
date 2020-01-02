#!/usr/bin/env python
import cgi, os, json, glob
import user_management as um
from shutil import copyfile
db = um.newDBConnection()

def process():
  form = cgi.FieldStorage()
  if not 'sid' in form or not 'ids' in form:
    print('Content-Type:text/plain')
    print('')
    print('Erorr!')
    return
  
  sid = form.getvalue('sid')
  username = um.sidtouser(db, sid)
  userid = um.usertoid(db, username)
  useruploaddir = getUserUploadDir(userid)
  
  ids = json.loads(form.getvalue('ids'))
  ids = [x for x in ids if len(x) == 7]
  
  data_dir = os.environ['HPDB_BASE'] + '/database/hpdb_data-master/'
  with open(data_dir + 'strains_list.csv') as f:
    reader = csv.reader(f)
    rows = [row for row in reader if row[0] != 'Name']
  
  for row in rows:
    for id in ids:
      genome_id = int(id) // 10
      type = int(id) % 10
      if row[1] == str(genome_id):
        if type == 1: # FASTA
          copyfile(data_dir + row[1] + '/genomic.fna', useruploaddir + row[1] + '.fasta')
        elif type == 2: # GENBANK
          gbks = glob.glob(data_dir + row[1] + '/RAST/*.gbk')
          # gbks[0]: RASTID.ec-stripped.gbk
          # gbks[1]: RASTID.gkb
          # gbks[2]: RASTID.merged.gbk
          copyfile(gbks[1], useruploaddir + row[1] + '.gbk')
  
  print('Content-Type:text/plain')
  print('')
  print('Done')

if __name__ == "__main__":
  process()
  db.close()