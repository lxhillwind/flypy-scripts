#!/usr/bin/env python3

"""
本程序的目的是找出有二简码但是不在首位候选的字;
(注意已经将一简码合并到二简码首位了, 所以部分字的候选顺序相比官方数据发生了改变,
例如 着 / 遮 / 任 等等.)
(另外, 也将全码通过字频按顺序合并到三简码了; 不过三简码的顺序相比官方数据没有改变)

并对其进行分析, 包括:
- 哪些字 **必须** 用二简码打出来, 否则三简码就没法打了 (以 a: 标注);
- 哪些字在补充到三简码后, 更靠后 (因此鼓励打二简码, 以 b: 标注);
- 哪些字本来有二简码首位, 我们将其修改了然后其三简码没变顺序 (因此鼓励打二简码, 以 c: 标注);
- 官方数据没有二简码首位的, 三简码提前或没变顺序 (因此不鼓励打二简码, 分别以 d: / e: 标注).

实际结果中:
- a: 要求打二简码的没有 (如果有的话, 我们会手动将其添加到 ./gen-fullcode.py 的 additional_data 里并重新生成)
- b: 因为二简码比三简码更靠前而鼓励打二简码的一共有 12 个字
- c: 二简码被往后移, 和三简码候选位置一样而鼓励打二简码的一共有 17 个字
因此最好记住 b.

注意 c 类的是官方的二简码首位字, 其读音与一简码类似, 因此无需强记.

执行方式:
    ./gen-非首位二码候选.py | sort
"""

import re
import subprocess

# key: 字; value: 嵌套字典 (key: 码长 (str); value: 对象 (seq, code))
chars_with_double_code = {}

single_chars = r'''
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
single_chars = [i.split(',') for i in single_chars]
single_chars_code = [i[0] for i in single_chars]

p = subprocess.run('./gen-2.py; ./gen-3.py; ./gen-4.py', shell=True, text=True, capture_output=True)

for line in p.stdout.splitlines():
    if not re.match('^[a-z]', line):
        continue
    code, seq, ch = re.split('[,=]', line)
    if len(ch) != 1:
        continue
    seq = int(seq)
    if len(code) == 2 and seq > 1:
        chars_with_double_code[ch] = {}
        chars_with_double_code[ch]['2'] = {'seq': seq, 'code': code}

for line in p.stdout.splitlines():
    if not re.match('^[a-z]', line):
        continue
    code, seq, ch = re.split('[,=]', line)
    seq = int(seq)
    if ch in chars_with_double_code and len(code) == 3:
        chars_with_double_code[ch]['3'] = {'seq': seq, 'code': code}

for ch, data in chars_with_double_code.items():
    if '3' not in data:
        print('a: 没有三简码, 必须打二简码:', ch, data['2']['code'], data['2']['seq'])
    else:
        if data['2']['seq'] < data['3']['seq']:
            print('b: 三简码候选顺序靠后, 鼓励打二简码:', ch, data['2']['code'], data['2']['seq'])
        elif data['2']['code'] in single_chars_code and data['2']['seq'] == data['3']['seq'] == 2:
            print('c: 二简码官方数据是首位但是三简码候选顺序不变, 鼓励打二简码:', ch, data['2']['code'], data['2']['seq'])
        elif data['2']['seq'] > data['3']['seq']:
            print('d: 三简码候选顺序提前, 鼓励打三简码:', ch, data['3']['code'], data['3']['seq'])
        else:
            print('e: 三简码候选顺序不变:', ch, data['3']['code'], data['3']['seq'])
