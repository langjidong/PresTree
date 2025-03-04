#!/usr/bin/env python

__author__ = ('Jidong Lang (langjidong@hotmail.com)')
__version__ = 'v1.0'
__date__ = '24 May 2024'

import sys
import os
from optparse import OptionParser

parser = OptionParser("%prog [options]")
parser.add_option("-b","--base", dest="base", default="", action="store", help="Baseinfo File")
parser.add_option("-d","--dir", dest="dir", default="", action="store", help="Dir Name")
parser.add_option("-o","--output", dest="output", default="", action="store", help="Text File")
(options, args) = parser.parse_args()

if not options.base:
    parser.print_help()
    sys.exit()

base_file = options.base
dir_file = options.dir
output_file = options.output

total_matched_files = 0
total_files = 0

for root, dirs, files in os.walk(dir_file):
    for file in files:
        if file.endswith('.txt'):
            file_path = os.path.join(root, file)
            total_files += 1
            
            count = 0
            with open(base_file, 'r', encoding='utf-8') as file1:
                keys = set(line.strip().split('\t')[0] for line in file1)

            with open(file_path, 'r', encoding='utf-8') as file2:
                for line in file2:
                    line = line.strip().split('\t')[0]
                    if line in keys:
                        count += 1
            if(len(keys) == count):
                total_matched_files += 1

print(total_matched_files)
print(total_files)
with open(output_file, 'w', encoding='utf-8') as outputfile:
    result = total_matched_files / total_files
    outputfile.write('Goodness of fit: ' + f'{result:.2f}' + '\n')
print('Goodness of fit: ' + f'{result:.2f}')
