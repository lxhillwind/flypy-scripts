#!/usr/bin/env python3

"""
根据 搜狗拼音win版自定义短语.ini 生成一简码和二简码;

将一简码合并到二简码, 并将原有二简码向后挪.

一简码来源:
https://xgr313l2jy.k.topthink.com/@xhrm/jm.html
"""

import re
import sys
import subprocess


complement_chars = r'''
qu,去
wo,我
er,二
rf,人
ta,他
yi,一
ui,是
iu,出
oo,哦
pk,平
aa,啊
sj,三
de,的
fw,非
ge,个
he,和
jq,就
ke,可
le,了
zd,在
xn,小
cd,才
ve,这
bu,不
ni,你
mw,没
'''.strip().split('\n')
complement_chars = [i.split(',') for i in complement_chars if ',' in i]
complement_chars = {i[0]: i[1] for i in complement_chars}

# 先排序, 让同样前缀的字按顺序排在一起.
res = subprocess.run('sort 搜狗拼音win版自定义短语.ini', shell=True, text=True, capture_output=True)

if True: # keep indent
    for line in res.stdout.split('\n'):
        line = line.strip()
        if not line or re.match('^[;#]', line):
            continue

        if len(line) > len('xxxx,nn=c'):
            # otherwise re.split may raise.
            continue
        code, seq, ch = re.split('[,=]', line)

        if len(ch) > 1:
            continue
        if re.match('^o[^mou]', code):
            continue
        if len(code) >= 3:
            continue

        if code in complement_chars:
            seq = str(int(seq) + 1)

        i = (code, seq, ch)
        print(f'{i[0]},{i[1]}={i[2]}')

for k, v in complement_chars.items():
    i = (k, 1, v)
    print(f'{i[0]},{i[1]}={i[2]}')


# 补充的二简码;
# 例如: liw 对应的几个字都很常用, 但其中几个字不方便打全码;
# 因此将其中最常见的字挪到二简码来.
print('li,2=立')
# 另外, 有些组合没有二简码, 也补充到这里. (generated by ./gen-no-2.py)
print('bl,1=𰻝')  # biáng biáng miàn 或油泼扯面
print('df,1=扽')  # ?
print('dx,1=嗲')
print('ix,1=欻')  # ?
print('js,1=囧')
print('jt,1=觉')
print('lj,1=蓝')
print('lt,1=略')
print('lx,1=俩')
print('mq,1=谬')
print('nd,1=乃')
print('nl,1=娘')
print('nz,1=槈')  # ?
print('rv,1=瑞')
print('rx,1=挼')  # ?
print('ry,1=润')
print('sh,1=桑')
print('sy,1=笋')
print('tw,1=忒')
print('ty,1=吞')
print('ud,1=晒')
print('ux,1=耍')
print('vd,1=宅')
print('vw,1=这')  # ?
print('vy,1=准')
print('xy,1=迅')
print('zj,1=暂')
print('zr,1=赚')
print('zy,1=尊')

# 缺失二简码导致 gen-4.py 报错, 需要补上:
print('eg,1=鞥')
print('fn,1=覅')
print('fv,1=猤')
print('ki,1=怾')
print('my,1=椧')
print('ny,1=黁')
print('ra,1=囕')
print('sw,1=聓')
