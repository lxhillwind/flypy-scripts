#!/usr/bin/env python3

"""
生成辅助码; 并去重.
"""

import re
import sys
import subprocess


res = subprocess.run('{ python3 ./gen-fullcode.py; } | sort', shell=True, text=True, capture_output=True)


all_ch = {}

# 根据运行此程序, 逐步完善此变量.
all_ch_whitelist = {
        # vim 命令来载入正确编码 (将错误的手动去掉):
        # 尽量按照官方数据, 但是也考虑顺手程度.
        # :r !{ ./% >/dev/null } 2>&1 | sed -E 's/^duplicate code://'
 '巴': 's',
 '觱': 'x',
 '蹙': 'w',
 '鸟': 'w',
 '东': 'a',
 '酆': 'f', # 官方拆为 山　丰　丰　一　口　丷　一　阝 (不使用; 采用读音.)
 '尬': 'y',
 '艮': 'e', # 官方拆为 彐　乛　丿　ㄟ;
 '甘': 'n',
 '尴': 'y',
 '感': 'x',
 '广': 'd',
 '贯': 'g', # 官方拆为 毌　冂　人 (毌guàn); (正好读音一致)
 '禾': 'p', # 官方拆为 丿　木; (见官方小字拆分规则 https://xgr313l2jy.k.topthink.com/@xhrm/gz.html)
 '亍': 'e',
 '鹩': 'd',
 '尥': 'y',
 '耒': 'f',
 '冒': 'o', # 官方拆为 冂　一　一　目; 不使用; 其他日字头的类似.
 '冕': 'o',
 '木': 'u',
 '南': 'u',
 '廿': 'c',
 '邳': 'p',
 '戚': 'w',
 '壬': 'p', # 官方拆为 丿　士; (其部首为 士)
 '鸶': 's',
 '爽': 'd',
 '戍': 'w',
 '奘': 'p',
 '竹': 'p',
 '朱': 'p',
 '歪': 'b',
 '尪': 'y',
 '戊': 'g', # 官方拆为 戈　丿; (戈 确实是其部首)
 '威': 'x',
 '卫': 'v', # 官方拆为 卩　一; 不使用; 这个和耳偏旁的形状差得太远了.
 '咸': 'x',
 '卸': 'w',
 '戌': 'w',
 '勖': 'o',
 '冔': 'o',
 '燕': 'n',
 '酉': 'x',
 '尤': 'y',
 '臧': 'w',
        }


if True: # keep indent with last version of this file.
    for line in res.stdout.split('\n'):
        line = line.rstrip("\n")
        if not line or re.match('^[;#]', line):
            continue
        # [code,priority,char]
        code, seq, ch = re.split('[,=]', line)
        if len(code) < 3:
            continue
        if ch not in all_ch:
            all_ch[ch] = set()
        # 只关注第3位, 即首位形码.
        graph = code[2]
        if ch in all_ch_whitelist and graph not in all_ch_whitelist.get(ch, []):
            continue
        all_ch[ch].add(graph)


for ch, graphes in all_ch.items():
    if len(graphes) >= 2:
        print(f"""duplicate code: '{ch}': '{"".join(graphes)}',""", file=sys.stderr)
    else:
        print(f'{ch}={graphes.pop()}')
