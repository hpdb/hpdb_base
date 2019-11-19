import requests
import csv

url = "https://helicobacter.biocyc.org/get-organisms-json"

resp = requests.get(url=url)
data = resp.json()
filtered = [x for x in data if 'Helicobacter pylori' in x['label']]

keys = filtered[0].keys()
with open('biocyc.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(filtered)