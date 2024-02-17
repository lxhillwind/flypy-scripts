#!/usr/bin/env python3

import re
import subprocess

p = subprocess.run('python3 ./gen-2.py', shell=True, text=True, capture_output=True)

code_map = {}

for line in p.stdout.splitlines():
    if not re.match('^[a-z]', line):
        continue
    code, seq, ch = re.split('[,=]', line)
    if len(code) > 2:
        continue
    seq = int(seq)
    if code not in code_map:
        code_map[code] = seq
    if seq > code_map[code]:
        code_map[code] = seq

for k, v in code_map.items():
    print(f'{k},{v+1}=|')
