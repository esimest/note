#!/bin/bash

# filelock -- A flexible file-locking mechanism(机制)

retries="10"             # Default number of retries
action="lock"            # Default action
nullcmd="'which true'"   # Null command for lockfile

# /usr/bin/true : 返回值恒为 0
# /usr/bin/false : 返回值恒为 1

# getopts: 获取命令行选项,参数后加':'表示必须传入选项的值
# $OPTARG 选项对应的值
# $OPTIND 下一个待处理的参数的索引

while getopts "lur:" opt; do
  case $ipt in
    l ) action="lock"      ;;
    u ) action="unlock"    ;;
    r ) retries="$OPTARG"  ;;
  esac
done

shift $(($OPTIND - 1))  # 丢弃参数列表中的 $OPTIND - 1 个参数，原来的 $OPTIND 变为现在的 $1

if [ $# -eq 0 ]; then
  cat << EOF >&2
Usage: $0 [-l|-u] [-r retries] LOCKFILE
Where -l requests a lock(the default), -u requests an unlock, -r X
specifies a max number of retries before it fails(default=$retries).
EOF
  exit 1
fi

# Ascertain(弄清，确认) if we have the lockfile command.

if [ -z "$(which lockfile 2 >&1| grep -v 'no lockfile')" ]; then
  echo "$0 failed: 'lockfile' utility not found in PATH." >&2
  exit 1
fi

if [ "$action" = "lock" ]; then
  if ! lockfile -1 -r $retries "$1" 2> /dev/null; then
    echo "$0: Failed: Coldn't create lockfile in time." >&2
    exit 1
  fi
else
  if [ ! -f "$1" ]; then
    echo "$0: Warning: lockfile $1 doesn't exist to unlock." >&2
    exit 1
  fi
  rm -f "$1"
fi

exit 0
