#!/usr/bin/env python3

"""
根据 IDS-UCS-*.txt 文件, 将单字拆分为多个字.

输入编码统一以 o 开头 (以避免干扰词组的输入):

例如, 要输入 "䐜", 可以输入 "o yt (月) vf (真)", 即 "oytvf".
"""

import re
import os
import subprocess
import copy
import sys

def eprint(*args):
    print(*args, file=sys.stderr)

all_element = {}

with open('./split-char-element.txt') as f:
    element_translate = f.read()
element_translate = element_translate.strip().splitlines()
element_translate = {i[0]: i[1:] for i in element_translate if len(i) >= 2}

element_with_pinyin = {}
full_codes_priority = {}
p = subprocess.run('{ ./gen-2.py; ./gen-3.py; ./gen-4.py; } | sort', shell=True, text=True, capture_output=True)
for line in p.stdout.splitlines():
    if not re.match('^[a-z]', line):
        continue
    code, seq, ch = re.split('[,=]', line)
    if len(ch) != 1:
        continue
    if len(code) < 2:
        continue
    if ch not in element_with_pinyin:
        element_with_pinyin[ch] = set()
    # 考虑多音字.
    element_with_pinyin[ch].add(code[:2])
    if len(code) == 4:
        seq = int(seq)
        # 考虑到部分输入法并不能总是遵守优先级设置, 我们将拆分输入的编码统一添加一个字母 (o) 作为前缀;
        # 如果不这么做的话, 词组输入就会很不自然: 例如: mudi (目的), yige (一个),
        # 它们对应的拆分输入编码是有很多的, 而且搜狗输入法会将这些编码排在词组前面.
        #
        # 既然添加了前缀, 这里就没有必要从小鹤的码表里导入码表优先级数据了.
        # if code not in full_codes_priority:
        #     full_codes_priority[code] = seq
        # if seq > full_codes_priority[code]:
        #     full_codes_priority[code] = seq

os.chdir(os.path.expanduser('~/repos/chise-ids'))

def handle_fp(f):
    for line in f.readlines():
        if not re.match(r'^U[+-]', line):
            continue
        line = line.rstrip('\n')
        _, ch, element = line.split('\t', maxsplit=2)
        if '&' in element:  # like: "U+FA1F	﨟	⿱艹&M-29726;"
            # TODO 处理这种情况.
            continue
        if '\t' in element:
            element = element.split('\t')[0]
        # TODO 添加更多这种组件
        element = re.sub('[⿰⿱⿺⿲⿳⿴⿵⿶⿷⿸⿹⿻]', '', element)
        if len(element) < 2:
            continue
        if not element:
            continue

        skip = False
        new_code = ['']
        for el in element[:]:
            if el in element_translate:
                element = element.replace(el, element_translate[el], -1)
                el_new = element_translate[el]
            else:
                el_new = el

            # el_new 可能是一个组件, 也可能是多个.
            for el in el_new:
                if el not in element_with_pinyin:
                    eprint('element not common, skip:', ch, el)
                    skip = True
                    break

                pinyin = element_with_pinyin[el]
                new_code_tmp = new_code[:]
                new_code = []
                for i in pinyin:
                    for j in new_code_tmp:
                        new_code.append(f'{j}{i}')

        if not skip:
            for code in new_code:
                seq = 1
                if code not in full_codes_priority:
                    full_codes_priority[code] = seq
                else:
                    seq = full_codes_priority[code] + 1
                    full_codes_priority[code] = seq
                i = (code, seq, ch)
                # 打印示例: uzbk,3=拼
                print(f'o{i[0]},{i[1]}={i[2]}')
            # 打印示例: 拼 手并 ['uzbk']
            #print(ch, element, new_code)

for file in [
    'IDS-UCS-Basic.txt',
    'IDS-UCS-Ext-A.txt',
    'IDS-UCS-Compat.txt',
    'IDS-UCS-Ext-B-1.txt',
    'IDS-UCS-Ext-B-2.txt',
    'IDS-UCS-Ext-B-3.txt',
    'IDS-UCS-Ext-B-4.txt',
    'IDS-UCS-Ext-B-5.txt',
    'IDS-UCS-Ext-B-6.txt',
    'IDS-UCS-Compat-Supplement.txt',
    'IDS-UCS-Ext-C.txt',
    'IDS-UCS-Ext-D.txt',
    'IDS-UCS-Ext-E.txt',
    'IDS-UCS-Ext-F.txt',
    'IDS-UCS-Ext-G.txt',
    'IDS-UCS-Ext-H.txt',
        ]:
    with open(file) as f:
        handle_fp(f)
