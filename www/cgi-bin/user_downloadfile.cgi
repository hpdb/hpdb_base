#!/usr/bin/env python
import cgi, os, yaml, csv
import user_management as um

db = um.newDBConnection()

def process():
  form = cgi.FieldStorage()
  if not 'sid' in form or not 'file' in form:
    return ''
  
  sid = form.getvalue('sid')
  file = form.getvalue('file')
  username = um.sidtouser(db, sid)
  userid = um.usertoid(db, username)
  safe_dir = os.path.realpath(um.getUserDir(userid)) + '/'
  
  # prevent directory traversal attack
  if os.path.commonprefix((os.path.realpath(os.path.join(safe_dir + file)), safe_dir)) != safe_dir:
    return ''
  
  return os.path.join(safe_dir + file)

if __name__ == "__main__":
  filepath = process()
  if filepath == '':
    print('Access-Control-Allow-Origin: *')
    print('Content-Type:text/plain')
    print('')
  else:
    print('X-Sendfile: ' + filepath)
    print('Content-Type: application/octet-stream')
    print('Content-Disposition: attachment; filename=' + os.path.basename(filepath))
    print('Pragma: no-cache')
    print('')
  db.close()