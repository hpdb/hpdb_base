import csv
from htmldom import htmldom

ncbi = []

def checkPage(page):
    dom = htmldom.HtmlDom('https://www.ncbi.nlm.nih.gov/genomes/Genome2BE/genome2srv.cgi?action=GetGenomes4Grid&genome_id=169&genome_assembly_id=&king=Bacteria&mode=2&flags=1&page=' + str(page) + '&pageSize=1000')
    dom = dom.createDom()
    
    rows = dom.find('tr')    
    for row in rows:
        cols = row.find('td')
        try:
            ncbi.append({'id': cols[0].find('a').attr('href')[31:], 'assembly': cols[4].text().strip()})
        except Exception:
            pass  # or you could use 'continue'

if __name__ == "__main__":
    for page in range(1, 16):
        checkPage(page)
    keys = ncbi[0].keys()
    with open('ncbi.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(ncbi)