#!/usr/bin/env python
import cgi, os, json
import user_management as um

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
  
  ids = json.loads(form.getvalue('filename'))
  ids = [x for x in ids if len(x) == 7]
  
  print('Content-Type:text/plain')
  print('')
  print(ids)

if __name__ == "__main__":
  process()
  db.close()