# Zookeeper

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
   > 检查 ZXID, ZXID 最大的优先选为 Leader
   > ZXID 相同时，myid 最大的优先选为 Leader
   > 根据处理比对的结果，失败的服务器更新自己的投票信息，重新发起投票。

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

### 选举算法

#### 发起投票

- SID：用于唯一标识集群中的某一台服务器，与 myid 一致
- ZXID：事务 ID
- Vote：投票（状态为 LOOKING 的机器向集群发送的消息称之为 投票）
- Quorum：过半机器数

#### 变更投票

- vote_sid：接收到的投票所推举的服务器的 SID
- vote_zxid：接收到的投票所推举的服务器的 ZXID
- self_sid：当前服务器的 SID
- self_zxif：当前服务器的 ZXID

```python
# 变更规则
if vote_zxid > self_zxid:
  return "认可该投票，并将自己的投票发送出去"
elif vote_zxid = self_zxid:
  if vote_sid > self_sid:
    return  "认可该投票，并将自己的投票发送出去"
  else:
    return "坚持自己的投票"
else:
  return "坚持自己的投票"
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
