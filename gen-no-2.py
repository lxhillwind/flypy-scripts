#!/usr/bin/env python3

"""
生成没有二简码的组合.
"""

import re
import subprocess

all_possible_codes = set()
all_available_codes = set()

res = subprocess.run('{ python3 ./gen-3.py; } | sort', shell=True, text=True, capture_output=True)
if True: # keep indent with last version of this file.
    for line in res.stdout.split('\n'):
        line = line.rstrip("\n")
        if not line or re.match('^[;#]', line):
            continue
        # [code,priority,char]
        code, seq, ch = re.split('[,=]', line)
        prefix = code[:2]
        all_possible_codes.add(prefix)

res = subprocess.run('{ python3 ./gen-2.py; } | sort', shell=True, text=True, capture_output=True)
if True: # keep indent with last version of this file.
    for line in res.stdout.split('\n'):
        line = line.rstrip("\n")
        if not line or re.match('^[;#]', line):
            continue
        # [code,priority,char]
        code, seq, ch = re.split('[,=]', line)
        all_available_codes.add(code)


print(all_possible_codes - all_available_codes)
