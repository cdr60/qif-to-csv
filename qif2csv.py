#!/usr/bin/python3
import argparse
import csv
import os
import sys
from collections import OrderedDict


def parse_lines(lines, config, options=None):
    if not options:
        options = {}
    res = []
    transaction = OrderedDict()
    for (idx, line) in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        field_id = line[0]
        if field_id == '^':
            if transaction:
                res.append(transaction)
            transaction = OrderedDict([])
        elif field_id in list(config["FIELDS"].keys()):
            transaction[config["FIELDS"][field_id]] = line[1:]
        elif line:
            transaction['%s' % idx] = line

    if len(list(transaction.keys())):
        res.append(transaction)

    # post-check to not interfere with present keys order
    for t in res:
        for field in list(config["FIELDS"].values()):
            if field not in t:
                t[field] = None
        t['filename'] = options.get('src', '')
    return res


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Convert MS Money files to CSV')
    parser.add_argument("infile", type=argparse.FileType(
        'r' , encoding='latin-1'), help="File to convert to CSV")
    parser.add_argument("-o", "--output", help="Output file",
                        type=argparse.FileType('w'))
    args = parser.parse_args()

    f = args.output if args.output else sys.stdout
    writer = csv.writer(f, dialect='excel')
    writer.writerow(['Date Time', 'Comment', 'Amount', 'Ref Number'])

    config = {
        "FIELDS": {'D': 'date', 'T': 'amount', 'P': 'payee', 'L': 'category',
                   'N': 'number', 'M': 'memo'},
        "EXTRA_FIELDS": {'F': 'filename'}
    }

    _, filename = os.path.split(args.infile.name)

    for transaction in parse_lines(args.infile.readlines(), config, options={'src': filename}):
        #print(transaction)
        amount=transaction.get("amount", "").replace(",","")
        dt=transaction.get("date", "")
        if ((dt[2:3]=="/") and (dt[5:6]=="'")): dt=dt[0:2]+"/"+dt[3:5]+"/"+dt[6:11]
        writer.writerow([dt, amount, transaction.get("payee", ""), transaction.get("category", ""), transaction.get("number", "")])

    args.infile.close()
    if args.output:
        args.output.close()
        
