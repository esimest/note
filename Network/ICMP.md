# ICMP(Internet Control Message Protocol)

> IP 协议通过 ICMP 实现差错控制
> ICMP 是网络层的协议，但是不像 IP 协议和 ARP 协议直接发送数据给链路层
> ICMP 先封装成 IP 报文然后传送给链路层
> 当 IP 报文头中 protol(上层协议) 字段为 1(TCP 为 6) 时，传输的时 ICMP 报问

## ICMP 报文结构

- Type(8 bits): ICMP 报文类型
- Code(8 bits): 类型细分
- Checksum(16bits): 首部 + 报文体的检验和
- 首部其余部分(对于不同的 Type 和 Code 对应不同的剩余部分)
- 报文体

## ICMP 报文分类

### 差错控制报文

> 用来报告错误而不是纠正错误

#### Type

- 3(Destination Unreachable)
   > Code 0: Net Unreachable
   > Code 1: Host Unreachable
   > Code 2: Protol Unreachable
   > Code 3: Port Unreachable
   > Code 4:
   > Code 5: Source Route Failed
   > Code 6: Destination Network Unkonwn
   > Code 7: Destination Host Unknown
   > Code 8: Source Host isolated
   > Code 9:
   > Code 10:
   > Code 11:
- 4(Source quench)
   > 目标主机的处理能力无法匹配源主机的发送速度，提醒源主机发送慢点
- 5(Redirect):
- 11(Time Exceeded)
   > Code 0: IP 报文中 TTL 字段减为 0，依旧没有到达目标主机
   > Code 1: 目标主机接收 IP 分片是，当接收到第一个 IP 分片后在指定时间内没有接收到最后一个 IP 分片
- 12(Parameter Problem)
   > 参数错误


### 查询报文

#### Type

- 0(echo request)
   > 回显请求报文
- 8(echo reply)
   > 回显应答报文
- 13(timestamp echo request)
   > 回显请求报文(带时间戳), 可用于时间同步
- 14(timestamp echo reply)
   > 回显应答报文(带时间戳)


## Ping 命令

### 参数

- d: 使用Socket的SO_DEBUG功能。

- f:  极限检测。大量且快速地送网络封包给一台机器，看它的回应。

- n: 只输出数值。

- q: 不显示任何传送封包的信息，只显示最后的结果。

- r: 忽略普通的Routing Table，直接将数据包送到远端主机上。通常是查看本机的网络接口是否有问题。

- R: 记录路由过程。

- v: 详细显示指令的执行过程。

- c: 数目：在发送指定数目的包后停止。

- i: 秒数：设定间隔几秒送一个网络封包给一台机器，预设值是一秒送一次。

- I: 指定网卡

- l: 前置载入：设置在送出要求信息之前，先行发出的数据包。

- p: 范本样式：设置填满数据包的范本样式。

- s: 字节数：指定发送的数据字节数，预设值是56，加上8字节的ICMP头，一共是64ICMP数据字节。

- t: 存活数值：设置存活数值TTL的大小。