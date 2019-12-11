# mdadm(Multiple Devices admin)

[相关链接](https://linux.cn/article-6085-1.html)

## 基本概念

- 校验方式
   > 重建 RAID 时用于生成丢失的数据

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
# 1. 检查要做 raid 的磁盘是否已经做了 raid
ls /dev/ | egrep "sd[^a]" | xargs -n1 -i mdadm --examine /dev/{}
## 如果输出如下结果代表该磁盘不属于任何现有 raid 阵列，则可直接跳过第二步
mdadm: No md superblock detected on /dev/sdb.
## 如果输出如下结果代表磁盘之前做过 raid，需要清除 raid 信息(第二步)
/dev/sdb:
          Magic : a92b4efc
        Version : 1.2
    Feature Map : 0x1
     Array UUID : 11ee5edc:28376b5c:5370a75c:0e66971e
           Name : TENCENT64.site:0  (local to host TENCENT64.site)
  Creation Time : Sun Aug 18 03:22:46 2019
     Raid Level : raid5
   Raid Devices : 3

 Avail Dev Size : 3514957824 (1676.06 GiB 1799.66 GB)
     Array Size : 3514957824 (3352.13 GiB 3599.32 GB)
    Data Offset : 262144 sectors
   Super Offset : 8 sectors
   Unused Space : before=262056 sectors, after=0 sectors
          State : active
    Device UUID : 0759634c:be460a58:db249192:1f3cb773

Internal Bitmap : 8 sectors from superblock
    Update Time : Sun Aug 18 03:43:02 2019
  Bad Block Log : 512 entries available at offset 72 sectors
       Checksum : 78c14202 - correct
         Events : 7669

         Layout : left-symmetric
     Chunk Size : 512K

   Device Role : Active device 0
   Array State : AAA ('A' == active, '.' == missing, 'R' == replacing)

# 2. 清除磁盘 raid 信息
## 查看磁盘对应的 raid 卷信息(如 md0 md1 ...)
lsblk
## 关闭对应 raid 盘并删除对应的逻辑盘，如关闭 md0 为以下命令
mdadm --stop /dev/md0
rm -f /dev/md0
## 清空磁盘的 raid 信息
ls /dev/ | egrep "sd[^a]" | xargs -i -n1 mdadm --zero-superblock /dev/{}
## 如果磁盘有分区，则需删除分区，下列命令为删除分区 1
# ls /dev/ | egrep "sd[^a]$" | xargs -n1 -i parted /dev/{} rm 1


# 3. 创建磁盘分区表
## 查看分区信息
ls /dev/ | egrep "sd[^a]" | xargs -n1 -i parted /dev/{} p
## 输出结果类似于
Model: LSI MR9361-8i (scsi)
Disk /dev/sdb: 1800GB
Sector size (logical/physical): 512B/4096B
Partition Table: msdos
Disk Flags:

Number  Start  End  Size  Type  File system  Flags
## 如果 Partition Table: 对应的为 unKnown 或不是 msdos，则执行以下命令，否则跳过
ls /dev/ | egrep "sd[^a]" | xargs -n1 -i parted /dev/{} mklabel msdos (unKnown)
echo "yes" | parted /dev/sdb mklable msdos (其它)


# 获取磁盘大小
# size_b=$(lsblk /dev/sdb -b| awk 'NR==2{print $4}') && size_m=$(($size_b / 1000000))"."$(($size_b % 1000000))
# size_b=$(lsblk /dev/nvme0n1 -b| awk 'NR==2{print $4}') && size_m=$(($size_b / 1000000))"."$(($size_b % 1000000))

# 创建磁盘分区
# ls /dev/ | egrep "sd[^a]" | xargs -n1 -i parted /dev/{} mkpart primary 1 ${size_m}
# ls /dev/ | egrep "nvme" | xargs -n1 -i parted /dev/{} mkpart primary 1 ${size_m}


# 创建 raid5
cd /dev/ && echo "yes" | mdadm -C /dev/md0 -l raid5 -n 11 -x 1 $(ls /dev/ | egrep "sd[^a]" | xargs)

# 查看磁盘 raid 信息
ls /dev/ | egrep "sd[^a]" | xargs -n1 -i mdadm --examine /dev/{}

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
