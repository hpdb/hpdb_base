#!/usr/bin/env python

from __future__ import division
from Bio import SeqIO
import cgi, os, regex, yaml
import jinja2

def main():
    form = cgi.FieldStorage()
    pwd = form.getvalue('pwd')
    if not pwd or pwd != 'ptnk1720':
        j2_env = jinja2.Environment(loader = jinja2.FileSystemLoader(os.environ['HPDB_BASE'] + '/scripts/template'), trim_blocks = True)
        j2_temp = j2_env.get_template('notfound.html')
        print('Content-type:text/html')
        print('')
        print(j2_temp.render(os.environ).encode('utf8'))
        return
    
    data_dir = os.environ['HPDB_BASE'] + '/data/project/'
    jobids = sorted(os.listdir(data_dir))
    
    print('Content-type:text/html')
    print('')
    print('<html>')
    print('<head>')
    print('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    print('<title>HPDB - PTNK</title>')
    print('</head>')
    print('<body>')
    print('<ul>')
    for id in jobids:
        with open(data_dir + id + '/configs.yaml') as f:
            configs = yaml.full_load(f)
        if os.path.isfile(data_dir + id + '/queued'):
            print('<li><b>' + configs['filename'] + ':</b> {0} (in queue)</li>'.format(id))
        else:
            print('<li><b>' + configs['filename'] + '</b>,<a href="/cgi-bin/getbyid.cgi?jobid={0}&pwd={1}">{0}</a>'.format(id, pwd))
    print('</ul>')
    print('</body>')
    print('</html>')
    
if __name__ == "__main__":
    main()