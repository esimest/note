# Linux磁盘与分区

- **一扇区容量为 512 bytes = 8 \* 512 bits**
- **第一个扇区保存着主引导记录(446 bytes)和分区表信息(64 bytes)**
- **一个主分区信息需要占用 16 bytes，所以最多只能创建4个分区**
- **通常将第四个分区设置为扩展分区，并不实际写入分区信息，只是指向其它逻辑分区，进而创建更多逻辑分区，达到创建多个分区的效果**

---

- linux硬件设备均以文件形式存放在/dev目录下
- 目前通用存储设备为 /dev/sd[a-p]
- 以/dev/sda为例/dev/sda1, /dev/sda2 ... 为该磁盘划分的不同分区

---

## /etc/fstab(自动挂载文件)

>磁盘或分区被手动挂载后，必须把挂载信息写入/etc/fstab中，使系统开机重启后能够自动挂载。

- 第一列为分区的标签或uuid可唯一标识一个分区
- 第二列为该分区的挂载点
- 第三列为分区文件系统

## 挂载注意事项
**<font color=red>挂载就是将目录与分区互相关联，使得操作系统可以使用该分区</font>**

1. 根目录必须被挂载，且必须时系统中第一个挂载点
2. 挂载点必须是已存在的目录
3. 一个挂载点同一时间只能被挂载一次
4. 一个分区或磁盘同一时间只能挂一次
5. 若要卸载，则必须先脱出挂载点及其子目录

## 文件系统

***文件系统主要用于控制数据在不使用时如何存储、访问、以及元数据的保存***
> 用户通过VFS提供的接口和系统交互
> ext4 xfs等实现了VFS的接口
---

## Inode 与 Data Block

**一个文件包括了，文件的权限、属性信息与文件存储的数据(目录类似)**

- 文件的权限与属性保存在Inode中
- 文件的实际数据保存在 Data Block 中
- 每个文件系统都有一个 superblock 保存着该文件系统的inode 与 data block 的信息(使用量、总量等)
**<font color=red>系统通过文件名找到对应的inode号码,然后找到对应的inode,读取权限等信息,最后根据inode找到 data block</font>**
**<font color=red>碎片整理的目的就是将过于离散的block整合在一起，提高读取速率</font>**

---
## 硬连接与软连接

- 硬连接指向的是源数据的inode(可以实现保护源数据)
- 软连接的data block保存着源数据的inode

---

## ext4与xfs对比

---

## 磁盘与分区工具

***<font color=red>注：磁盘管理步骤：1.建立分区(fdisk) 2.格式化分区(mkfs) 3.挂载(mount)</font>***

## fdisk(新建分区)

- fdisk -l <disk/partition> 查看磁盘/分区信息

```shell
[root@localhost dev]# fdisk -l /dev/sda

Disk /dev/sda: 21.5 GB, 21474836480 bytes, 41943040 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk label type: dos
Disk identifier: 0x000bb996

   Device Boot      Start         End      Blocks   Id  System
/dev/sda1   *        2048     2099199     1048576   83  Linux
/dev/sda2         2099200    41943039    19921920   8e  Linux LVM
```

- fdisk <disk/partition> 进入fdisk命令行,输入m查看使用方式

```shell
[root@localhost dev]# fdisk /dev/sda
Welcome to fdisk (util-linux 2.23.2).

Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

Command (m for help): m
Command action
   a   toggle a bootable flag
   b   edit bsd disklabel
   c   toggle the dos compatibility flag
   d   delete a partition
   g   create a new empty GPT partition table
   G   create an IRIX (SGI) partition table
   l   list known partition types
   m   print this menu
   n   add a new partition
   o   create a new empty DOS partition table
   p   print the partition table
   q   quit without saving changes
   s   create a new empty Sun disklabel
   t   change a partition's system id
   u   change display/entry units
   v   verify the partition table
   w   write table to disk and exit
   x   extra functionality (experts only)
```

- 新建分区  p: 主分区 e: 扩展分区 l: 逻辑分区

```shell
[root@localhost dev]# fdisk /dev/sdb
Welcome to fdisk (util-linux 2.23.2).

Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

Command (m for help): n
Partition type:
   p   primary (2 primary, 0 extended, 2 free)
   e   extended
Select (default p): p
Partition number (1,3, default 1): 3
First sector (1024064-10485759, default 1026048):
Using default value 1026048
Last sector, +sectors or +size{K,M,G} (1026048-2390015, default 2390015):
Using default value 2390015
Partition 3 of type Linux and of size 666 MiB is set
```

- 建好分区后需要在命令行键入w保存

```shell
Command (m for help): w
The partition table has been altered!

Calling ioctl() to re-read partition table.
Syncing disks.
```

---

## mkfs(格式化分区)

- 将 /dev/sdb4分区格式化为xfs格式， -f 强制格式化, -c 检查是否有坏轨

```shell
mkfs.xfs: Use the -f option to force overwrite.
[root@localhost dev]# mkfs.xfs /dev/sdb4
meta-data=/dev/sdb4              isize=512    agcount=4, agsize=252992 blks
         =                       sectsz=512   attr=2, projid32bit=1
         =                       crc=1        finobt=0, sparse=0
data     =                       bsize=4096   blocks=1011968, imaxpct=25
         =                       sunit=0      swidth=0 blks
naming   =version 2              bsize=4096   ascii-ci=0 ftype=1
log      =internal log           bsize=4096   blocks=2560, version=2
         =                       sectsz=512   sunit=0 blks, lazy-count=1
realtime =none                   extsz=4096   blocks=0, rtextents=0
```

---

## mount(挂载)

- 将 /dev/sdb4 挂载在 /mon目录

```shell
mount /dev/sdb4 /mon
vi /etc/fstab
```
