#!/usr/bin/env python

__author__ = ('Jidong Lang (langjidong@hotmail.com)')
__version__ = 'v1.0'
__date__ = '23 May 2024'

import sys
from optparse import OptionParser

parser = OptionParser("%prog [options]")
parser.add_option("-i","--input", dest="input", default="", action="store", help="Merge File List")
parser.add_option("-d","--dir", dest="dir", default="", action="store", help="Merge File Dirname")
parser.add_option("-o","--output", dest="output", default="", action="store", help="Merged File")
(options, args) = parser.parse_args()

if not options.input:
    parser.print_help()
    sys.exit()

mergelist_file = options.input
mergefile_dir = options.dir
merged_file = options.output

filelist_info = []

with open(mergelist_file, 'r', encoding='utf-8') as input:
    for line in input.readlines():
        full_path = mergefile_dir + line.strip() + '.tmp2'
        #print(full_path)
        filelist_info.append(full_path)

columns = []

for file_info in filelist_info:
    with open(file_info, 'r', encoding='utf-8') as f:
        columns.append([line.strip() for line in f.readlines()])
        #for line in f.readlines():
            #columns.append(line.strip())

min_length = min(len(column) for column in columns)

with open(merged_file, 'w', encoding='utf-8') as output:
    for i in range(min_length):
        row = '\t'.join(column[i] for column in columns)
        output.write(row + '\n')
