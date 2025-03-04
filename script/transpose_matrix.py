#!/usr/bin/env python

__author__ = ('Jidong Lang (langjidong@hotmail.com)')
__version__ = 'v1.0'
__date__ = '4 April 2024'

import sys
import pandas as pd
from optparse import OptionParser

parser = OptionParser("%prog [options]")
parser.add_option("-i","--input", dest="input", default="", action="store", help="Raw Matrix File")
parser.add_option("-o","--output", dest="output", default="", action="store", help="Transposed Matrix File")
(options, args) = parser.parse_args()

if not options.input:
    parser.print_help()
    sys.exit()

raw_matrix_file = options.input
df = pd.read_csv(raw_matrix_file, sep='\t', na_values=['0'], header=0)
df_transposed = df.transpose()
transposed_matrix_file = options.output
df_transposed.to_csv(transposed_matrix_file, sep='\t', index=True, header=False, na_rep=0, encoding='utf-8')
