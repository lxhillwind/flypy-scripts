#!/usr/bin/env python3

import sys
import re
import subprocess

"""
本程序打印没有简码的全码次选字, 用于辅助判断全码是否需要做调整
(例如, 是否将 mmgg (魔) 的首选字改为 魔, 而不是非常用词)

目前结果: 根据 ./单字字频统计.txt,
- 全部计入: 一共有 336 个字.
- 仅前 3000: 81 个字.
- 仅前 1000: 7 个字 (一共 13 个; 其他的是非常见读音).
(引入 ./handle-flypy-plus-data.py 的数据之前统计的; 不过引入后, 结果也差不了一两百)

(目前考虑, 还是不调整全码.)
"""

ch_code_map = {}
check_ch = set()  # 常用字

# 最大不会超过 10000 个字.
limit = 10000 if len(sys.argv) == 1 else int(sys.argv[1])
p = subprocess.run(f'head -n {limit} ./单字字频统计.txt', shell=True, text=True, capture_output=True)
for line in p.stdout.splitlines():
    if not re.match('^.$', line):
        continue
    check_ch.add(line)


p = subprocess.run('{ ./gen-2.py; ./gen-3.py; ./gen-4.py; } | sort | uniq', shell=True, text=True, capture_output=True)
for line in p.stdout.splitlines():
    if not re.match('^[a-z]', line):
        continue
    code, seq, ch = re.split('[,=]', line)
    if len(ch) != 1:
        continue
    if ch not in check_ch:
        continue
    seq = int(seq)
    if ch not in ch_code_map:
        ch_code_map[ch] = {}
    # 仅当值不存在或者大于 seq 时才更新.
    if ch_code_map[ch].get(len(code), 100) > seq:
        ch_code_map[ch][len(code)] = seq

for line in p.stdout.splitlines():
    if not re.match('^[a-z]', line):
        continue
    code, seq, ch = re.split('[,=]', line)
    seq = int(seq)
    if ch not in check_ch:
        continue
    if len(code) == 4:
        if ch in ch_code_map and (
                ch_code_map[ch].get(1, 100) < 3
                or ch_code_map[ch].get(2, 100) < 3
                or ch_code_map[ch].get(3, 100) < 3
                ):
            continue
        if seq != 1:
            print(line)
