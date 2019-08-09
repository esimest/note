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
