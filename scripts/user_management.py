#!/usr/bin/env python

import os, binascii
import MySQLdb, hashlib
import utils

# change your password here
def newDBConnection():
    return MySQLdb.connect(user = "root", passwd = "hpdb2019", db = "hpdb")

def generateRandomSessionKey():
    return binascii.hexlify(os.urandom(32))

def sidtouser(db, sid):
    c = db.cursor()
    c.execute("select username from sessions where sid=%s", [sid])
    r = c.fetchall()
    return r[0][0].lower() if len(r) > 0 else ''

def usertoid(db, username):
    username = username.lower()
    c = db.cursor()
    c.execute("select id from users where username=%s", [username])
    r = c.fetchall()
    return r[0][0] if len(r) > 0 else 0

def getUserDir(userid):
    return os.environ['HPDB_BASE'] + '/data/' + str(userid) + '/'

def getUserUploadDir(userid):
    return os.environ['HPDB_BASE'] + '/data/' + str(userid) + '/MyUpload/'

def getUserDownloadDir(userid):
    return os.environ['HPDB_BASE'] + '/data/' + str(userid) + '/MyDownload/'

def getUserProjectDir(userid):
    return os.environ['HPDB_BASE'] + '/data/' + str(userid) + '/MyProjects/'

def addsession(db, userid, username, sid, logintime):
    username = username.lower()
    c = db.cursor()
    c.execute("insert into sessions(sid, userid, username, lastlogin) values (%s, %s, %s, %s)", (sid, userid, username, logintime));
    db.commit()

def checksession(db, sid):
    c = db.cursor()
    c.execute("select * from sessions where sid=%s", [sid])
    r = c.fetchall()
    return r

def addproject(db, userid, username, jobid):
    username = username.lower()
    c = db.cursor()
    c.execute("insert into projects(jobid, userid, username) values (%s, %s, %s)", (jobid, userid, username));
    db.commit()

def listprojects(db, username):
    username = username.lower()
    c = db.cursor()
    c.execute("select jobid from projects where username=%s", [username])
    r = c.fetchall()
    return [x[0] for x in r]

def checkpassword(db, username, hash, random):
    username = username.lower()
    c = db.cursor()
    c.execute("select password from users where username=%s", [username])
    r = c.fetchall()
    if len(r) == 0 or hash != hashlib.sha256((random + r[0][0]).encode()).hexdigest():
        return False
    else:
        return True

def signup(db, email, username, password):
    # FIX-ME: check when user exists
    username = username.lower()
    c = db.cursor()
    c.execute("insert into users(email, username, password) values (%s, %s, %s)", (email, username, password));
    db.commit()
    id = usertoid(db, username)
    user_folder = os.environ['HPDB_BASE'] + '/data/' + str(id) + '/'
    utils.mkdir(user_folder)
    utils.mkdir(user_folder + 'MyUpload')
    utils.mkdir(user_folder + 'MyDownload')
    utils.mkdir(user_folder + 'MyProjects')

def logout(db, sid):
    c = db.cursor()
    c.execute("delete from sessions where sid=%s", [sid]);
    db.commit()