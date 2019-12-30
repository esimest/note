# ps(Process Status)

## 进程状态

- `D`: 不可中断的睡眠 (通常为等待 IO) == 无法接收信号
- `R`: 运行中或可运行(当前进程在运行队列中)
- `S`: 可中断的睡眠 (通常为等待某个事件完成) == 可以通过信号结束该进程
- `T`: 被任务管理信号关闭
- `t`: 在跟踪期被调试器关闭
- `X`: 死亡状态(不可能出现在 ps 的结果中)
- `Z`: 僵死, 终止后没有被父进程重新启动.

### 对于 BSD 的格式有以下特殊输出

- `<`: 优先级高.

- `N`: 优先级低.

- `L`: `has pages locked into memory (for real-time and custom IO)`.

- `s`: 该进程是会话的维护进程.

- `l`: 多线程进程.

- `+`: 前台进程组中的进程.

## 选项

ps [options]

options 分以下三类(最好不要混用):

- BSD 风格 options, 以字母为选项 如 ps aux
- UNIX 风格 options,以 `-` 开头如 ps -ef
- GUN 风格 options, 以 `--` 开头

### 结果过滤类选项

- `a`: 列出所有带有终端 (tty) 的进程, 和 `x` 选项一起使用会列出所有进程.

- `x`: 列出当前用户所有进程 ( 和 ps 进程的 EUID 相同的进程 ), 和 `a` 选项一起使用会列出所有进程.

- `g`: 列出当前用户所有带终端 (tty) 的进程.

- `T`: 列出所有与当前终端相关的进程.

- `-A/-e`: 列出所有进程, 与 `ps ax` 相同.

- `-a`: 列出所有与会话维持无关且带有终端的进程.

- `-d`: 列出所有与会话维持无关的进程. (与会话维持有关的进程有 `bash`).

- `r`: 列出所有正在运行的进程.

```shell
[root@localhost ~]# ps ax | wc -l
168
[root@localhost ~]# ps -e | wc -l
168
```

### 结果过滤(通过参数列表)

- `-p/--pid/-${pid}`: 列出 pid 对应的进程号的进程, `-p` 与 `--pid` 后可以指定列表 `"1 2"/ 1,2`.

- `-C ${cmdlist}`: 列出命令名为 `cmdlist` 指定的命令名的进程.

- `-G ${grouplist}/--Group=${grouplist}`: 列出所有真实所属组 ID 与 组名 在 grouplist 中的进程.

- `-g ${grouplist}/--group=${grouplist}`: 列出所有有效所属组 ID 与 组名 在 grouplist 中的进程.

- `--ppid`: 通过父进程 ID 过滤.

- `q/-q/--qid=`: 通过进程 ID 过滤(快速模式:在此模式下, 不允许使用其他选择选项 排序和 进程树列表)

- `-s/--sid=`: 通过会话 ID 过滤.

- `t/-t/--tty=`: 通过终端名称过滤.

- `U/-u/--user=`: 通过有效用户 ID 过滤.

- `-U/--User=`: 通过真实用户 ID 过滤.

### 输出格式控制类选项

- `-c`: 输出 `PID CLS PRI TTY TIME CMD`

- `--context`:

- `-f`: 输出 `UID PID PPID C STIME TTY TIME CMD`

- `-F`: 输出 `UID PID PPID C SZ RSS PSR STIME TTY TIME CMD`

- `o/-o/--format=`: 自定义输出项

- `j`: 输出 `PPID PID PGID SID TTY TPGID STAT UID TIME COMMAND`

- `-j`: 输出 `PID PGID SID TTY TIME CMD`

- `l`: 输出 `F UID PID PPID PRI NI VSZ RSS WCHAN STAT TTY TIME COMMAND`

- `-l`: 输出 `F S UID PID PPID C PRI NI ADDR SZ WCHAN TTY TIME CMD`

- `Z/-M`: 添加一列 `LABEL`

- `s`: 输出 `UID PID PENDING BLOCKED IGNORED CAUGHT STAT TTY TIME COMMAND`

- `u`: 输出 `USER PID %CPU %MEM VSZ RSS TTY STAT START TIME COMMAND`

- `v`: 虚拟内存, 输出 `PID TTY STAT TIME MAJFL TRS DRS RSS %MEM COMMAND`

- `X`: 输出 `PID STACKP ESP EIP TMOUT ALARM STAT TTY TIME COMMAND`

- `-y`: 只能配合 `-l` 选项使用，将 `ADDR` 列换为 `RSS`

### 输出修改类选项

- `--width n/--cols=n/--columns=n`: 控制每列的宽度为 n, 以字符为单位.

- `--lines n/--rows=n`: 设置每页的行数为 n.

