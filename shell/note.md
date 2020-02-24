# Shell Note

## 特殊符号

### `[]`

`[]` 是 `test` 命令的另一种形式(可直接当作命令使用). `[` 与参数之间需要有空格 `]`.
该命令的返回值只有 `0`(true) 和 `1`(false).
查看帮助: `man test`/`man [`

```shell
# 字符串是否为空
[ -z ${var} ] # return len(${var}) == 0
[ -n ${var} ] # return lent(${var}) != 0

# 字符串判等 ==/= !=
[ ${a} == ${b} ] # retrun str(${a}) == str(${b})

# 数字(整数)判等 -eq -lt -gt
[ ${a} -eq ${b} ] # return int(${a}) == int(${b})

# and(-a) or(-o) not(!)
[ ! $(expr)] # return not $(expr)
[ $(expr1) -a $(expr2) ] # return $(expr1) and $(expr2)
```

## Compound Commands(复合命令)

查看帮助: `man bash`

### `(list)`

在 subshell 中执行命令集合, 通过 `$` 获取命令的结果.

### `{list;}`

在当前 shell 中执行命令集合

### `[[]]`

条件表达式.
`[[]]` 可以使用 `[]` 中大部分选项.

```shell
# and or not
[[ expr1 && expr2 ]] # return expr1 and expr2
[[ ! 3 < 2 ]]  # true

# 正则匹配
[[ str =~ regex ]] # return re.match(regex, str)
```

### `(())`

1. 算术表达式, 通过 `$` 符号获取表达式的值;
2. 用于 for 循环, 语法与 `C` 语言类似;

```shell
for (( i = 0; i < 3; i++ )); do
  echo "$i"
done

```

## Linux 字符串

### 单引号、双引号

```shell
## 单引号内变量无法替换，双引号内变量可以替换
[root@VM_0_15_centos etc]# var=var
[root@VM_0_15_centos etc]# echo '${var}'
${var}
[root@VM_0_15_centos etc]# echo "${var}"
var
[root@VM_0_15_centos etc]#

```

### 字符串取值

```shell
## 返回变量 var 的值
${var} or $var

## return var if var is defined else return DEFAULT
${var-DEFAULT}

## return var if var else return DEFAULT
${var:-DEFAULT}

## return var if var is defined else return DEFAULT
${var=DEFAULT}

## return var if var else return DEFAULT
${var:=DEFAULT}

## return OTHER if var is defined else return null
${var+OTHER}

## return OTHER if var else return null
${var:+OTHER}

## return ERR_MSG if var is not defined
${var?ERR_MSG}

## return ERR_MSG if not var
${var:?ERR_MSG}
```

### 字符串操作

```shell
## return len(string)
${#string}

## return string[position:]
${string:position}

## reutrn string[position:position+length]
${string:position:length}

## return string.replace('substing', '', 1) if string.startswith('substing')
## return string.partition('substing')[2] if string.startswith('substing')
${string#substring}

## retur string.lstrip('substing'), 去掉最长匹配
${string##substring}

## return string.rpartition('substing')[0] if string.endswith('substing')
${string%substring}

## return string.rstrip('substing')
${string%%substring}

## return string.replace('substing', 'replacement', 1)
${string/substring/replacement}

## return string.replace('substing', 'replacement')
${string//substring/replacement}

## return string.replace('substing', 'replacement', 1) if string.startswith('substing')
${string/#substring/replacement}

## return string.rpartition('substing')[0] + 'replacement' if string.endswith('substing')
${string/%substing/replacement}

```
