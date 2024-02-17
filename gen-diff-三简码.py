#!/usr/bin/env python3

"""
统计我们根据字频生成的三简码 (./4-to-3.py) 和官方的三简码数据 (./搜狗拼音win版自定义短语.ini)
有什么区别; 以及, 是否我们需要调整.
(排除掉一简码和二简码的)
(目前也排除了全码靠前的字; 可以视工作量将其取消排除掉.)

(调整的结果直接补充到 ./fixed-encoding.txt 中)

TODO: 来源程序变更, 导致 codes_map / codes_map_ours 可能需要调整.
"""

import subprocess
import re

codes_map = {}
codes_map_ours = {}

character_with_short_code = set()
character_with_full_code = set()


p = subprocess.run('{ ./gen-2.py; ./gen-3.py; ./gen-4.py; } | sort', shell=True, text=True, capture_output=True)
for line in p.stdout.splitlines():
    if not re.match('^[a-z]', line):
        continue
    code, seq, ch = re.split('[,=]', line)
    if len(ch) != 1:
        continue
    if len(code) == 1 and int(seq) == 1:
        character_with_short_code.add(ch)
    if len(code) == 2 and int(seq) < 3:
        character_with_short_code.add(ch)
    if len(code) == 4 and int(seq) <= 2:
        character_with_full_code.add(ch)
    if len(code) != 3:
        continue
    if code not in codes_map:
        codes_map[code] = {}
    codes_map[code][seq] = ch

    if code not in codes_map_ours:
        codes_map_ours[code] = {}
    codes_map_ours[code][seq] = ch

for code, values in codes_map.items():
    for k, v in values.items():
        if v in character_with_short_code:
            continue
        if v in character_with_full_code:
            continue
        if codes_map_ours[code].get('1') == v or codes_map_ours[code].get('2') == v:
            # 首选或次选字匹配上了, 还是不管.
            continue
        print(f'{code} seq={k}: old: {v}; new: {codes_map_ours[code]}')
