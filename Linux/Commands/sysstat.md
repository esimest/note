# SYSSTAT

sysstat -- 用于检测系统性能软件包.
sysstat 工具包中的所有命令的输出都带有 CPU 的统计信息.

```shell
# 安装 sysstat 后默认会设置以下系统定时任务
[root@localhost ~]# cat /etc/cron.d/sysstat
# Run system activity accounting tool every 10 minutes
*/10 * * * * root /usr/lib64/sa/sa1 1 1
# 0 * * * * root /usr/lib64/sa/sa1 600 6 &
# Generate a daily summary of process accounting at 23:53
53 23 * * * root /usr/lib64/sa/sa2 -A
```

## sar(System Activity Report)

sar 是目前 Linux 上最为全面的系统性能分析工具之一, 可以从多方面对系统的活动进行报告.
包括:

- 文件的读写情况

- 系统调用的使用情况

- 磁盘I/O

- CPU效率

- 内存使用状况

- 进程活动

- IPC有关的活动
...

### sar n [m]

每 n 秒钟统计一次, 统计 m 次.

```shell
# 每两秒钟统计一次, 统计三次
[root@localhost ~]# sar 2 3
Linux 3.10.0-693.el7.x86_64 (localhost.localdomain) 	01/09/2020 	_x86_64_	(4 CPU)

10:03:21 AM     CPU     %user     %nice   %system   %iowait    %steal     %idle
10:03:23 AM     all      1.68      0.00      2.19      0.00      0.00     96.13
10:03:25 AM     all      0.78      0.00      1.94      0.00      0.00     97.29
10:03:27 AM     all      0.90      0.00      1.93      0.00      0.13     97.04
Average:        all      1.12      0.00      2.02      0.00      0.04     96.82
```

- all: 标识后面的指标为所有 CPU 的平均值;

- %user: 用户模式下使用的 CPU 时间百分比;

- %nice: 带 NICE 值的用户模式下使用的 CPU 时间百分比;

- %sys: 内核模式下使用的 CPU 时间百分比;

- %iowait: 等待 I/O 所浪费的 CPU 时间;
   > 此指标过高时, 表示硬盘 I/O 存在瓶颈.

- %steal: 管理程序维护另一个虚拟处理器时，虚拟CPU的无意识等待时间百分比;

- %idle: CPU 空闲时间百分比;
   > 次指标过低时, 表示 CPU 处理性较实际场景的需求能相对较低.

### sar -P {<1,2,..> | ALL}

查看具体 CPU 的统计信息

```shell
# 查看 CPU 1 的信息
[root@localhost ~]# sar -P 1 2 1
Linux 3.10.0-693.el7.x86_64 (localhost.localdomain) 	01/09/2020 	_x86_64_	(4 CPU)

10:15:32 AM     CPU     %user     %nice   %system   %iowait    %steal     %idle
10:15:34 AM       1      0.00      0.00      0.00      0.00      0.00    100.00
Average:          1      0.00      0.00      0.00      0.00      0.00    100.00

# 产看 CPU 1 3 的信息
[root@localhost ~]# sar -P 1,3 2 1
Linux 3.10.0-693.el7.x86_64 (localhost.localdomain) 	01/09/2020 	_x86_64_	(4 CPU)

10:17:07 AM     CPU     %user     %nice   %system   %iowait    %steal     %idle
10:17:09 AM       1      1.05      0.00      3.68      0.00      0.00     95.26
10:17:09 AM       3      4.66      0.00      3.63      0.00      0.00     91.71

Average:        CPU     %user     %nice   %system   %iowait    %steal     %idle
Average:          1      1.05      0.00      3.68      0.00      0.00     95.26
Average:          3      4.66      0.00      3.63      0.00      0.00     91.71

# 查看所有的 CPU 信息
[root@localhost ~]# sar -P ALL 2 1
Linux 3.10.0-693.el7.x86_64 (localhost.localdomain) 	01/09/2020 	_x86_64_	(4 CPU)

10:16:16 AM     CPU     %user     %nice   %system   %iowait    %steal     %idle
10:16:18 AM     all      1.55      0.00      2.58      0.00      0.00     95.87
10:16:18 AM       0      0.00      0.00      0.50      0.00      0.00     99.50
10:16:18 AM       1      0.50      0.00      1.50      0.00      0.00     98.00
10:16:18 AM       2      3.23      0.00      4.30      0.00      0.00     92.47
10:16:18 AM       3      3.17      0.00      3.70      0.00      0.00     93.12

Average:        CPU     %user     %nice   %system   %iowait    %steal     %idle
Average:        all      1.55      0.00      2.58      0.00      0.00     95.87
Average:          0      0.00      0.00      0.50      0.00      0.00     99.50
Average:          1      0.50      0.00      1.50      0.00      0.00     98.00
Average:          2      3.23      0.00      4.30      0.00      0.00     92.47
Average:          3      3.17      0.00      3.70      0.00      0.00     93.12
```

