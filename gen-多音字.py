#!/usr/bin/env python3

import sys
import re
import subprocess

"""
本程序打印多音字 (不考虑声调不同; 只考虑声韵母不同的)
"""

ch_code_map = {}
prefix_map = {}
ch_with_short_code = {}  # 有简码的字

all_chars = []
with open('单字字频统计.txt') as f:
    for line in f.readlines():
        line = line.rstrip("\n")
        if line.startswith('#') or len(line) != 1:
            continue
        all_chars.append(line)


p = subprocess.run('{ ./gen-2.py; ./gen-3.py; } | sort', shell=True, text=True, capture_output=True)

for line in p.stdout.splitlines():
    if not re.match('^[a-z]', line):
        continue
    code, seq, ch = re.split('[,=]', line)
    if len(code) < 3:
        if (
                # 对于一简字, 仅统计首选字.
                (len(code) == 1 and int(seq) == 1)
                or len(code) == 2
                ):
            if ch not in ch_with_short_code:
                ch_with_short_code[ch] = []
            if len(code) == 2:
                ch_with_short_code[ch].append(code)

for line in p.stdout.splitlines():
    if not re.match('^[a-z]', line):
        continue
    code, seq, ch = re.split('[,=]', line)
    if len(code) < 3:
        continue
    if ch in ch_with_short_code:
        ch_with_short_code[ch].append(code)
    prefix = code[:3]
    if prefix not in prefix_map:
        prefix_map[prefix] = []
    if ch not in prefix_map[prefix]:
        prefix_map[prefix].append(ch)
    if ch not in ch_code_map:
        ch_code_map[ch] = []
    if prefix not in ch_code_map[ch]:
        ch_code_map[ch].append(prefix)

to_print = set()
for k, v in ch_code_map.items():
    if len(v) >= 2:
        if len(set([code[:2] for code in v])) == 1:
            # 读音 (声韵母) 相同, 只是拆字方案有多种; 不用处理.
            continue
        for pinyin in v:
            def get_index(ch):
                # 返回列表: 列表第一个元素表示是否存在, 第二个元素表示权重.
                # 2个值越小, 表示权重越高.
                if ch in all_chars:
                    return [0, all_chars.index(ch)]
                else:
                    # 这里使用 ch, 是为了让排序是稳定的 (即每次执行程序的结果是一样的).
                    return [1, ch]
            # 按照字频排序
            prefix_map[pinyin].sort(key=get_index)

            suffix = ''
            for ch in prefix_map[pinyin][:]:
                if ch in ch_with_short_code:
                    if len(ch_with_short_code[ch]) >= 2 and pinyin[:2] not in ch_with_short_code[ch]:
                        # 一/二简码字也是多音字, 且此读音不是其简码读音, 则添加后缀,
                        # 便于辅助判断优先级调整
                        suffix += f' {ch}:{sorted(ch_with_short_code[ch])}'
                    else:
                        # 一/二简码字不是多音字或者此读音是简码读音, 则从打印结果中排除;
                        # 这种结果我们额外在 ./4-to-3.py 中处理.
                        prefix_map[pinyin].remove(ch)

            if k not in prefix_map[pinyin]:
                # 简码字处理将此字去掉了; 这一行就无需处理了.
                continue

            if len(prefix_map[pinyin]) < 2:
                # 该前缀只有1个字的话, 就不用处理了.
                continue

            to_print.add('%s %s%s' % (pinyin, ''.join(prefix_map[pinyin]), suffix))

for i in sorted(list(to_print)):
    print(i)
