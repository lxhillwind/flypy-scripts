#!/usr/bin/env python3

import sys
import subprocess
import re

if sys.stdin.isatty():
    print('''
用途:
    检查是否有重复或不连续编码.

使用方式:
    将码表数据作为标准输入.
    (例如: 在 vim 中, 执行 %Sh -t ./check-duplicate.py; 因为文件不是 utf-8 编码的, 不能直接 cat 导入)
          ''')
    sys.exit(1)


p = subprocess.run('cat', shell=True, text=True, capture_output=True)

code_map = {}

for line in p.stdout.splitlines():
    if not re.match('^[a-z]', line):
        continue
    code, seq, ch = re.split('[,=]', line)
    seq = int(seq)
    if code not in code_map:
        code_map[code] = []
    if seq in code_map[code]:
        print('duplicate:', code, seq, ch)
    else:
        code_map[code].append(seq)

for k, v in code_map.items():
    v.sort()
    if len(v) == 1:
        # max / min 的参数不能只有1个数字.
        continue
    if max(*v) - min(*v) != len(v) - 1:
        print('inconsistent:', k, v)
