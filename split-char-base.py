#!/usr/bin/env python3

"""
根据 IDS-UCS-*.txt 文件, 将单字拆分为多个字.

此程序的作用是输出没有找到对应拼音的组件.
"""

import re
import os
import subprocess
import copy

all_element = {}

# element_translate 是从 split-char-base.py 生成的, 然后手动去掉不想用的, 再为剩下的补上替换字.
# 多次迭代执行, 就能让 ./split-char-base.py 的输出尽量少.
with open('./split-char-element.txt') as f:
    element_translate = f.read()
element_translate = element_translate.strip().splitlines()
element_translate = {i[0]: i[1:] for i in element_translate if len(i) >= 2}

element_with_pinyin = {}
p = subprocess.run('python3 ./gen-3.py | sort', shell=True, text=True, capture_output=True)
for line in p.stdout.splitlines():
    if not re.match('^[a-z]', line):
        continue
    code, _, ch = re.split('[,=]', line)
    if len(code) < 2:
        continue
    element_with_pinyin[ch] = code[:2]

os.chdir(os.path.expanduser('~/repos/chise-ids'))

def handle_fp(f):
    for line in f.readlines():
        if not re.match(r'^U\+', line):
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
        if ch == element:
            continue
        for el in element:
            if el in element_translate:
                el = element_translate[el]
            if el not in all_element:
                all_element[el] = 0
            all_element[el] += 1


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

for k, v in copy.copy(all_element).items():
    # 如果出现次数过低, 就忽略它.
    if v < 20:
        del all_element[k]

# helper
def get_element_without_pinyin():
    result = []
    for ch_ in all_element:
        # ch_: ./split-char-element.txt 中一个字可能对应多个字.
        for ch in ch_:
            if ch not in element_with_pinyin:
                result.append(ch_)
                break
    return result


print(''.join(get_element_without_pinyin()))
