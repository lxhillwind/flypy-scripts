#!/usr/bin/env python3

"""
全码字排序.

根据 ./4-to-3.py 来重写了优先级.
"""

import re
import sys
import subprocess


used_code = {}
all_codes_2 = {}
all_codes_3 = {}
all_valid_2_code = set()
code_begin_with_1 = set()  # 允许从1开始排的全码; 数据来自 ./gen-fullcode.py, 间接来自 ./搜狗拼音win版自定义短语.ini

with open('./fixed-encoding.txt') as f:
    for line in f.readlines():
        line = line.strip()
        if not line or re.match('^[;#]', line):
            continue
        code, seq, ch = re.split('[,=]', line)
        i = (code, seq, ch)
        if len(code) == 4:
            print(f'{i[0]},{i[1]}={i[2]}')
        if code not in used_code:
            used_code[code] = {}
        used_code[code][seq] = ch


class LastPrefix:
    def __init__(self, prefix):
        self.prefix = prefix
        self.chars = []

    def add(self, char):
        self.chars.append(char)

    def finish(self):
        prefix = self.prefix

        def get_index(ch):
            prefix_2 = prefix[:2]
            idx_type = 0
            if ch == all_codes_2.get(prefix_2, {}).get('1'):
                idx_type = 2
                seq = 2
            elif ch == all_codes_2.get(prefix_2, {}).get('2'):
                idx_type = 2
                seq = 1
            else:
                prefix_3 = prefix[:3]
                seq = [
                        seq
                        for seq in all_codes_3[prefix_3]
                        if all_codes_3[prefix_3][seq] == ch
                        ][0]
                seq = int(seq)
                if seq < 3:
                    idx_type = 1
                    seq = seq * -1
            return [idx_type, seq]

        # 先去重再排序
        self.chars = list(set(self.chars))
        self.chars.sort(key=get_index)

        # 如果对应二简码 / 三简码中排在首位或次位, 则直接从全码中移除;
        prefix_2 = prefix[:2]
        for ch in self.chars[:]:
            if ch == all_codes_2[prefix_2].get('1') or ch == all_codes_2[prefix_2].get('2'):
                self.chars.remove(ch)
        prefix_3 = prefix[:3]
        for ch in self.chars[:]:
            if ch == all_codes_3[prefix_3].get('1') or ch == all_codes_3[prefix_3].get('2'):
                self.chars.remove(ch)

        code = prefix
        for seq, ch in used_code.get(code, {}).items():
            if ch in self.chars:
                self.chars.remove(ch)

        seq = 0

        # 为可能的词组 保留 首选位置;
        # 单字优先的话, 就让以后的我可能会完成的 vim 输入法来设置吧:
        # 只需要在 vim 中能实现盲打即可. {{{
        # 如果全码没有对应词组, 则不做优先级调整.
        if code[:2] in all_valid_2_code and code[2:] in all_valid_2_code:
            seq_1_preserve = True
        else:
            seq_1_preserve = False
        # }}}

        for ch in self.chars:
            seq += 1
            while used_code.get(code, {}).get(str(seq)):
                seq += 1
            if seq_1_preserve and seq == 1:
                seq += 1
            print(f'{prefix},{seq}={ch}')


# 获取二简码首选次选的信息
res = subprocess.run('{ python3 ./gen-2.py; } | sort', shell=True, text=True, capture_output=True)
if True: # keep indent with last version of this file.
    for line in res.stdout.split('\n'):
        line = line.rstrip("\n")
        if not line or re.match('^[;#]', line):
            continue
        # [code,priority,char]
        code, seq, ch = re.split('[,=]', line)

        if len(code) == 2 and int(seq) < 3:
            prefix = code
            if code not in all_codes_2:
                all_codes_2[code] = {}
            all_codes_2[code][seq] = ch


# 获取三简码首选次选的信息
res = subprocess.run('{ python3 ./gen-3.py; } | sort', shell=True, text=True, capture_output=True)
if True: # keep indent with last version of this file.
    for line in res.stdout.split('\n'):
        line = line.rstrip("\n")
        if not line or re.match('^[;#]', line):
            continue
        # [code,priority,char]
        code, seq, ch = re.split('[,=]', line)
        if len(code) != 3:
            continue
        if code not in all_codes_3:
            all_codes_3[code] = {}
        all_codes_3[code][seq] = ch


last_prefix = None
res = subprocess.run('{ python3 ./gen-fullcode.py; } | sort', shell=True, text=True, capture_output=True)


if True: # keep indent with last version of this file.
    for line in res.stdout.split('\n'):
        line = line.rstrip("\n")
        if not line or re.match('^[;#]', line):
            continue
        # [code,priority,char]
        code, seq, ch = re.split('[,=]', line)
        if int(seq) == 1:
            code_begin_with_1.add(code)

        all_valid_2_code.add(code[:2])

if True: # keep indent with last version of this file.
    for line in res.stdout.split('\n'):
        line = line.rstrip("\n")
        if not line or re.match('^[;#]', line):
            continue
        # [code,priority,char]
        code, _, ch = re.split('[,=]', line)

        if len(code) != 4:
            continue

        prefix = code[:4]

        if not last_prefix:
            last_prefix = LastPrefix(prefix)
        # 开始新的前缀了, 将上一个前缀的结果记录下来.
        if last_prefix and last_prefix.prefix != prefix:
            last_prefix.finish()
            # 更新 last_prefix
            last_prefix = LastPrefix(prefix)

        last_prefix.add(ch)

last_prefix.finish()
