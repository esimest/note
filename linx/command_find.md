# find 笔记

> find 用于查找符合条件的文件或目录

- 用法

  ```shell
  find [-H] [-L] [-P] [-D debugopts] [-Olevel] [starting-point...] [expression]
  starting-point 没指定时为当前目录
  expression
  ```

- 大写参数(写在要查找的路径前面)
   > man说明中的command-line 参数实指 starting-point
   > 如果同时指定了PLH三个参数，出现在命令行最后一个的生效
   1. -P 不查找链接文件所指向的文件或目录(默认参数)
   2. -L 查找链接文件所指向的目录，并以该链接文件为base目录
   3. -H 不查找链接文件，除非后面的starting-point是链接文件
   4. -D 打印诊断信息，后接具体的诊断方式
   5. -O 选择优化级别，后接具体的级别[1~3]

## 基本用法

```shell
# 列出目录及子目录下所有文件，包括隐藏文件
find [path]

# 通过名字查找，支持正则表达式
find path -name name

# 通过名字查找，或略大小写
find path -iname name

# 限制子目录的深度
find path -name name -maxdepth 1 # 只查找 path 目录

# 反向查找
find path -not express # 查找与表达式不符的选项
fidn path ! express

# 通过类型查找（支持的类型有 b d c p l f）
find path -name name -type f

# 通过比较另外一个文件的后顺序
## 查找比 file1 修改得更晚的文件
find path -newer file1

## 查找比 file1 修改得更早的文件
find path ! -newer file1

# 默认有多个条件时，使用 AND 逻辑关系
# 使用 OR 逻辑关系
find path -newer file1 -o ! -newer file2 # 比 file1 晚 比 file2 早
```

## 基于时间和日期查找

```shell
# 按最后修改时间查找，n 表示 之前的第 n 天，-n 表示 n 天内，+n 表示 n 天前
find path  -mtime 3
find paht -mtime +3 -mtime -5

# 按最后状态改变的时间
find path -ctime 3

# 按最后访问的时间
find path -atime 3

# 按修改时间，单位为分钟
find path -mmin 3

# 按状态改变时间，单位为分钟
find path -cmin 3

# 按访问时间，单位为分钟
find path -amin 3

# 修改时间比 file1 晚
find path -newer file1

# 状态改变时间比 file1 晚
find path -cnewer file1

# 访问时间比 file1 晚
find path -anewer file1

```

## 基于文件大小查找

```shell
# 查找空文件
find path -type f -empty

# 查找大小为 50M 的文件
find path -type f -size 50M

# 查找大小为 50M ~ 100M 的文件
find path -type f -size +50M -size -100M

```

## 基于文件权限与属性查找

```shell
# 查找权限为 755 的 文件
find path -type f -perm 755

# 查找只读文件
find path -type f -perm /u=r # 用户的权限为 r 则该文件的权限肯定是只读

# 查找可执行文件
find path -type f -perm /a=x

# 查找属主为 esime 的文件
find path -type f -user esime

# 查找属组为 esime 的文件
find path -type f -group esime
```
