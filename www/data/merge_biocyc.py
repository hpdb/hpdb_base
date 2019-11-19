import csv
from difflib import SequenceMatcher
from heapq import nlargest as _nlargest

def get_close_matches_indexes(word, possibilities, n=3, cutoff=0.6):
    if not n >  0:
        raise ValueError("n must be > 0: %r" % (n,))
    if not 0.0 <= cutoff <= 1.0:
        raise ValueError("cutoff must be in [0.0, 1.0]: %r" % (cutoff,))
    result = []
    s = SequenceMatcher()
    s.set_seq2(word)
    for idx, x in enumerate(possibilities):
        s.set_seq1(x)
        if s.real_quick_ratio() >= cutoff and \
           s.quick_ratio() >= cutoff and \
           s.ratio() >= cutoff:
            result.append((s.ratio(), idx))
    
    # Move the best scorers to head of list
    result = _nlargest(n, result)
    
    # Strip scores for the best n matches
    return [x for score, x in result]

with open('biocyc.csv') as f:
    reader = csv.reader(f)
    raw = list(reader)

ids = [x[0] for x in raw]
label = [x[1] for x in raw]

with open('data.csv') as f:
    reader = csv.reader(f)
    with open('output.csv', 'w') as g:
        writer = csv.writer(g)
        for row in reader:
            if row[0] == 'Name':
                new_row = row + ['BioCYC ID']
            else:
                id = get_close_matches_indexes(row[0], label, n=1, cutoff=0.95)
                if len(id) == 1:
                    new_row = row + [ids[id[0]]]
                else:
                    new_row = row + ['']
            writer.writerow(new_row)