#!/usr/bin/env python

__author__ = ('Jidong Lang (langjidong@hotmail.com)')
__version__ = 'v1.0'
__date__ = '4 April 2024'

import sys
import pandas as pd
from optparse import OptionParser

parser = OptionParser("%prog [options]")
parser.add_option("-i","--input", dest="input", default="", action="store", help="Txt File")
parser.add_option("-o","--output", dest="output", default="", action="store", help="Excel File")
(options, args) = parser.parse_args()

if not options.input:
    parser.print_help()
    sys.exit()

txt_file = options.input
# 读取txt文件
df = pd.read_csv(txt_file, sep='\t', na_values=['NA'])  # 根据你的txt文件分隔符来设置sep参数，如果是逗号分隔，则使用sep=','

excel_file = options.output
# 输出到Excel文件
df.to_excel(excel_file, index=False, na_rep='NA')