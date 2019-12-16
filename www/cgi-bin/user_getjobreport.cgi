#!/usr/bin/env python
import cgi, os
import jinja2
import yaml
import MySQLdb
import user_management as um

db = um.newDBConnection()

def main():
  form = cgi.FieldStorage()
  if not 'sid' in form or not 'jobid' in form:
    return False
  
  jobid = form.getvalue('jobid')
  sid = form.getvalue('sid')
  username = um.sidtouser(db, sid)
  userid = um.usertoid(db, username)
  job_dir = um.getUserProjectDir(userid) + jobid + '/'
  
  html_path = os.environ['HPDB_BASE'] + '/scripts/template/invalid.html'
  if os.path.isfile(job_dir + 'configs.yaml'):
    with open(job_dir + 'configs.yaml') as f:
      configs = yaml.full_load(f)
    if configs['username'] == username and os.path.isfile(job_dir + '/report.html'):
      html_path = job_dir + '/report.html'
  
  print('Content-Type:text/html')
  print('')
  with open(html_path, 'r') as f:
    print(f.read())
  
  return True

if __name__ == "__main__":
  if not main():
    j2_env = jinja2.Environment(loader = jinja2.FileSystemLoader(os.environ['HPDB_BASE'] + '/scripts/template'), trim_blocks = True)
    j2_temp = j2_env.get_template('notfound.html')
    print('Content-type:text/html')
    print('')
    print(j2_temp.render(os.environ).encode('utf8'))
  db.close()