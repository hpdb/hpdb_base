#!/usr/bin/env python

import cgi
import os
import MySQLdb
import json
import time
import user_management as um

db = um.newDBConnection()

def process():
  form = cgi.FieldStorage()
  action = form.getvalue('action')
  res = { 'success': False }
  if not action:
    res['error'] = 'No action selected'
  elif action == 'login':
    username = form.getvalue('username')
    hash = form.getvalue('hash')
    timestamp = form.getvalue('timestamp')
    logintime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(timestamp)/1000))
    if not username or not hash or not timestamp:
      res['error'] = 'Missing information'
    else:
      valid = um.checkpassword(db, username, hash, timestamp)
      if not valid:
        res['error'] = 'Incorrect credentials'
      else:
        sid = um.generateRandomSessionKey()
        userid = um.usertoid(db, username)
        um.addsession(db, userid, username, sid, logintime)
        res['success'] = True
        res['sid'] = sid
  elif action == 'check':
    sid = form.getvalue('sid')
    if not sid:
      res['error'] = 'Missing session id'
    else:
      r = um.checksession(db, sid)
      if len(r) > 0:
        res['success'] = True
        res['userid'] = r[0][1]
        res['username'] = r[0][2]
        res['lastlogin'] = r[0][3].strftime('%Y-%m-%d %H:%M:%S')
      else:
        res['error'] = 'sid not valid'
  elif action == 'logout':
    sid = form.getvalue('sid')
    if not sid:
      res['error'] = 'Missing session id'
    else:
      um.logout(db, sid)
      res['success'] = True
  elif action == 'signup':
    email = form.getvalue('email')
    username = form.getvalue('username')
    hash = form.getvalue('hash')
    if not email or not username or not hash:
      res['error'] = 'Missing information'
    else:
      um.signup(db, email, username, hash)
      res['success'] = True
  else:
    res['error'] = 'Invalid action'
  
  return res

if __name__ == "__main__":
  print('Content-Type:text/json')
  print('')
  print(json.dumps(process()))
  db.close()