#!/usr/bin/env python

from __future__ import division
import cgi
import json
import requests
import regex

DEBUG = False

def log(s):
  if DEBUG:
    print(s)

def getPredictResult(id):
  return requests.get('http://www.mgc.ac.cn/cgi-bin/VFs/v5/v5/v5_predictJsondata.pl?ID={}'.format(id)).text

def findPredictionIndex(raw):
  region = raw.index('renderPredictedGene')
  start = raw.index('"dataIndex":"', region - 200) + len('"dataIndex":"')
  end = raw.index('",', start)
  return raw[start:end]

def findGeneID(raw, gene, ind):
  region = raw.index('"related_genes":"<i>{}</i>"'.format(gene))
  start = raw.index('{', region - 200)
  end = raw.index('}', start) + 1
  return json.loads(raw[start:end])[ind].split(',')

def downloadGene(id):
  response = requests.get('http://www.mgc.ac.cn/cgi-bin/VFs/v5/v5/v5_predictGeneWin.pl?VFGID={}&folder={}'.format(*id))
  raw = response.text
  
  start_dna = raw.index('<input type="hidden" name="seq" value="') + len('<input type="hidden" name="seq" value="')
  end_dna = raw.index('" />', start_dna)
  
  start_pro = raw.index('<input type="hidden" name="seq" value="', end_dna) + len('<input type="hidden" name="seq" value="')
  end_pro = raw.index('" />', start_pro)
  return [raw[start_dna:end_dna], raw[start_pro:end_pro]]

def fuzzyFind(s1, s2, start = 0):
  fuzzy = regex.search('(?:%s){s<=%d}' % (s2, len(s2)), s1[start:], flags=regex.BESTMATCH)
  return [1 - fuzzy.fuzzy_counts[0] / len(fuzzy[0]), fuzzy]

def identifyEPIYA(pro):
  isA = isB = isC = isD = False
  fuzzyA = fuzzyFind(pro, 'EPIYA[QK]VNKKK[AT]GQ')
  if fuzzyA[0] >= 0.85:
    print('<li><b>%s:</b> %s</li>' % ('EPIYA-A', fuzzyA[1][0]))
    isA = True
  elif fuzzyA[0] >= 0.65:
    print('<li>%s</li>' % 'Lai EPIYA-A')
  log('Matching Percentage: %.2f' % fuzzyA[0])
  
  fuzzyB = fuzzyFind(pro, 'EPIY[AT]QVAKKVNAKID')
  if fuzzyB[0] >= 0.85:
    print('<li><b>%s:</b> %s</li>' % ('EPIYA-B', fuzzyB[1][0]))
    isB = True
  elif fuzzyB[0] >= 0.65:
    print('<li>%s</li>' % 'Lai EPIYA-B')
  log('Matching Percentage: %.2f' % fuzzyB[0])
  
  fuzzyC = fuzzyFind(pro, 'EPIYATIDDLGQPFPLK')
  if fuzzyC[0] >= 0.85:
    print('<li><b>%s:</b> %s</li>' % ('EPIYA-C', fuzzyC[1][0]))
    isC = True
  elif fuzzyC[0] >= 0.65:
    print('<li>%s</li>' % 'Lai EPIYA-C')
  log('Matching Percentage: %.2f' % fuzzyC[0])
  
  fuzzyD = fuzzyFind(pro, 'EPIYATIDFDEANQAG')
  if fuzzyD[0] >= 0.85:
    print('<li><b>%s:</b> %s</li>' % ('EPIYA-D', fuzzyD[1][0]))
    isD = True
  elif fuzzyD[0] >= 0.65:
    print('<li>%s</li>' % 'Lai EPIYA-D')
  log('Matching Percentage: %.2f' % fuzzyD[0])
  
  if isA and isB and isC:
    print('<li><b>Origin: Western</b></li>')
  
  if isA and isB and isD:
    print('<li><b>Origin: East Asian</b></li>')

