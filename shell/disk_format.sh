#!/bin/bash
# disk_format -- 快速格式化裸磁盘，并挂在至指定目录

if [ $# -lt 2 ] ; then
    echo "Usage: $0 device direction [format_methon]" >&2
    exit
fi

device=$1 dir=$2 method=mkfs.xfs

if [ ! -z $3 ] ; then
    method=$3
fi

# 格式化磁盘
$method $device

# 挂载
mount $device $dir

# 挂载信息记录到/etc/fstab
echo "$device $dir $(df $dir -T|awk 'NR==2 {print $2}') defaults 0 0" >> /etc/fstab