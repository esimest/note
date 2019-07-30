### 规则(Policy)
> 一条规则就是 条件 + 动作 的组合
> 规则定义了对符合条件的数据包的行为
> 一条规则由五部分组成
1. target 使用iptables -j 指定
> 规则中的行为/动作，表示如何处理符合该条件的流量
> target有 8 类
  - ACCEPT: 允许数据包通过
  - DROP: 直接丢弃数据包，不给客户端任何响应
  - REJECT: 丢弃数据包，并给客户端一条响应信息
  - SNAT: Source Network Address Transmission
  - MASQUERADE: SNAT 的一种特殊形式，适用于动态的、临时会变的 IP 上
  - DNAT: Destinate Network Address Transmission
  - REDIRECT: 在本机上做端口映射
  - LOG: 在 /etc/log/messages 中留下记录，不对数据包做任何操作
2. prot 使用iptables -p 指定
> 规则中的条件：数据包使用的传输层协议(TCP/UPD)
3. source 使用iptables -s 指定
> 规则中的条件：数据包中的源IP地址或网段
4. destination 使用 iptables -d 指定
> 规则中的条件：数据包中的目的地址或网段
5. source_port 使用 iptables --sport 指定
> 规则中的条件：数据包中的源端口号
6. destination_port 使用iptables --dport 指定
> 规则中的条件：数据包中的目的端口号

### 规则链
> 规则链就是规则的集合。针对特定数据包的各种防火墙规则，按照顺序依次放入对应的链中。
- prerouting
> 在对数据包做路由选择之前，应用此链的规则。
- input
> 当收到访问防火墙本地地址的数据包时，应用此链的规则
- output
> 当防火墙本机向外发出数据时，应用此链的规则。
- forward
> 当收到要通过防火墙发送给其他网络地址的数据包时，应用此链的规则。
- postrouting
> 在对数据包做路由选择之后，应用此链的规则。
![](./images/iptables规则链.png)

### 表
> 用于完成特定功能的规则链的集合
> 表的处理优先级： RAW --> MANGLE --> NAT --> FILTER
- filter
> 功能：过滤数据包
> 使用的规则链：INPUT, FORWARD, OUTPUT

- nat
> 功能：network address transmission。转发数据包
> 使用的规则链：PREROUTING, [INPUT, ]OUTPUT, POSTROUTING

- mangle
> 功能：对数据内容进行修改后重新封装
> 使用的规则链：PREROUTING, INPUT FORWARD, OUTPUT, POSTROUTING

- raw 
> 功能：关闭NAT表上启用的连接追踪机制
> 使用的规则链：PREROUTING, OUTPUT

### 数据包的几种流向
- 流入本机
> PREROUTING --> INPUT

- 由本机流出
> OUTPUT --> POSTROUTING

- 转发
> PREROUTING --> FORWARD -->POSTROUTING