def identifys1s2(pro):
  start = fuzzyFind(pro, 'MEIQQTHRKINRP')
  if start[0] < 0.85:
    print('<li>Khong xac dinh duoc s1/s2</li>')
    return
  
  end = fuzzyFind(pro, 'AFFTTVII', start[1].start())
  if end[0] < 0.85:
    print('<li>Khong xac dinh duoc s1/s2</li>')
    return
  
  slen = end[1].start() - start[1].start() - len('MEIQQTHRKINRP')
  if slen <= 25:
    print('<li><b>s1</b></li>')
  else:
    print('<li><b>s2</b></li>')
  log('Matching Percentage: %.2f/%.2f' % (start[0], end[0]))

def identifym1m2(pro):
  matched = regex.search('LGKAVNL(?:R){s<=1}VDAHT(A[YN]FNGNIYLG){s<=10}', pro)
  if not matched:
    print('<li><b>m1</b></li>')
  else:
    percent = 1 - matched.fuzzy_counts[0] / len(matched[0])
    if percent >= 0.85:
      print('<li><b>m2</b></li>')
    elif percent >= 0.65:
      print('<li><b>Lai m1/m2</b></li>')
    log('Matching Percentage: %.2f' % percent)
    log('Matched sequence: %s' % matched[0])

def outputError(mess):
  print('Content-type:text/html')
  print('')
  print('<html>')
  print('<head>')
  print('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
  print('<title>HPDB - PTNK</title>')
  print('</head>')
  print('<body>')
  print('<h2>{}</h2>'.format(mess))
  print('</body>')
  print('</html>')

def main():
  #import sys
  #sys.stdout = open("test.html", "w")
  #jobid = 'Aug_29-4584919985'
  #jobid = 'Aug_31-5406644293'
  #jobid = 'Sep_3-3321946967'
  
  form = cgi.FieldStorage()
  jobid = form.getvalue('jobid')
  
  global DEBUG
  if form.getvalue('debug') == 'on':
    DEBUG = True
  else:
    DEBUG = False
  
  raw = getPredictResult(jobid)
  if raw == '0':
    outputError('The retrieve ID you provided is invalid, please check your input carefully.')
    return
  if raw == '1':
    outputError('The retrieve ID you provided is invalid, or that project was removed!')
    return
  if raw == '2':
    outputError('Your project is still processing, please wait a few minutes and try later.')
    return
  
  ind = findPredictionIndex(raw)
  cagaid = findGeneID(raw, 'cagA', ind)
  vacaid = findGeneID(raw, 'vacA', ind)
  
  print('Content-type:text/html')
  print('')
  print('<html>')
  print('<head>')
  print('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
  print('<title>HPDB - PTNK</title>')
  print('</head>')
  print('<body>')
  
  print('<h2><a href="http://www.mgc.ac.cn/cgi-bin/VFs/v5/main.cgi?JobID=%s">View full report on VFDB</a></h2>' % jobid)
  
  if cagaid[0] != '-':
    print('<h2><a href="http://www.mgc.ac.cn/cgi-bin/VFs/v5/v5/v5_predictGeneWin.pl?VFGID=%s&folder=%s">View report for cagA</a></h2>' % tuple(cagaid))
    caga = downloadGene(cagaid)
    print('<ul>')
    identifyEPIYA(caga[1])
    print('</ul>')
  else:
    print('<h2>No cagA found!</h2>')
  
  if vacaid[0] != '-':
    print('<h2><a href="http://www.mgc.ac.cn/cgi-bin/VFs/v5/v5/v5_predictGeneWin.pl?VFGID=%s&folder=%s">View report for vacA</a></h2>' % tuple(vacaid))
    vaca = downloadGene(vacaid)
    print('<ul>')
    identifys1s2(vaca[1])
    identifym1m2(vaca[1])
    print('</ul>')
  else:
    print('<h2>No vacA found!</h2>')
  
  print('</body>')
  print('</html>')

if __name__ == "__main__":
  main()