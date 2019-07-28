#!/bin/bash

## scriptbc -- 封装了 bc 命令，返回对参数的计算结果

# 命令行进行数字运算有两种方法
## $(( 算术表达式 ))，$(( 1/2 )) == 0
## bc 命令（交互式命令）

if [ "$1" = "-p" ]; then
  # -p 后接小数位的精度，通过这个选项来实现任意精度的计算
  # 注意：* 和 / 后不能留空格
  precision=$2
  shift 2
else
  precision=2
fi

# $*: 所有参数组成的一个字符串
# $@: 所有参数组成的一个字符串列表，列表中的的元素与参数一一对应

bc -q -l << EOF
scale=$precision
$*
quit
EOF

exit 0
