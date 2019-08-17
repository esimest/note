# mdadm(Multiple Devices admin)

[相关链接](https://linux.cn/article-6085-1.html)

## 基本概念

- 校验方式
   > 用于重建 RAID 时生成丢失的数据

- 条带化
   > 将切片数据随机存储到多个磁盘

- 镜像
   > 镜像会自动备份数据

- 热备份
   > 备用驱动，用于发生故障时替换故障的驱动

- 块
   > RAID 读写数据的最小单元

## RAID

- RAID5
   > 使用奇偶校验来恢复损坏的数据(如果损坏的磁盘超过一块将会导致数据丢失)
   > 不论使用多少块盘做 RAID5，都会有且只有一块盘的容量用于存储校验数据

## 使用 mdadm 做软 raid

```shell
# 查看分区信息
ls /dev/ | egrep "sd[^a]" | xargs -n1 -i parted /dev/{} p
# ls /dev/ | egrep "nvme" | xargs -n1 -i parted /dev/{} p

# 创建磁盘分区表
ls /dev/ | egrep "sd[^a]" | xargs -n1 -i parted /dev/{} mklabel msdos
# ls /dev/ | egrep "nvme" | xargs -n1 -i parted /dev/{} mklabel msdos

# 获取磁盘大小
size_b=$(lsblk /dev/sdb -b| awk 'NR==2{print $4}') && size_m=$(($size_b / 1000000))"."$(($size_b % 1000000))
# size_b=$(lsblk /dev/nvme0n1 -b| awk 'NR==2{print $4}') && size_m=$(($size_b / 1000000))"."$(($size_b % 1000000))

# 创建磁盘分区
ls /dev/ | egrep "sd[^a]" | xargs -n1 -i parted /dev/{} mkpart primary 1 ${size_m}
# ls /dev/ | egrep "nvme" | xargs -n1 -i parted /dev/{} mkpart primary 1 ${size_m}

# 删除磁盘分区
# ls /dev/ | egrep "sd[^a]$" | xargs -n1 -i parted /dev/{} rm 1

# 创建 raid file system
#vim fd.sh
##!/bin/sh
#
#fdisk "$1" <<EOF
#t
#fd
#w
#EOF

# ls /dev/ | egrep "sd[^a]" | xargs -n1 -i bash +x ./fd.sh {}

# 创建 raid5
cd /dev/ && mdadm -C /dev/md0 -l raid5 -n 11 -x 1 $(ls /dev/ | egrep "sd[^a]1" | xargs)
# mdadm -C /dev/md0 -l raid5 -n 4 /dev/nvme0n1p1 /dev/nvme1n1p1 /dev/nvme2n1p1 /dev/nvme3n1p1
# mdadm -C /dev/md0 -l raid5 -n 3 /dev/sdb1 /dev/sdc1 /dev/sdd1
# cd /dev/ && mdadm -C /dev/md0 -l raid5 -n 3 $(ls /dev/ | egrep "sd[^a]1" | xargs)

# 关闭 raid
mdadm  --stop /dev/md*

# 清除 raid 信息
ls /dev/ | egrep "sd[^a]" | xargs -i -n1 mdadm --zero-superblock /dev/{}

# 查看分区 raid 信息
ls /dev/ | egrep "sd[^a]1" | xargs -n1 -i mdadm --examine /dev/{}
# ls /dev/ | egrep "nvme.n1p1" | xargs -n1 -i mdadm --examine /dev/{}

# 格式化 raid 盘
mkfs.ext4 /dev/md0

# 创建挂载点，添加挂载信息
mkdir /data12 && echo "/dev/md0      /data12/  ext4    defaults        0       0" >> /etc/fstab
mount -a

# 将 raid 信息写入 /etc/mdadm.conf
mdadm -E -s -v > /etc/mdadm.conf

# 重启机器
reboot
```

1. 检查磁盘/分区是否已经做了 raid
   `mdadm --examine /dev/sd[a-d]`

2. 磁盘分区
   `fdisk ${disk} --> n --> 1 --> p --> t --> fd --> w`

3. 创建 RAID

   ```shell
   # 以下两种方式都可以用于创建 RAID
   mdadm -C ${raid_dev} -l ${level} -n ${num} -x ${num1} ${devices}
   mdadm --create  ${raid_dev} --level=${level} --raid-devices= ${num} --spare-devices=${num1} ${devices}
   ```

4. 查看 RAID
   `cat /proc/mdstat`

5. 查看分区设备信息
   `mdadm -E ${devices}`

6. 查看阵列信息
   `mdadm --detail ${raid_dev}`

> 后续可将创建的 raid 设备当作正常的磁盘分区使用(如创建分区，挂载...)

n. 挂载后，将配置信息写入  /etc/mdadm.conf
   > 如果不写入 /etc/mdadm.conf，重启操作系统后会出问题

`mdadm -E -s -v >> /etc/mdadm.conf && mdadm --detail --scan --verbose >> /etc/mdadm.conf`

## command

```shell
# 检查磁盘/分区是否已经做了 raid
mdadm --examine /dev/sda[3-4]

```