- `e`: 在最后一列后追加环境变量, 如果 COMMAND 没有输出完会先将 COMMAND 输出完整，然后追加环境变量.

- `f/-H/--forest`: 显示进程树

- `h/--no-headers/--no-heading`: 不显示第一行(标题行)

- `--headers`: 当输出跨多个页面时，每页第一行输出标题行. (配合 `--lines/--rows` 一起使用)

- `k/--sort=`: 排序

- `n`: 数字显示 `WCHAN` 和 `USER` 列对应的值

- `-n/N`:

- `S`: 将一些统计值如 CPU 使用率、内存使用率、CPU 使用时间等. 将子进程所占用的资源累加到父进程

- `ww/-ww`: 不限制每列的输出范围

### 线程输出选项

- `H`: 将线程当作进程输出

- `-L`:

- `m/-m`: 在每个进程下面显示线程的信息

- `-T`: 使用新增列 `SPID` 显示线程信息

### 其它选项

- `--info`: 输出调试信息

- `L`: 显示所有可选的输出列格式

- `V/-V/--version`: 输出 `ps` 的版本信息

## 排序可选值

### `O` 选项排序

- `c/cmd`: 可执行文件的名字

- `C/pcpu`: `cpu` 利用率

- `f/flags`: `F` 列的值

- `g/pgrp`: 进程所属组 ID

- `G/tpgid`: 控制进程的终端进程的所属组 ID

- `j/cutime`: 用户累计使用的 `CPU` 时间

- `J/cstime`: 系统累计使用的 `CPU` 时间

- `k/utime`: 用户时间

- `m/min_flt`: `number of minor page faults`

- `M/maj_flt`: `number of minor page faults`

- `n/cmin_flt`: `number of minor page faults`

- `N/cmaj_flt`: `number of minor page faults`

- `o/session`: 会话 ID

- `p/pid`: 进程 ID

- `P/ppid`: 父进程 ID

- `r/rss`: 进程设置的常驻内存

- `R/resident`: 进程使用的常驻内存

- `s/size`: 内存大小(kb)

- `S/share`: 共享页的数量

- `t/tty`: `tty` 对应的设备号

- `T/start_time`: 进程的启动时间

- `U/uid`: 用户 ID

- `u/user`: 用户名

- `v/vsize`: 进程使用的总虚拟内存大小(kb)

- `y/priority`: 进程优先级

### `--sort=` 选项排序, 输出列含义

