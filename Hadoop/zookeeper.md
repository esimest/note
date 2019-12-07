# Zookeeper(分布式应用协同服务)

> 分布式数据一致性解决方案

Zookeeper 事务:
  能够改变 Zookeeper 服务器状态的操作(包括数据的更新、会话的创建与失效)
  Zookeeper 会为每个事务分配一个事务ID(ZXID), 每个 ZXID 对应一个更新操作。
  ZXID 是全局的

## 分布式系统

### 概述

> 分布式系统是一个硬件或软件组件分布在不同网络计算机上，彼此之间仅仅通过
> 消息传递进行通信和协调的系统。

### 特征

- 分布性
- 对等性
- 并发性
- 缺乏全局时钟
- 故障总是会发生

### 分布式带来的问题

- 通信异常(网络问题)
- 网络分区(split brain)
- 三态(成功、失败、超时)
- 节点故障

## CAP 和 BASE

### CAP理论

> Consitency(一致性)、Availability(可用性)、Partition tolerance(分区容错性) 同时只能满足两个

网络分区:
  分布式系统中，不同节点分布在不同子网内，当发生网络故障时，导致子网之间无法通信，但是子网内通信
  正常，从而导致整个网络被划分成多个孤立的子网。

- 一致性
  > 多副本之间数据保持一致

- 可用性
  > 有限时间内返回正确结果

- 分区容错性(必须要保证)
  > 系统在遇到任何网络分区故障时，任然需要对外部保证一致性和可用性，除非是整个网络故障

### BASE(Basic Avaiability、Soft state、Eventually consistency)

- 基本可用
- 软状态
- 最终一致性
  > 系统中的所有数据副本，在经过一段时间后，最终能达到一致性

### 最终一致性的变种

- 因果一致性
- 读已知所写
- 会话一致性
- 单调读一致性
- 单调写一致性

## Zookeeper 提供的服务

### 数据一致性

- 顺序一致性
  > 同一客户端发起的事物请求，会严格按照发起顺序被应用到 ZK 中
- 原子性
  > 所有事物请求的处理结果在集群中所有节点上的应用情况是一致的，只存在全都应用和全都没用两种情况
- 单一视图
  > 无论客户端连接的是集群中的哪个节点，看到的服务端数据模型都是一致的
- 可靠性
  > 等同于持久性
- 实时性
  > 一段时间内，客户端最终能从服务端读取到数据的最新状态

## ZAB(Zookeeper Atomic Broadcast: 原子消息广播协议)

### ZAB 核心

> 所有事物请求必须由一个全局唯一的服务器(Leader)来协调处理。Leader 服务器负责将一个客户的端的事物请求转换成一个事务 Proposal, 并将该 Proposal 分发给集群中的所有 Follower。之后 Leader 许需要等待所有 Follower 的反馈，一旦超过半数的 Follower 进行了正确的反馈后，Leader 就会向所有 Follower 发送 Commit 消息，要求将前一个 Proposal 进行提交。

### 崩溃恢复

> Leader 故障时，节点的状态变更为 LOOKING 并重新进行选举。

## Leader 选举

### 集群初始化时的 Leader 选举

1. 发起投票
   > 投票的信息里包括(myid, ZXID)，集群初始化时所有投票的 ZXID(事务ID) 都为0。

2. 接收其他服务器的投票
   > 每个服务器都会接收来自其它服务器的投票。

3. 处理投票
   > **依次检查来自其它节点的所有投票**
   > 将其它投票与自己的投票进行对比
   > 如果比较后自己是失败方，则要变更自己的投票，否则坚持自己的投票

4. 统计投票
   > 每次投票后，服务器统计所有投票，判断是否已经有过半的机器接收到相同的投票信息。如果有，则认为 Leader 已经选举出来了

5. 改变服务器状态
   > Leader 的状态改为 LEADING, Follower 的状态改为 FOLLOWINNG

### 运行期间的 Leader 选举

1. 变更状态
   > Leader 故障后，余下的所有非 Observer 节点都会将自己的状态变更为 LOOKING，然后开始选举

2. 发起投票
   > 由于在运行状态，所以会随机生成 ZXID

3. 接收投票
4. 处理投票
5. 统计投票
6. 改变服务器状态

#### 发起投票

- SID：用于唯一标识集群中的某一台服务器，与 myid 一致
- ZXID：事务 ID
- Vote：投票（状态为 LOOKING 的机器向集群发送的消息称之为 投票）
- Quorum：过半机器数

#### 变更投票

- vote_sid：接收到的投票所推举的服务器的 SID
- vote_zxid：接收到的投票所推举的服务器的 ZXID
- self_sid：当前服务器的投票所推举的服务器的 SID
- self_zxif：当前服务器的投票所推举的服务器的 ZXID

```python
# 变更规则
def count_vote():
    return '统计所有的投票结果'
def vote_slefs():
    return '向其他节点投自己'
def receive_votes():
    return '从其它节点接收投票'

vote_self()
receive_votes()
count_votes()
if '有超过半数的投票':
    return '选出 Leader'
else:
    for (vote_sid, vote_zxid) in others_vote:
        if vote_zxid > self_zxid:
            self_sid, self_zxid = (vote_sid, vote_zxid)
        elif vote_zxid = self_zxid:
            if vote_sid > self_sid:
                self_sid, self_zxid = (vote_sid, vote_zxid)
            else:
                pass
        else:
            pass
    return '发起第二轮投票'
```

#### 确定 Leader

> 经过变更投票，每台机器统计收到的投票。如果有一台机器的投票数过半，那么就投对应 SID 的机器为 Leader。

## 角色

### Leader

1. 事物请求的唯一调度和处理者，保证集群事务处理的顺序性。
2. 集群内部服务器的调度者

### Follower

1. 处理客户端非事务请求，转发事务请求给 Leader
2. 参与事务请求 Proposal 投票
3. 参与 Leader 选举投票

### Observer

1. 处理客户端非事务请求，转发事务请求给 Leader

## 端口

- 2181：用于监听客户端请求
- 2888：用 Leader 监听 Follower 的请求
- 3888：用于选举 Leader

## ACL（权限）

- Create：创建节点的权限
- Read：读取节点数据的权限
- Write：更新节点数据的权限
- Delete：删除节点的权限
- Admin：分配权限的权限

## 会话

> 客户端第一次与服务端建立 TCP 连接时，会话的生命周期就开始了
> 客户端可以通过心跳检测与服务器保持有效的会话

- SessionTimeout
  > 用来设置会话超时时间，客户端连接断开后只要在 SessionTimeout
  > 期间内连接上集群内任一节点，那么之前创建的 session 任然有效

## 事务处理

1. leader 接收事务请求，并同步到 follower
2. 如果超过半数 follower 回应 leader, leader 就发起提交事务的请求
3. leader 返回给 client


## 数据存储

> zk 的数据会保存再内存中

> zk 通过快照和日志实现对数据的备份管理