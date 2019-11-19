import csv
with open('merged.csv') as f:
    reader = csv.reader(f)
    with open('output.csv', 'w') as g:
        writer = csv.writer(g)
        for row in reader:
            if row[0] == 'Helicobacter pylori':
                new_row = [' '.join([row[0], row[1]])] + row[2:]
            else:
                new_row = [row[0]] + row[2:]
            writer.writerow(new_row)