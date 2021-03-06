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
ss -lntp state dport = :${port} or sport = :${port}

## 查看已建立的 TCP 连接数
ss -ant state established | wc -l

```

## 输出内容

- Netid: 套接字类型
- Recv-Q: 接收队列
- Send-Q: 输出队列
- State: 连接状态
- Local Address: 本机监听的 IP:PORT(如果 ip==127.0.0.1 则只能本机访问)
- Peer Address: 如果套接字已连接, 显示对端的 ip:port

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

### 套接字类型

- tcp

- udp

- raw

- u_str(unix_stream)

- u_dgr(unix_datagram): unix 数据报

- nl(netlink)

- p_dgr: 数据报套接字

- p_raw: raw 包套接字
