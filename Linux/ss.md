# SS(Socket Statistics)

## 和 netstat 比较

1. netstat 遍历 /proc 每个 PID 目录，ss 直接读取 /proc/net 目录
2. ss 随着连接数增长的时候速度会比 netstat 越来越快，原因是 ss 使用 TCP 协议栈中的 tcp_diag 模块

## 使用

```shell
# 查看统计信息
ss -s

# 查看监听状态的套接字
ss -l

# 查看所有状态的套接字
ss -a

## 查看已建立连接的套接字
ss -a state established

## 以数字形式显示地址和端口
ss -n

## 按协议显示套接字
ss -t(tcp) -u(udp) -4(ipv4) -6(ipv6) -x(unix) -w(raw) -f=(输入指定协议族)

## 显示相关进程信息
ss -p

## 查看进程与端口监听
ss -lntp | grep ${port}

## 查看已建立的 TCP 连接数
ss -ant state established | wc -l

```

## 输出内容

- Recv-Q: 接收队列
- Send-Q: 输出队列
- State: 连接状态
- Local Address: 连接本机的本机 ip(当有本机有多个 ip 时, 0.0.0.0 表示所有本机的 ip)
- Peer Address: 连接本机的外部 ip

### 连接状态

1. LISTENING
2. SYN-SENT
3. SYN-RECV
4. ESTABILSHED
5. FIN-WAIT1
6. CLOSE-WAIT
7. FIN-WAIT2
8. LAST-ACK
9. TIME-WAIT
10. CLOSING
11. CLOSED
12. UNKNOWN