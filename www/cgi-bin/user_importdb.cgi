#!/usr/bin/env python
import cgi, os
import jinja2
import yaml
import MySQLdb
import user_management as um

db = um.newDBConnection()

def main():
  form = cgi.FieldStorage()
  if not 'sid' in form or not 'jobid' in form or not 'filename' in form:
    return False
  
  jobid = form.getvalue('jobid')
  sid = form.getvalue('sid')
  username = um.sidtouser(db, sid)
  userid = um.usertoid(db, username)
  filename = form.getvalue('filename')
  filepath = um.getUserProjectDir(userid) + jobid + '/' + filename
  
  if not os.path.isfile(filepath):
    return False
  
  print('X-Sendfile: ' + filepath)
  print('Content-Type: application/octet-stream')
  print('Content-Disposition: attachment; filename=' + filename)
  print('Pragma: no-cache')
  print('')
  return True

if __name__ == "__main__":
  if not main():
    j2_env = jinja2.Environment(loader = jinja2.FileSystemLoader(os.environ['HPDB_BASE'] + '/scripts/template'), trim_blocks = True)
    j2_temp = j2_env.get_template('notfound.html')
    print('Content-type:text/html')
    print('')
    print(j2_temp.render(os.environ).encode('utf8'))
  db.close()