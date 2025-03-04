#!/usr/bin/env python

__author__ = ('Jidong Lang (langjidong@hotmail.com)')
__version__ = 'v1.0'
__date__ = '22 May 2024'

import sys
from optparse import OptionParser
import re
import os
import numpy as np

parser = OptionParser("%prog [options]")
parser.add_option("-a","--all", dest="all", default="", action="store", help="All Info File")
parser.add_option("-b","--base", dest="base", default="", action="store", help="Base Info File")
parser.add_option("-o","--output", dest="output", default="", action="store", help="Prescription Similarity Result")
(options, args) = parser.parse_args()

if not options.all:
    parser.print_help()
    sys.exit()

allinfo_file = options.all
baseinfo_file = options.base
presim_info = options.output

id_dict = {}
column_sums = [0]

with open(allinfo_file, 'r', encoding='utf-8') as file1:
    cal_info = []
    file1 = file1.readlines()
    for line in file1[1:]:
        parts = line.strip().split('\t', 1)
        if parts:
            id_value = parts[0]
            id_dict[id_value] = parts[1]

with open(baseinfo_file, 'r', encoding='utf-8') as file2, open('tmp.txt', 'w', encoding='utf-8') as file3:
    file3.write(f'Herbs_Name\tBase_Prescription\n')
    for id_value, _ in id_dict.items():
        found_in_second = False
        for line in file2:
            parts = line.strip().split('\t', 1)
            if parts[0] == id_value:
                id_dict[id_value] =1
                found_in_second = True
                break
        if not found_in_second:
            id_dict[id_value] = 0
        file3.write(f'{id_value}\t{id_dict[id_value]}\n')

os.system(f'awk -F \"\\t\" \'{{print $2}}\' tmp.txt > tmp_1.txt')
os.system(f'paste {allinfo_file} tmp_1.txt > tmp.txt')
os.system(f'rm -rf tmp_1.txt')

column_sums = {}
column_multi_sums = {}
name_info = []
with open('tmp.txt', 'r', encoding='utf-8') as file4, open(presim_info, 'w', encoding='utf-8') as file5:
    first_line = file4.readline().strip()
    if first_line:
        columns = first_line.split('\t')
        for i, _ in enumerate(columns):
            column_sums[i] = 0
            column_multi_sums[i] = 0
            name_info.append(columns[i])
        #print(name_info)
    
    for line in file4:
        columns = line.strip().split('\t')
        for i, column in enumerate(columns[1:]):
            try:
                column_sums[i] += float(column) * float(column)
                column_multi_sums[i] += float(column) * float(columns[-1])
            except ValueError:
                pass
    print(column_sums.items())
    print(column_multi_sums.items())

    result_dict = {}

    for key in column_multi_sums:
        if key in column_sums and column_sums[len(column_sums)-1] != 0:
            result_dict[key] = column_multi_sums[key] / (np.sqrt(column_sums[key]) * np.sqrt(column_sums[len(column_sums)-1]))
        else:
            pass

    for j, result_value in result_dict.items():
        #print(f'{name_info[j]}\t{result_value:.2f}')
        file5.write(f'{name_info[j]}\t{result_value:.2f}\n')

os.system(f'rm -rf tmp.txt')
