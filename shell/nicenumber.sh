#!/bin/bash
#  nicenumber -- 将给定的数字以逗号分割的形式显示出来
# 可接受两个选项：DD (decimal point delimiter，小数分隔符)
# TD (thousands delimiter，千分位分隔符)
# 美化数字显示，如果指定了第二个参数，则将输出回显在 stdout。


function nicenumber(){
    # 假定 '.' 是输入数字的小数分隔符
    # 默认输出小数分隔符也是'1'

    integer=$(echo $1 | cut -d. -f1)
    decimal=$(echo $1 | cut -d. -f2)

    # 判断输入数字是否有整数部分
    # 如果有整数部分，则将小数部分保存起来
    if ["$decimal" != "$1" ] ; then
        result="${DD:='.'}$decimal"
    fi

    thousands=$integer

    while [ $thousands -gt 99 ] ;do
        remainder=$(($thousands % 1000))

        while [ ${#remainder} -lt 3 ] ; do
            remainder="0$remainder"
        done

        result="${TD:=','}${remainder}${result}"
        thousands=$(($thousands / 1000))
    done

    nicenum="${thousands}${result}"
    if [ ! -z $2 ] ; then
        echo $nicenum
    fi
}

DD="."
TD=","

while getopts "d:t:" opt; do
    case $opt in
        d ) DD="$OPTARG"    ;;
        t ) TD="$OPTARG"    ;;
    esac
done

shift $(($OPTIND - 1))

if [ $# -eq 0 ] ; then
    echo "Usage: $(basename $0) [-d c] [-t c] numeric_value"
    echo "  -d specifies the decimal point delimiter (default '.')"
    echo "  -t specifies the thousands point delimiter (default '.')"
    exit 0
fi

nicenumber $1 1

exit 0