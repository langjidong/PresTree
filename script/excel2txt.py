#!/usr/bin/env python

__author__ = ('Jidong Lang (langjidong@hotmail.com)')
__version__ = 'v1.0'
__date__ = '4 April 2024'

import sys
import pandas as pd
from optparse import OptionParser

parser = OptionParser("%prog [options]")
parser.add_option("-i","--input", dest="input", default="", action="store", help="Excel File")
parser.add_option("-o","--output", dest="output", default="", action="store", help="Text File")
(options, args) = parser.parse_args()

if not options.input:
    parser.print_help()
    sys.exit()

# 读取Excel文件
#excel_file = '/Users/langjidong/Desktop/disease_gene_multi_source-2.xlsx'  # 替换为你的Excel文件名
excel_file = options.input
df = pd.read_excel(excel_file)

df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# 将数据写入TXT文件，使用制表符作为分隔符
#txt_file = '/Users/langjidong/Desktop/disease_gene_multi_source-2.txt'  # 输出的TXT文件名
txt_file = options.output
df.to_csv(txt_file, sep='\t', index=False, header=True)

print(f"Excel file has been successfully converted to {txt_file}")
