# 不提交到仓库的文件 (由于版权因素不能放在此仓库, 或者是根据编码数据生成的文件)

<hr />

- 单字字频统计.txt

文件头:

```
# 下载之后, 需要仅保留汉字;
# Sh -r curl -s https://raw.githubusercontent.com/argb/hanzi-data/master/%E7%8E%B0%E4%BB%A3%E6%B1%89%E8%AF%AD%E6%B1%89%E5%AD%97%E9%A2%91%E7%8E%87%E8%A1%A8.csv
```
来源于 <https://github.com/gaboolic/rime-frost> 仓库; 用作包含多音字的字频统计.

<hr />

- cn_dicts/8105.dict.yaml

来源于 <https://github.com/gaboolic/rime-frost> 仓库; 用作包含多音字的字频统计.

<hr />

- libre-flypy.txt

来源于 <https://github.com/OverflowCat/libre-flypy> 仓库; 用作鹤形编码的补充.

<hr />

- 鹤形辅助码.txt

文件头:

```
# 用于手心输入法的辅助码; 主要用于去重词组.
#
# 数据来自自定义的鹤形方案的全码, 然后去掉音节, 形码保留首位 (形码全码不知道为什么不工作).
#
# 更新方式 (vim 指令):
# :exec 'normal jdG' | r !./gen-辅助码.py 2>/dev/null
```

<hr />

- 鹤形辅助码-unicode.txt

*windows unicode 编码*

文件头:

```
# :r ./鹤形辅助码.txt
```

<hr />

- 搜狗拼音win版自定义短语.ini

*windows unicode 编码, 需要保存为 ff=unix / fenc=utf-8*

文件来源参考小鹤音形官方网站的下载说明.

<hr />

- all-utf8.ini

文件头:

```
# how to update:
# :exec 'normal 2jdG' | r ./macos-base.ini | r ./macos-special-split-char.ini
# :+1,$v/^[a-z]/d
```

<hr />

- flypy_plus.txt
- flypy_extra.txt

文件来源: <https://github.com/OscarXWei/hesingle>

<hr />

- macos-base.ini

*windows unicode 编码*

文件头:

```
# 注意:
# *不要* 在此文件中导入 macos-split-char.ini;
# 因为 Mac OS 上搜狗输入法是按照 code 字母排序导入的, 而且已经导入的就不会再导入了;
# 这导致, 例如, yj (yan) 开头的三码字基本上无法补全.
# (o 之后的三码字就会有问题)
#
# 要在 MacOS 上搜狗输入法中导入 macos-split-char.ini 中的短语的话, 需要先导入此文件, 然后再导入它.
# 即, 需要分2次导入.
#
# 如果词库更新了, 可以执行这个 vim 指令来删除内容并导入更新的文件:
# :exec 'normal jdGo# 如下内容是通过 vim 指令导入' | :$r !{ ./gen-2.py; ./gen-3.py; ./gen-4.py; } | grep -E '^[a-z]' | sort | uniq
```

<hr />

- macos-special-delimiter.ini

*windows unicode 编码*

文件头:

```
# how to update:
# :exec 'normal jdGo' | :$r !python3 ./gen-delimiter.py | sort
```

<hr />

- macos-special-split-char.ini

*windows unicode 编码*

文件头:

```
# how to update:
# :exec 'normal jdGo' | :$r !python3 ./split-char.py 2>/dev/null | sort
```
