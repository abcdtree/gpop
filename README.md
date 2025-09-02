# gpop
return a gene id based on chromosome and position

## installation

```
    git clone https://github.com/abcdtree/gpop.git
    gpop/gpop.py -h
```

## create database

```
    gpop.py create -n human human.gff
```

## query gene by chromesome and position

```
    gpop.py pop --db human 1 25000
```

## handle output from npTranscript

```
    #works on 3 types of npTranscript output
    gpop.py np --db human join.fa.gz --output join.tab
    gpop.py np --db human overlap.fa.gz #print to screen if no output parameter
    gpop.py np --db ferret nogap.fa.gz --output nogap.tab 
    gpop.py np --db human --all all.fa.gz --output all.tab
```
