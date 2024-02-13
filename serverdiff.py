#!/usr/bin/env python

"""
To compare the server's ansible facts against a template or standard build

Usage:
    serverdiff.py [options] FACTS1 FACTS2

Options:
    --format=<type>    Report format either in json or csv [default: json].
    --help             Show the usage.
"""

import sys
import json
import pprint
import csv
from docopt import docopt
from deepdiff import DeepDiff

exclude_items = ["root['ansible_facts']['env']['LS_COLORS']",
                ]

def load_json_facts(file):
    try:
        with open(file, 'r') as f:
            data = f.read()
            f_json = json.loads(data)
            return f_json
    except Exception as e:
        print('Failed to read the file: {}'.format(e))
        sys.exit(1)

def report_to_csv(d):
    print('creating csv report...')
    with open('report.csv', 'w', newline='') as csvfile:
        fieldnames = ['values_changed', 'old_value', 'new_value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for key, value in d.items():
            old_value = value.get('old_value')
            new_value = value.get('new_value')
            writer.writerow({'values_changed': key, 'old_value': old_value, 'new_value': new_value})

    
def main():
    f1 = load_json_facts(facts1)
    f2 = load_json_facts(facts2)

    diff_output = DeepDiff(f1,f2, exclude_paths=exclude_items)
    diff_output_dict = diff_output.to_dict()
    values_changed = diff_output_dict.get('values_changed')
    
    if format_type == 'csv':
        report_to_csv(values_changed)
    else:
        pprint.pprint(values_changed, indent=2)


# TODO
# organize the code into a class
# print raw report in json (default) in stdout
# print report in csv , create an output file
# create an exclude list

if __name__ == '__main__':
    opts = docopt(__doc__)
    format_type = opts['--format']
    facts1 = opts['FACTS1']
    facts2 = opts['FACTS2']

    main()





