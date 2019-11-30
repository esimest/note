# AWK 命令

## 使用场景

1. 把 Awk 当作简化的用于处理或统计文本表格的特定 C 语言来理解。
2. Awk 核心逻辑是文本行记录处理，行列分割处理

备注:

1. 简单上手，够用即可
2. 复杂的逻辑推荐使用 Python 等工具

## awk 流程的 Python 表示

```python3
begin_process()
for line in file:
    if pattern:
        process_line(line, line.split())
end_process()
return
```

## 基本语法及运行说明

1. C 类语法.

```awk
{
    print "Hello, World";
}
```

2. `-f` 指定 awk 脚本文件

3. `#!/usr/bin/awk -f` `#!/usr/bin/env awk` SHELLBANG

## 记录行有关的列表

- `$0` 表示当前匹配的记录行
- `$1` 表示当前记录行的第 1 列数据.
- `$2` 表示当前记录行的第 2 列数据.
- `$3` 表示当前记录行的第 3 列数据.
- `$<N>` 表示当前记录行的第 N 列数据.

## awk 使用模板

```awk
BEGIN {
    # 一般用于变量初始化
}
pattern(模式匹配相当于在每行执行前做个 if 判断，支持正则)
# 正则 ~ /regex/
# 判等 a == b
# 不等 a != b
# 与 && 或 || 非 !a
{
    # 实际处理部分
}
END {
    # 退出前执行的代码块。例如打印结果...
}
```

```awk
{
    print $1, $3; # 输出第一、三列，不会输出逗号和空格
}
```

## 内置全局变量

- `FS` 列分割符，支持正则.
- `NF` 当前行记录的列数
- `NR` 当前行号.
- `FNR` 当前文件的当前行号.
- `FILENAME` 当前文件名
- `RS` 行分割符(默认为换行)
- `OFS` 用于输出的记录分割符(默认是换行)
- `OFMT` 数字的输出格式(默认是 %.6g)
- `CONVFMT` 数字的转换格式(默认是 %.6g)
- `SUBSEP` 分割多下标(默认是 034)
- `ARGC` 参数个数
- `ARGV` 参数数组，可修改
- `ENVIRON` 环境变量

## 内置函数

内置函数中大部分都是处理文本的(因为主要用于处理文本表格)

- `rand` 返回 (0, 1) 之间的随机数.
- `srand` 设置随机数种子，返回之前的种子.
- `int` 返回整型值.
- `length` 返回参数作为字符串的长度，(无参则以 %0 为参数).
- `substr(s, m, n)` n表示长度，m 表示起始位置(注意: 从 1 开始).
- `index(s, t)` 查找 `t` 出现的索引位置，0 表示没有出现.
- `match(s, r)` 查找匹配正则表达式 `r` 的出现开始位置，返回 0 表示未找到, `RSTART` 会被设置为匹配的起始位置，`RLENGTH` 表示匹配的长度.
- `split(s, a, fs)` 将字符串 `s` 分割成数组元素 `a[1], a[2], a[3],...,a[n]` 然后返回 n.
- `sub(r, t, s)` 将 `s` 中第一次匹配`r` 正则表达式的内容替换为 `t`.
- `gsub(r, t,s)` 将 `s` 中所有匹配`r` 正则表达式的内容替换为 `t`.
- `tolower(str)` 转小写.
- `toupper(str)` 转大写.
- `sprintf(fmt, expr, ...)` 类似于 C 语言中 `printf`.
- `system(cmd)` 执行系统命令并返回退出状态.

## awk 实现单词统计(每行一个单词)

```awk
cat file | awk '{for(i=1; i<=NF; i++) array[$1]++}END{for(i in array) print i, array[i]}'
```

