#!/usr/bin/env python

__author__ = ('Jidong Lang (langjidong@hotmail.com)')
__version__ = 'v1.0'
__date__ = '25 June 2024'

import sys
import pandas as pd
from optparse import OptionParser
from pypinyin import pinyin, Style

parser = OptionParser("%prog [options]")
parser.add_option("-i","--input", dest="input", default="", action="store", help="Hanzi Excel File")
parser.add_option("-o","--output", dest="output", default="", action="store", help="Pinyin Excel File")
(options, args) = parser.parse_args()

if not options.input:
    parser.print_help()
    sys.exit()

hanzi_excel_file = options.input
df = pd.read_excel(hanzi_excel_file)

df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

pinyin_list = []
for cell in df['方剂组成']:
    # 如果单元格不是空，则进行转换
    if not pd.isnull(cell):
        chinese_words = cell.split('、')
        pinyin_words = []
        for word in chinese_words:
            # 使用pypinyin库将汉字转换为拼音，并设置为无声调
            pinyin_word = ''.join([p[0] for p in pinyin(word, style=Style.NORMAL)])
            #print(pinyin_word)
            pinyin_words.append(pinyin_word)
        pinyin_list.append(pinyin_words)
    else:
        # 如果单元格为空，则添加空字符串
        pinyin_list.append('')

pinyin_list_1 = []
for cell1 in df['方剂']:
    # 如果单元格不是空，则进行转换
    if not pd.isnull(cell1):
        pinyin_words_1 = []
        for word1 in cell1:
            # 使用pypinyin库将汉字转换为拼音，并设置为无声调
            pinyin_word_1 = ''.join([p1[0] for p1 in pinyin(word1, style=Style.NORMAL)])
            pinyin_words_1.append(pinyin_word_1)
        pinyin_list_1.append(pinyin_words_1)
    else:
        # 如果单元格为空，则添加空字符串
        pinyin_list_1.append('')

# 将转换后的拼音列表列表（二维列表）转换为DataFrame的列;这里使用列表推导式和join函数将每个单元格的拼音列表合并为一个用空格分隔的字符串
df['Pinyin_Column_1'] = [''.join(map(str, pinyin_words_1)) for pinyin_words_1 in pinyin_list_1]
df['Pinyin_Column'] = ['、'.join(map(str, pinyin_words)) for pinyin_words in pinyin_list]
df = df.drop(columns=['方剂'])
df = df.drop(columns=['方剂组成'])
df = df.rename(columns={'Pinyin_Column_1': '方剂'})
df = df.rename(columns={'Pinyin_Column': '方剂组成'})

pinyin_excel_file = options.output
df.to_excel(pinyin_excel_file, index=False)

print(f"Excel file has been successfully converted to {pinyin_excel_file}")
