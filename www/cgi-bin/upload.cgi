#!/usr/bin/env python

import cgi
import requests

def main():
  form = cgi.FieldStorage()
  if not form.getvalue('seqfile'):
    print('Content-Type:text/html')
    print('')
    print('<html>')
    print('<head>')
    print('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    print('<title>HPDB - PTNK</title>')
    print('</head>')
    print('<body>')
    print('<h2>Invalid</h2>')
    print('</body>')
    print('</html>')
    return
  
  data = {'option3-checkbox': 'on',
      'uGenus4F': 'Helicobacter',
      'uStrain4F': 'HP',
      'fileType': form.getvalue('fileType'),
      'email': 'hpdb.ptnk@gmail.com'}
  file = {'seqfile': form['seqfile'].file}
  res = requests.post('http://www.mgc.ac.cn/cgi-bin/VFs/v5/v5/v5_form4pipeline.pl', data=data, files=file).text
  
  if "'success':false" in res:
    print('Status: 400 Bad Request')
    start = res.index("'error':'") + len("'error':'")
    end = res.index("'}", start)
  else:
    start = res.index('Your job id: ') + len('Your job id: ')
    end = res.index('. After finishing this job', start)
  
  print('Access-Control-Allow-Origin: *')
  print('Content-Type:text/html')
  print('')
  print(res[start:end])

if __name__ == "__main__":
  main()