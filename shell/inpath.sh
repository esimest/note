#!/bin/bash
# inpath -- 验证指定程序是否有效，或者能否在PATH目录列表中找到。


function in_path(){
    # 尝试在环境变量PATH中找到给定的命令。如果找到，返回 0；
    # 如果没有找到，则返回1. 注意，该函数会临时修改IFS（内部字段分隔符）
    # 不过在函数执行完毕时会将其恢复原状。
    cmd=$1 ourpath=$2 result=1
    oldIFS=$IFS IFS=":"

    for directory in $ourpath
    do
      if [ -x $directory/$cmd ] ; then
      result=0
      fi
    done

    IFS=$oldIFS
    return $result
}


function checkForCmdInPath(){
    var=$1
    if [ "$var" != "" ] ; then
        if [ "${var:0:1}" = "/" ] ; then
            if [ ! -x "${var}" ] ; then
                return 1
            fi
        elif ! in_path $var "$PATH" ; then
            return 2
        fi
    fi

}

if [ $# -ne 1 ] ; then
    echo "Usage: $0 command" >&2
    exit
fi

checkForCmdInPath "$1"
case $? in
    0) echo "$1 found in PATH" ;;
    1) echo "$1 not found or executable" ;;
    2) echo "$1 not found in PATH" ;;
esac

exit 0

# ${var:n:m} 获取var参数的n-m个字符 或
# ${var%${var#?}} %: 去除结尾   #: 去除开头   或
# $(echo $var | cut -c1)
