#!/usr/bin/env python3

"""
处理 ./搜狗拼音win版自定义短语.ini, flypy_plus.txt, flypy_extra.txt, 生成全码字 (seq 缺失).
"""

import re


flypy_chars = set()


additional_data = r'''
# 只有一简码或者二简码
keue,-1=克
yivr,-1=以
tddd,-1=太
'''.strip().splitlines()


def handle_line(line):
    line = line.strip()
    if not line or re.match('^[;#]', line):
        return

    if len(line) > len('xxxx,nn=c'):
        # otherwise re.split may raise.
        return
    code, seq, ch = re.split('[,=]', line)
    if len(code) < 3:
        return
    if len(ch) > 1:
        return
    if re.match('^o[^mou]', code):
        return
    i = (code, seq, ch)
    print(f'{i[0]},{i[1]}={i[2]}')
    flypy_chars.add(ch)


with open('搜狗拼音win版自定义短语.ini') as f:
    for line in f.readlines():
        handle_line(line)

for line in additional_data:
    handle_line(line)

with open('flypy_plus.txt') as f:
    for line in f.readlines():
        line = line.strip()
        if line.startswith('#') or not line:
            continue
        ch, code = re.split('[\t ]', line)
        if len(code) < 3:
            continue

        i = (code, -1, ch)
        print(f'{i[0]},{i[1]}={i[2]}')
        flypy_chars.add(ch)

# 2024-08-15: 加入对 flypy_extra.txt 的处理;
# 注意, 这天将字频 / 多音字的处理改成从 rime-ice / rime-frost 获取元信息.
with open('flypy_extra.txt') as f:
    for line in f.readlines():
        line = line.strip()
        if line.startswith('#') or not line:
            continue
        ch, code = re.split('[\t ]', line)
        if len(code) < 3:
            continue

        i = (code, -1, ch)
        print(f'{i[0]},{i[1]}={i[2]}')
        flypy_chars.add(ch)


# 2024-08-21: 加入对 libre-flypy.txt 的处理;
# 以 flypy_plus / flypy_extra 为准, 因此引入变量 flypy_chars.
with open('libre-flypy.txt') as f:
    for line in f.readlines():
        line = line.strip()
        arr = re.match('^(.)\t([a-z]+)$', line)
        if not arr:
            continue
        ch, code = arr.groups()
        if len(code) < 3:
            continue

        i = (code, -1, ch)
        if ch not in flypy_chars:
            print(f'{i[0]},{i[1]}={i[2]}')