| CODE | HEADER | DESCRIPTION | ALIAS|
| :--  | :--    | :--         | :--  |
| %cpu | %CPU   | cpu 使用率   | pcup |
| %mem | %MEM   | rss/物理内存 | pmem |
| args | COMMAND | 命令使用的参数| cmd, command|
| blocked | BLOCKED || sig_block, sigmask |
| bsdstart | START | 命令启动时间 | lstart, start, start_time, stime |
| bsdtime  | TIME | 进程使用的 CPU 时间( uset + sys ) | 无 |
| c | C | 处理器使用率 | 进程生命周期内的 CPU 使用率(整数表示) | %cpu |
| caught | CAUGHT | 无 | |
| cgroup | CGROUP | 进程所属的控制组 | 无 |
| class | CLS | 进程的调度类别  | policay, cls|
| comm | COMMAND | 可执行文件的名字 | 无 |
| cp | CP |  cpu 使用率(千分之一为单位) | 无 |
| time | TIME | cpu 使用时间 ([DD-]hh:mm:ss 格式) | time|
| drs | DRS | 驻留内存集的大小(不包含代码占用的空间) | 无 |
| egid | EGID | 进程的有效所属组 ID | gid |
| egroup | EGROUP | 进程的有效所属组名称 | group |
| eip | EIP | instruction pointer. | 无 |
| esp | ESP | stack pointer| 无 |
| etime | ELAPSED | 进程启动后经过的时间([DD-]:hh:mm:ss 格式) | 无 |
| etimes | ELAPSED | 进程启动后经过的时间(秒为单位) | 无 |
| euid | EUID | 有效用户 ID | uid |
| euer | EUSER | 有效用户名 | user |
| f | F | 进程的 flags | flag, flags |
| fgid | FGID | filesystem access group ID | fsgid |
| fgroup | FGROUP | filesystem access group NAME | fsgroup |
| fname | COMMAND | 可执行文件的名字(截取前 8 字节) | 无 |
| fuid | FUID | filesystem access user ID | fsid |
| fuser | FUSER | filesystem access user NAME | 无 |
| ignored | IGNORED | mask of the ignored signals | sig_ignore, sigignore |
|ipcns | IPCNS | 进程所属 IPC namespace 的文件描述符的 inode | 无 |
| label | LABEL | 安全标签 | 无 |
| lsession | SESSION | 登录会话的标识符 | 无 |
| lwp | LWP | 轻量级进程(线程) 的 id | spid, tid |
| machine | MACHINE | displays the machine name for processes assigned to VM or container |
| maj_flt | MAJFLT | The number of major page faults that have occurred with this process. | 无 |
|min_flt | MINFLT | The number of min page faults that have occurred with this process. | 无 |
| mntns | MNTNS | 进程所属 MNT namespace 的文件描述符的 inode | 无 |
| netns | NETNS | 进程所属 NET namespace 的文件描述符的 inode | 无 |
|ni | NI | 进程的 nice 值 | nice |
| nlwp | NLWP | 进程的线程数 | thcount |
| nwchan | WCHAN | 进程失眠时所执行的函数的地址(正在运行的进程该值为 `-`) | 无 |
| ouid | OWNER | 进程所属会话的属主 | 无 |
| pending | PENDING | mask of the pending singals | sig, sig_pend |
| pgid | PGID | 进程组 ID 或是进程属组的 ID  | pgrp |
| pid | PID | 进程 ID | tgid |
| pidns | PIDNS | 进程所属的 PID namespace 的文件描述符的 inode | 无 |
| ppid | PPID | 父进程 ID | 无 |
| pri | PRI  | 进程的优先级 | 无 |
| psr | PSR | 处理该进程的处理器 | 无 |
| rgid | RGID | 进程所属的真实 group id | 无 |
| rgroup | RGROUP | 进程所属的真实 group name | 无 |
| rss | RSS | 驻留内存集大小, 不包括虚拟内存(单位 kb) | rssize, rsz |
| rtprio | RTPRIO | realtime priority | 无 |
| ruid | RUID | 真实用户 ID | 无 |
| ruse | RUSER | 真实用户名 | 无 |
| s | S | 进程状态 | state |
| sched | SCH | 调度策略 | 无 |
| seat | SEAT | 与进程 workspace 相关的硬件的标识符 | 无 |
| sess | SESS | 会话进程的 PID | session, sid |
| sgi_p | P | 运行进程的处理器, 不在运行队列的进程该值显示 `*` | 无 |
| sgid | SGID | saved group id | svgid |
| sgroup | SGROUP | saved group name | 无 |
| size | SIZE | 将进程所有可写页弄脏，交换出去所需要的虚拟内存大小 | 无 |
| slice | SLICE | displays the slice unit with a process belongs to | 无 |
| stackp | STACKP | 进程使用的栈的起始地址 | 无 |
| stat | STAT | 多字符进程状态 | 无 |
| suid | SUID | saved user id | svuid |
| supgid | SUPGID | 补充组的组 ID  | 无 |
| supgrp | SUPGRP | 补充组的组名称 | 无 |
| suser | SUSER | saved user id | 无 |
| sz | SZ | 进程所占物理页大小 | 无 |
| thcgr | THCGR | 线程所属控制组 | 无 |
| tname | TTY | 控制终端的名称 | tt, tty |
| tpgid  | TPGID | 前台终端进程的所属组 ID | 无 |
| trs | TRS | 代码所占物理内存大小 | 无 |
| unit | UNIT | 进程所属的单元 | 无 |
| userns | USERNS | 进程所属的 USER namespace 的文件标识符的 inode | 无 |
| utsns | UTSNS | 进程所属的 UTS namespace 的文件标识符的 inode  | 无 |
| uunit | UUNIT | 进程所属的用户单元 | 无 |
| vsize | VSZ | 进程所使用的虚拟内存(交换内存) | vsz |
| wchan | WCHAN | 导致进程睡眠的内核函数的名称( 正在运行的进程该值显示 `-`, 多线程的进程该值显示 `*`) | 无 |

### PS 可用的环境变量

- `COLUMNS`: 每列可显示的字符个数

- `LINES`: 行高

- `PS_PERSONALITY`:

- `CMD_ENV`:

- `I_WANT_A_BROKEN_PS`: 强制执行过时的命令行解释.

- `LC_TIME`: 时间格式

- ` PS_COLORS`: 暂不支持

- `PS_FORMAT`: 默认的输出列组合

- `PS_SYSMAP`: 默认的 namelist 位置.

- `PS_SYSTEM_MAP`: 默认的 namelist 位置.

- `POSIXLY_CORRECT`: `Don't find excuses to ignore bad "features".`

- `POSIX2`: 当设置为 `on` 时, 行为和 `POSIXLY_CORRECT` 一样.

- `UNIX95`: `Don't find excuses to ignore bad "features".`

- `_XPG`: 关闭 `CMD_ENV=irix` 的行为


## 命令使用

```shell

```