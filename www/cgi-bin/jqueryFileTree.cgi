#!/usr/bin/env python
import cgi, os, yaml
import user_management as um

db = um.newDBConnection()

def getJobInfo(config_file, dirname):
  if os.path.isfile(config_file):
    with open(config_file) as f:
      configs = yaml.full_load(f)
    
    return '%s (%s, %s, %s)' % (dirname, configs['projname'], configs['jobtype'], configs['daysubmit'])
  else:
    return dirname

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
  
  show_job_info = False
  if os.path.realpath(real_dir) == os.path.realpath(um.getUserProjectDir(userid)):
    show_job_info = True
  
  r = ['<ul class="jqueryFileTree" style="display: none;">']
  lst = sorted(os.listdir(real_dir))
  for f in lst:
    ff = os.path.join(real_dir, f)
    fff = os.path.join(dir, f)
    if os.path.isdir(ff):
      if show_job_info:
        r.append('<li class="directory collapsed"><a rel="%s/">%s</a></li>' % (fff, getJobInfo(ff + '/configs.yaml', f)))
      else:
        r.append('<li class="directory collapsed"><a rel="%s/">%s</a></li>' % (fff, f))
  
  show_job_info = False
  if os.path.realpath(real_dir) == os.path.realpath(um.getUserDownloadDir(userid)):
    show_job_info = True
  
  projectdir = um.getUserProjectDir(userid)
  for f in lst:
    ff = os.path.join(real_dir, f)
    fff = os.path.join(dir, f)
    if os.path.isfile(ff):
      jobid = os.path.splitext(f)[1][0]
      e = os.path.splitext(f)[1][1:]
      if show_job_info:
        r.append('<li class="file ext_%s"><a rel="%s">%s</a></li>' % (e, fff, getJobInfo(projectdir + jobid + '/configs.yaml', f)))
      else:
        r.append('<li class="file ext_%s"><a rel="%s">%s</a></li>' % (e, fff, f))
  r.append('</ul>')
  return ''.join(r)

if __name__ == "__main__":
  print('Access-Control-Allow-Origin: *')
  print('Content-Type:text/plain')
  print('')
  print(listdir())
  db.close()