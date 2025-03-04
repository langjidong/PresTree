#!/usr/bin/env python

__author__ = ('Jidong Lang (langjidong@hotmail.com)')
__version__ = 'v1.0'
__date__ = '27 June 2024'

import sys
from optparse import OptionParser

parser = OptionParser("%prog [options]")
parser.add_option("-i","--input", dest="input", default="", action="store", help="Raw Herbs File")
parser.add_option("-l","--lib", dest="lib", default="", action="store", help="Standardization Name File")
parser.add_option("-o","--output", dest="output", default="", action="store", help="Standardized File")
(options, args) = parser.parse_args()

if not options.input:
    parser.print_help()
    sys.exit()

input_file = options.input
lib_file = options.lib
output_file = options.output

def read_replacements(file_path):
    replacements = {}
    with open(file_path, 'r', encoding = 'utf-8') as file:
        for line in file:
            old, new = line.strip().split('\t')
            replacements[new] = old
    return replacements
  
def update_file1(file1_path, file2_path, output_path):
    replacements = read_replacements(file2_path)
    with open(file1_path, 'r', encoding='utf-8') as file1, open(output_path, 'w', encoding='utf-8') as outfile:
        for line in file1:
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                ingredients = parts[1].split('、')  # 假设成分之间用'、'分隔
                updated_ingredients = []
                for ingredient in ingredients:
                    for old, new in replacements.items():
                        if old == ingredient:
                            ingredient = ingredient.replace(old, new) 
                    updated_ingredients.append(ingredient)
                outfile.write(f"{parts[0]}\t{'、'.join(updated_ingredients)}\n")  
            else:  
                outfile.write(line)
  
update_file1(input_file, lib_file, output_file)

