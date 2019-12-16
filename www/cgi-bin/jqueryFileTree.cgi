#!/usr/bin/env python
import cgi
import os
import user_management as um

db = um.newDBConnection()

def listdir():
  form = cgi.FieldStorage()
  if not 'sid' in form:
    return ''
  
  dir = form.getvalue('dir')
  if not dir:
    dir = ''
  
  sid = form.getvalue('sid')
  username = um.sidtouser(db, sid)
  userid = um.usertoid(db, username)
  safe_dir = os.path.realpath(um.getUserDir(userid)) + '/'

  # prevent directory traversal attack
  if os.path.commonprefix((os.path.realpath(os.path.join(safe_dir + dir)), safe_dir)) != safe_dir:
    dir = ''
  real_dir = os.path.join(safe_dir + dir)
  
  r = ['<ul class="jqueryFileTree" style="display: none;">']
  lst = sorted(os.listdir(real_dir))
  for f in lst:
    ff = os.path.join(real_dir, f)
    fff = os.path.join(dir, f)
    if os.path.isdir(ff):
      r.append('<li class="directory collapsed"><a rel="%s/">%s</a></li>' % (fff, f))
  for f in lst:
    ff = os.path.join(real_dir, f)
    fff = os.path.join(dir, f)
    if os.path.isfile(ff):
      e = os.path.splitext(f)[1][1:]
      r.append('<li class="file ext_%s"><a rel="%s">%s</a></li>' % (e, fff, f))
  r.append('</ul>')
  return ''.join(r)

if __name__ == "__main__":
  print('Access-Control-Allow-Origin: *')
  print('Content-Type:text/plain')
  print('')
  print(listdir())
  db.close()