### sar -R

内存统计信息

```shell
[root@localhost ~]# sar -R 1 3
Linux 3.10.0-693.el7.x86_64 (localhost.localdomain) 	01/09/2020 	_x86_64_	(4 CPU)

02:59:04 PM   frmpg/s   bufpg/s   campg/s
02:59:05 PM    -39.00      0.00      0.00
02:59:06 PM      0.00      0.00      0.00
02:59:07 PM      0.00      0.00      0.00
Average:       -13.00      0.00      0.00
```

- frmpg/s: 每秒系统释放的页的数量(负数代表分配)

- bufpg/s: 每秒增加的用于 buff 的页的数量(负数代表释放)

- campg/s: 每秒增加的用于 cached 的页的数量(负数代表释放)

### sar -r

内存使用率的统计信息

```shell
[root@localhost ~]# sar -r 2 1
Linux 3.10.0-693.el7.x86_64 (localhost.localdomain) 	01/09/2020 	_x86_64_	(4 CPU)

10:18:21 AM kbmemfree kbmemused  %memused kbbuffers  kbcached  kbcommit   %commit  kbactive   kbinact   kbdirty
10:18:23 AM   5642168   2351640     29.42      2108   1796584   1850992      7.47   1809744    288148      2008
Average:      5642168   2351640     29.42      2108   1796584   1850992      7.47   1809744    288148      2008
```

- kbmemfree: 可用物理内存空间(同 `free` 命令输出的 free 项)

- kbmemused: 已用物理内存空间(同 `free` 命令输出的 used + cache + buff )

- %memused: 已用物理内存空间百分比

- kbbuffers: 内核缓存使用的内存大小(同 `free -w` 命令输出的 buffers 一样)

- kbcached: 页缓存使用的内存大小(同 `free -w` 命令输出的 cached 一样)

- kbcommit: 保证当前系统正常运行所需要的时间

- %commit: `kbcommit/total`

- kbactive: 活跃的内存空间(最近使用的内存, 除非绝对必要通常不会回收)

- kbinact: 不活跃的内存空间()

- kbdirty: 脏数据(更新至内存但是还未同步到磁盘的数据)

### sar -B

内存页统计信息

```shell
[root@localhost ~]# sar -B 1 1
Linux 3.10.0-693.el7.x86_64 (localhost.localdomain) 	01/09/2020 	_x86_64_	(4 CPU)

03:06:14 PM  pgpgin/s pgpgout/s   fault/s  majflt/s  pgfree/s pgscank/s pgscand/s pgsteal/s    %vmeff
03:06:15 PM      0.00      0.00     25.00      0.00     50.00      0.00      0.00      0.00      0.00
Average:         0.00      0.00     25.00      0.00     50.00      0.00      0.00      0.00      0.00
```

- pgping/s: 每秒从磁盘或虚存置换到内存的页数量.

- pgpgout/s: 每秒从内存置换到磁盘或虚存的页数量.

- fault/s: 每秒系统产生的缺页数.

- majflt/s: 每秒系统产生的主缺页数.

- pgfree/s: 每秒进入空闲队列的页数.

- pgscank/s: 每秒被 kswapd 扫描的页数.

- pgscand/s: 每秒被直接扫描的页数.

- pgsteal/s: 每秒从 cache 钟被清除出来满足内存需求的页数量.

- %vmff: pgsteal/(pgscank + pgscand)

## sa1

按日收集系统活动数据, 并以二进制格式写入文件中(/var/log/sa/sa${day of month} file).

## sa2

按日收集系统活动数据, 并以二进制格式写入文件中(/var/log/sa/sar${day of month} file).

## sadc(System Acitvity Data Collector)

## sadf(System Activity Data Formater)

## pidstat(Pid Statistics)

## vmstat(Virtual Memory Statistics)

## iostat(I/O Statistics)

## cifsiostat(Common Internet File System iostat)

## nfsiostat(Network File System iostat)

## mpstat

## sysstat
