import csv
with open('data.csv') as f:
    reader = csv.reader(f)
    with open('output.csv', 'w') as g:
        writer = csv.writer(g)
        for row in reader:
            new_row = row
            if row[0] != 'Name':
                new_row[17] += '/' + row[1]
            writer.writerow(new_row)