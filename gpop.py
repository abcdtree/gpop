#!/usr/bin/env python3

import os
import json
import argparse
import sys
import subprocess

def read_db_from_json(j_file):
    db_dict = {}
    with open(j_file, 'r') as f:
        db_dict = json.load(f)
    return db_dict

def save_json_to_file(j_file, db_dict):
    with open(j_file, 'w') as f:
        json.dump(db_dict, f)

def bash_command(cmd):
	p = subprocess.Popen(cmd, shell=True)
	while True:
		return_code = p.poll()
		if return_code is not None:
			break
	return

def find_name(info):
    all_info = info.split(";")
    gene_id, gene_name = "N/A", "N/A"
    for i in all_info:
        if "gene_id" in i:
            gene_id = i.split('"')[1]
        elif "gene_name" in i:
            gene_name = i.split('"')[1]
        elif "ID=" in i:
            gene_id = i.replace("ID=","")
        elif "Name=" in i:
            gene_name = i.replace("Name=","")
        else:
            continue
    return (gene_id, gene_name)

def create_annotation_dict(annofile):
    final_dict = {}
    with open(annofile , 'r') as myinput:
        for line in myinput:
            if line[0] == "#":
                continue
            info = line.strip().split("\t")
            #print(info)
            if len(info) > 2 and info[2] == "gene":
                chromesome = info[0]
                start = int(info[3])
                end = int(info[4])
                gene_info = info[8]
                gene_id, gene_name = find_name(gene_info)
                gene_list = final_dict.get(chromesome, [])
                gene_list.append([start, end, gene_id, gene_name])
                final_dict[chromesome] = gene_list
    return final_dict

def find_gene(chromesome, position, db):
    chrome_list = db.get(chromesome,[])
    if len(chrome_list) == 0:
        print(f"please check your chromesome input {chromesome}, no record of this chromesome in DB")
    else:
        for rec in chrome_list:
            start, end, gene_id, gene_name = rec
            if end < position:
                continue
            else:
                if start <= position:
                    print(chromesome, start, end, gene_id, gene_name)
                    continue
                else:
                    break
          

def main():
    parser = argparse.ArgumentParser(description="Main program description")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    parser_create = subparsers.add_parser("create", help="create annotation db")
    parser_pop = subparsers.add_parser("pop", help="return gene id with position input")
    parser_create.add_argument("annotation", help="Annotation gtf/gff files to create the db")
    parser_create.add_argument("-n", "--name", help="db name", default="test")
    parser_create.add_argument('-p', "--path", help="path to storage the db and config", default="/home/jianshu/gpfs/punim1068/db/gpop")
    parser_pop.add_argument("--db", help="db name to search the position")
    parser_pop.add_argument("chromesome", help="chromesome id", type=str)
    parser_pop.add_argument("position", help="position to check", type=int)
    parser_pop.add_argument("--path", '-p', default="/home/jianshu/gpfs/punim1068/db/gpop", help="path to storage the db and config")
    args = parser.parse_args()

    if args.command == "create":
        #print("running create part")
        anno_dict = {}
        if os.path.exists(args.annotation):
            try:
                anno_dict = create_annotation_dict(args.annotation)
            except:
                print(f"Error when create annotation db from {args.annotation}, please double check input format")
                sys.exit(1)
        else:
            print(f"{args.annotation} does not exist, please check your input file")
            sys.exit(1)
        db_path = args.path
        config_file = f"{db_path}/config.json"
        if os.path.exists(config_file):
            config_dict = read_db_from_json(config_file)
            config_dict["last"] = args.name
        else:
            config_dict = {
                    "db_path": db_path,
                    "last": args.name}
        save_json_to_file(config_file, config_dict)
        cmd = f"mkdir -p {db_path}/{args.name}"
        bash_command(cmd)
        save_path = f"{db_path}/{args.name}/db.json"
        save_json_to_file(save_path, anno_dict)
        print(f"Annotation db created as Name: {args.name}, at {save_path}")
        print(f"Run 'gpop pop --db {args.name} chromesome position' to query ")

    elif args.command == "pop":
    #else:
        #load config
        db_path = args.path
        config_file = f"{db_path}/config.json"
        default_db = "human"
        if os.path.exists(config_file):
            config_dict = read_db_from_json(config_file)
            default_db = config_dict["last"]
        else:
            print("no config file found, default db as human")
        current_db = ""
        if args.db:
            current_db = args.db
            config_dict['last'] = args.db
            save_json_to_file(config_file, config_dict)
        else:
            current_db = default_db
        db_file = f"{db_path}/{current_db}/db.json"
        if os.path.exists(db_file):
            db_dict = read_db_from_json(db_file)
            try:
                find_gene(args.chromesome, args.position, db_dict)
            except:
                print("Error when query in database, please check your db or input")
                sys.exit(1)

        else:
            print(f"Could not find {db_file} in current database")
            sys.exit(1)

    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
