#!/usr/bin/env python
import cgi, os, json
import user_management as um

db = um.newDBConnection()

if __name__ == "__main__":
  form = cgi.FieldStorage()
  if not 'sid' in form or not 'ids' in form:
    return False
  
  sid = form.getvalue('sid')
  username = um.sidtouser(db, sid)
  userid = um.usertoid(db, username)
  ids = form.getvalue('filename')
  
  print('Content-Type:text/plain')
  print('')
  print('Done!')
  
  db.close()