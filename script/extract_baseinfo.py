#!/usr/bin/env python

__author__ = ('Jidong Lang (langjidong@hotmail.com)')
__version__ = 'v1.0'
__date__ = '22 May 2024'

import sys
from optparse import OptionParser
import re

parser = OptionParser("%prog [options]")
parser.add_option("-i","--input", dest="input", default="", action="store", help="Tree Log File")
parser.add_option("-c","--cutoff", dest="cutoff", default="", action="store", help="Cutoff Value of Pvalue")
parser.add_option("-o","--output", dest="output", default="", action="store", help="Baseinfo File")
(options, args) = parser.parse_args()

if not options.input:
    parser.print_help()
    sys.exit()

log_file = options.input
cutoff_value = options.cutoff
baseinfo_file = options.output

with open(log_file, 'r', encoding='utf-8') as file:
    content = file.read()

match = re.search(r'Analyzing sequences(.*?)\n(.*?)\*(.*?)TOTAL', content, re.DOTALL)

if match:
    result = match.group(2)
    print('Match found.')
    print(result)

    with open(baseinfo_file, 'w', encoding='utf-8') as outfile:
        #filter_lines = []
        lines = result.strip().split('\n')
        print('Filtered result:')
        for line in lines:
            columns = line.strip().split()
            if len(columns) == 5:
                try:
                    value = float(columns[4].replace('%',''))/100
                    if value <= float(cutoff_value):
                        #filter_lines.append(line)
                        filter_result = line.strip()
                        print(filter_result)
                        outfile.write(columns[1] + '\t' + '1' + '\n')
                except ValueError:
                    pass

else:
    print("No match found.")

