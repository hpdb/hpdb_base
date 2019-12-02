#!/usr/bin/env python

from __future__ import division
from Bio import SeqIO
import cgi, os, regex, yaml
import jinja2
import MySQLdb
import user_management as um

db = um.newDBConnection()

def main():
    form = cgi.FieldStorage()
    if not 'sid' in form:
        return ''
    
    sid = form.getvalue('sid')
    username = um.sidtouser(db, sid)
    userid = um.usertoid(db, username)
    jobids = um.listprojects(db, username)
    jobids.reverse() # list jobs from newest to oldest
    
    projects_dir = um.getUserProjectDir(userid)
    
    projects = []
    
    for id in jobids:
        if not os.path.isdir(projects_dir + id):
            continue
        proj = {}
        with open(projects_dir + id + '/configs.yaml') as f:
            configs = yaml.full_load(f)
        proj['jobid'] = configs['jobid']
        proj['name'] = configs['projname']
        proj['filename'] = configs['filename']
        proj['type'] = configs['jobtype']
        proj['daysubmit'] = configs['daysubmit']
        if os.path.isfile(projects_dir + id + '/error'):
            proj['done'] = False
            proj['status'] = 'Error'
            proj['percent'] = '0'
        elif os.path.isfile(projects_dir + id + '/running'):
            proj['done'] = False
            proj['status'] = 'Running'
            proj['percent'] = '50'
        elif os.path.isfile(projects_dir + id + '/queued'):
            proj['done'] = False
            proj['status'] = 'In queue'
            proj['percent'] = '0'
        else:
            proj['done'] = True
            proj['status'] = 'Complete'
            proj['percent'] = '100'
            proj['reportjob'] = '/cgi-bin/user_getjobreport.cgi?jobid=%s&sid=%s' % (id, sid)
            proj['downloadjob'] = '/cgi-bin/user_downloadjob.cgi?jobid=%s&sid=%s' % (id, sid)
            proj['deletejob'] = '/cgi-bin/user_deletejob.cgi?jobid=%s&sid=%s' % (id, sid)
        projects.append(proj)
    
    projects = {'projects': projects}
    
    j2_env = jinja2.Environment(loader = jinja2.FileSystemLoader(os.environ['HPDB_BASE'] + '/scripts/template'), trim_blocks = True)
    j2_temp = j2_env.get_template('projects_table.tmpl')
    
    return j2_temp.render(projects).encode('utf8')
    
if __name__ == "__main__":
    print('Access-Control-Allow-Origin: *')
    print('Content-type:text/plain')
    print('')
    print(main())
    db.close()