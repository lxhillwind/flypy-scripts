#!/usr/bin/env python3

"""
将 3码或全码字合并到3码字 (的候选区里);
根据 ./cn_dicts/8105.dict.yaml 来重写了优先级.
(也包含了只有一简字或二简字的字, 通过 ./flypy_plus.txt 获取了其全码数据.)
"""

import re
import sys
import subprocess


all_chars_with_pinyin = {}
with open('./cn_dicts/8105.dict.yaml') as f:
    for line in f.readlines():
        line = line.rstrip("\n")
        if line.startswith('#') or len(line) < 1:
            continue
        arr = re.match('^([^\t]+)\t([a-z]+)\t([0-9]+)$', line)
        if not arr:
            continue
        [ch, pinyin, freq] = arr.groups()
        freq = int(freq)
        if ch not in all_chars_with_pinyin:
            all_chars_with_pinyin[ch] = {}
        all_chars_with_pinyin[ch][pinyin] = freq


used_code = {}

with open('./fixed-encoding.txt') as f:
    for line in f.readlines():
        line = line.strip()
        if not line or re.match('^[;#]', line):
            continue
        code, seq, ch = re.split('[,=]', line)
        if len(ch) != 1:
            continue
        i = (code, seq, ch)
        #print(f'{i[0]},{i[1]}={i[2]}')
        if code not in used_code:
            used_code[code] = {}
        used_code[code][seq] = ch


# 二简码能直接打出来的字;
all_codes_2 = {}

prefix_added = {}


class LastPrefix:
    def __init__(self, prefix):
        self.prefix = prefix
        self.chars = []

    def add(self, char):
        self.chars.append(char)

    def finish(self):
        prefix = self.prefix

        def get_index(ch):
            # 返回列表: 列表第一个元素表示是否存在, 第二个元素表示权重.
            # 2个值越小, 表示权重越高.
            pinyin = prefix[:2]
            if ch in all_chars_with_pinyin and pinyin in all_chars_with_pinyin[ch]:
                return [0, -1 * all_chars_with_pinyin[ch][pinyin]]
            else:
                # 这里使用 ch, 是为了让排序是稳定的 (即每次执行程序的结果是一样的).
                return [1, ch]
        # 先去重再排序
        self.chars = list(set(self.chars))
        self.chars.sort(key=get_index)

        ch_1, ch_2 = None, None
        # 将二简码中排在首选和次选的字, 从三简码中往后挪.
        for i in self.chars:
            if i == all_codes_2.get(prefix[:2], {}).get('1'):
                ch_1 = i
                break
        for i in self.chars:
            if i == all_codes_2.get(prefix[:2], {}).get('2'):
                ch_2 = i
                break
        if ch_1:
            self.chars.remove(ch_1)
        if ch_2:
            self.chars.remove(ch_2)
        if ch_1 or ch_2:
            # 将二简码插入到第3个
            insert_position = min(len(self.chars), 2)
            # 先插入首选字; 这样, 如果三简码只有 ch_1 和 ch_2, 可以让 ch_2 排到前面来.
            if ch_1:
                self.chars.insert(insert_position, ch_1)
            if ch_2:
                self.chars.insert(insert_position, ch_2)

        code = prefix
        for seq, ch in used_code.get(code, {}).items():
            if ch in self.chars:
                self.chars.remove(ch)


        seq = 0
        for ch in self.chars:
            seq += 1
            while ch_fixed := used_code.get(code, {}).get(str(seq)):
                print(f'{prefix},{seq}={ch_fixed}')
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


# main
last_prefix = None
res = subprocess.run('{ python3 ./gen-fullcode.py; } | sort', shell=True, text=True, capture_output=True)
if True: # keep indent with last version of this file.
    for line in res.stdout.split('\n'):
        line = line.rstrip("\n")
        if not line or re.match('^[;#]', line):
            continue
        # [code,priority,char]
        code, seq, ch = re.split('[,=]', line)

        prefix = code[:3]
        if prefix not in prefix_added:
            prefix_added[prefix] = []

        if ch in prefix_added[prefix]:
            continue

        if not last_prefix:
            last_prefix = LastPrefix(prefix)
        # 开始新的前缀了, 将上一个前缀的结果记录下来.
        if last_prefix and last_prefix.prefix != prefix:
            last_prefix.finish()
            # 更新 last_prefix
            last_prefix = LastPrefix(prefix)

        if len(code) == 3:
            prefix_added[prefix].append(ch)
        last_prefix.add(ch)

last_prefix.finish()
