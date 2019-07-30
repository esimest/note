# Shell Note

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
