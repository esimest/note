# Linux 名称空间

## 作用

> namespace 实现了对内核资源的隔离(隔离是相对与进程而言的)


## 六种 NS

|  名称   |  隔离的资源                             |
| :----   |  :----                                  |
| IPC     |  信号量、消息队列、共享内存...           |
| Network |  网络设备、端口、IP...                   |
| Mount   |  文件系统挂载点(目录)(通过 chroot 实现)  |
| PID     |  进程号                                  |
| User    |  用户、用户组                            |
| UTS     |  主机名和 NIS 域名                       |
| cgroups |  硬件资源(cpu mem disk ...)              |