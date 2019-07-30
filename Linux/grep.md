# Grep

> Global search Regular Expression and Print out the line,全局搜索正则表达式并把行打印出来
> grep 从给定的文件中或标准输入中搜索表达式

***建议使用 grep 时，搜索的字符串都使用双引号括起来，正则表达式在双引号内才能生效***

```shell
# 默认的 grep 命令会将匹配的字符串以特殊的颜色标识出来
[root@VM_0_15_centos etc]# which grep
alias grep='grep --color=auto'
    /usr/bin/grep
```

## 输出控制选项

```shell

# 输出结果时打印行号
grep -n 'express' files

# 统计表达式出现的次数，不打印出匹配的行
grep -c 'express' files

# 打印匹配行及前n行
grep -B n 'express' files

# 打印匹配行及后n行
grep -A n 'express' files

# 打印匹配行及前后n行
grep -C n 'express' files

```

## 匹配控制选项

```shell
# 搜索时忽略大小写
grep -i 'express' files

# 同时搜索多个表达式
grep -e 'exp1' -e 'exp2' files
grep -E 'exp1|exp2' files
egrep 'exp1|exp2' files

# 搜索文件中的所有表达式（一行为一个表达式）
grep -f patterns_fiel files

# 搜索不包含表达式的行
grep -v 'express' files

# 精准匹配单词
grep -w 'world' files

# 精准匹配行（包括行首行尾的 空格数量等）
grep -x 'line' files

# 递归搜索目录下所有子目录
grep -r 'express' path

```
