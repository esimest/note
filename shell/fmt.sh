#!/bin/bash

# fmt-- Text formatting utility that acts as a wrapper for nroff
#    Adds two useful flags: -w n for line width
#    and -h to enable hyphenation(断字符) for better fills

while getopts "hw:" opt ; do
  case $opt in
    h ) hyph=1            ;;
    w ) width="$OPTARG"   ;;
  esac
done

shift $(( $OPTIND - 1 ))

# ${var:-default} 如果 var 为空或未定义 返回 default
# $@ 所有参数的字符串形式组成的列表

nroff << EOF
.ll ${width:-72}
.na
.hy ${hyph:-0}
.pl 1
$(cat "$@")
EOF

exit 0
