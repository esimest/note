> PDU(Protocol Data Unit)
- 实验内容
  1. 创建一个交换机（2960-24TT），4个终端ABCD
  2. 启动A --> B 的MAC帧转换过程
  3. 观察交换机转发表的变化过程
  4. 检查ICMP报文到MAC帧的封装过程

- 实验目的
  1. 验证交换机的连通性
  2. 验证转发表的建立过程
  3. 验证交换机MAC帧转发过程
  4. 验证ICMP报文逐层封装的过程

- 转发表结构
  1. MAC地址
  2. 转发端口（交换机的还口号）


- 转发过程
  - 目的MAC地址为广播地址，则广播
  - 目的MAC地址为单播地址，但是转发表中没有匹配项，则广播
  - 目的MAC地址为单播地址，转发表存在匹配项，转发至目的MAC地址


- 实验过程
  1. 清空交换机转发表
  2. 建立终端A与终端C之间的ICMP报文传输过程
  3. 查看报文传输过程
  4. 查看报文内容


- 结论
  1. 终端A实现了3层协议（网络层、传输层和物理层）
  2. 终端A将封装好，并发送给交换机
  3. 交换机接收报文，将报文解析成运链路层报文，并获取目的终端的MAC地址
  4. 交换机重新将报文封装好，根据转发表进行匹配并转发。

- 问题
  1. 终端A的报文封装的是终端B的MAC地址，他为什么会发送到交换机上呢？暂时不能确定答案
