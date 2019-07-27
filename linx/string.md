# Linux 字符串

## 单引号、双引号

```shell
# 单引号内变量无法替换，双引号内变量可以替换
[root@VM_0_15_centos etc]# var=var
[root@VM_0_15_centos etc]# echo '${var}'
${var}
[root@VM_0_15_centos etc]# echo "${var}"
var
[root@VM_0_15_centos etc]#

```
