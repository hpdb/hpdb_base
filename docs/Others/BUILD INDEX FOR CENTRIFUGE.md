# Buid index for Centrifuge

1. Make sure you have Centrifuge installed

2. Move to the `database` folder
```
cd ~/database
```

3. Download the NCBI taxonomy to `taxonomy` and helicobacter pylori genomes to `refseq`
```
centrifuge-download -o taxonomy taxonomy
centrifuge-download -o refseq -d "bacteria" -a "Any" -t 210 refseq >> seqid2taxid.map
```

4. Concatenate all downloaded sequences into a single file
```
cat refseq/*/*.fna > input-sequences.fna
```

5. Build centrifuge index:
```
centrifuge-build -p `nproc --all` --conversion-table seqid2taxid.map \
                                  --taxonomy-tree taxonomy/nodes.dmp \
                                  --name-table taxonomy/names.dmp \
                                  input-sequences.fna hp
```

## Run Centrifuge
```
centrifuge -f -p `nproc --all` -x ~/database/hp -U input.fasta --report-file cf.csv
```