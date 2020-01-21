#!/usr/bin/env python

import psutil
import platform
import datetime
import os
import regex
import subprocess
import sys
import commands

def run(command):
  try:
    result = subprocess.check_output(command, shell=True)
  except subprocess.CalledProcessError as exc:
    result = exc.output
  return result

def size_fmt(num, suffix='B'):
  for unit in ['','K','M','G','T','P','E','Z']:
    if abs(num) < 1024.0:
      return "%3.1f%s%s" % (num, unit, suffix)
    num /= 1024.0
  return "%.1f%s%s" % (num, 'Yi', suffix)

def getProcessList():
  procs = []
  procs_status = {}
  for p in psutil.process_iter():
    try:
      p.dict = p.as_dict(['username', 'nice', 'memory_info',
                'memory_percent', 'cpu_percent',
                'cpu_times', 'name', 'status'])
      try:
        procs_status[p.dict['status']] += 1
      except KeyError:
        procs_status[p.dict['status']] = 1
    except psutil.NoSuchProcess:
      pass
    else:
      procs.append(p)

  # return processes sorted by CPU percent usage
  processes = sorted(procs, key = lambda p: p.dict['cpu_percent'], reverse = True)
  return (processes, procs_status)

def checkIfProcessRunning(processName):
  out = commands.getstatusoutput("ps aux | grep -e '%s' | grep -v grep" % processName)
  return len(out) > 0

def printHeader():
  def get_dashes(perc):
    dashes = '|' * int((float(perc) / 10 * 4))
    empty_dashes = ' ' * (40 - len(dashes))
    return dashes, empty_dashes
  
  # cpu usage
  percs = psutil.cpu_percent(interval=1, percpu=True)
  for cpu_num, perc in enumerate(percs):
    dashes, empty_dashes = get_dashes(perc)
    print('CPU%-2s [%s%s] %5s%%' % (cpu_num, dashes, empty_dashes, perc))
  
  # memory usage
  mem = psutil.virtual_memory()
  dashes, empty_dashes = get_dashes(mem.percent)
  print('Mem   [%s%s] %5s%% %10s / %s' % (
    dashes, empty_dashes,
    mem.percent,
    size_fmt(mem.used),
    size_fmt(mem.total),
  ))

  # swap usage
  swap = psutil.swap_memory()
  dashes, empty_dashes = get_dashes(swap.percent)
  print('Swap  [%s%s] %5s%% %10s / %s' % (
    dashes, empty_dashes,
    swap.percent,
    size_fmt(swap.used),
    size_fmt(swap.total),
  ))

  # disk usage
  disk = psutil.disk_usage('/')
  dashes, empty_dashes = get_dashes(disk.percent)
  print('Disk  [%s%s] %5s%% %10s / %s' % (
    dashes, empty_dashes,
    disk.percent,
    size_fmt(disk.used),
    size_fmt(disk.total),
  ))
  
  # processes number and status
  procs, procs_status = getProcessList()
  st = []
  for x, y in procs_status.items():
    if y:
      st.append('%s=%s' % (x, y))
  st.sort(key = lambda x: x[:3] in ('run', 'sle'), reverse = 1)
  print('Processes: %s (%s)' % (len(procs), ', '.join(st)))
  
  # load average, uptime
  av1, av2, av3 = psutil.getloadavg()
  print('Load average: %.2f %.2f %.2f' % (av1, av2, av3))

  # uptime
  uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
  print('Uptime: %s' % str(uptime).split('.')[0])
  
  print('Platform: %s' % platform.platform())
  print('')
  print('apache is running as %s' % str(run('whoami')).rstrip('\n'))
  print('runcore is ' + ('' if checkIfProcessRunning('runcore') else 'not ') + 'running')

def findVersion(name, cmd, re):
  proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
  out = proc.stdout.read()
  out = regex.search(re, out)
  if out is not None:
    return name + ' version: ' + out.group(1)
  else:
    return name + ' is not installed'

def printVersion():
  print('HPDB version: %s' % os.environ['HPDB_VERSION'])
  print(findVersion('apache', 'apache2 -v', r'Apache/*([\d.]+)'))
  print(findVersion('conda', 'conda -V', r'conda\s*([\d.]+)'))
  print(findVersion('python', 'python -V', r'Python\s*([\d.]+)'))
  print(findVersion('perl', 'perl --version', r'\s\(v*([\d.]+)'))
  print(findVersion('java', 'java -version', r'version\s"*([\d.]+)'))
  print(findVersion('blast', 'blastn -version', r'blastn:\s*([\d.+]+)'))
  print(findVersion('centrifuge', 'centrifuge --version', r'version\s*([\d.]+)'))
  print(findVersion('clustalo', 'clustalo --version', r'([\d.]+)'))
  print(findVersion('prodigal', 'prodigal -v', r'Prodigal\sV*([\d.]+)'))
  print(findVersion('snippy', 'snippy --version', r'snippy\s*([\d.]+)'))
  print(findVersion('roary', 'roary --version', r'([\d.]+)'))
  print(findVersion('samtools', 'samtools --version', r'samtools\s*([\d.]+)'))
  print(findVersion('bcftools', 'bcftools --version', r'bcftools\s*([\d.]+)'))
  print(findVersion('htslib', 'bcftools --version', r'htslib\s*([\d.]+)'))
  print(findVersion('freebayes', 'freebayes --version', r'version:\s*([\d-.a-z]+)'))
  print(findVersion('snpEff', 'snpEff -version', r'SnpEff\s*([\d.a-z]+)'))
  print(findVersion('bwa', 'bwa', r'Version:\s*([\d-.a-z]+)'))
  print(findVersion('grinder', 'grinder --version', r'version\s*([\d.]+)'))

def printEnviron():
  print('Environment Variables:')
  print(str(run('env')).rstrip('\n'))

def main():
  print('Access-Control-Allow-Origin: *')
  print('Content-Type:text/plain')
  print('')
  printHeader()
  print('')
  printVersion()
  print('')
  if sys.stdout.encoding is not None:
    print('Encoding: ' + sys.stdout.encoding)
    print('')
  printEnviron()

if __name__ == '__main__':
  main()