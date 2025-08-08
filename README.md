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
