# HDFS 中的 ZKFC

ZKFC(ZooKeeper Failover Controller):
  NN 的高可用的一种实现机制

## 实现原理

> 依赖 zk 的数据强一致性，临时借点以及 watcher

1. Health monitoing
   > zkfc 定期对本地的 NN 发起 health-check 的命令，如果 NN 返回正常，则认定
   > 此 NN 状态是 OK 的，否则认为节点失效。
2. ZooKeeper Session Management
   > 如果本地 NN 状态正常，zkfc 会在 zk 持有一个 session。当 NN 正好是 active 时，
   > zkfc 还会在 zk 中持有一个临时节点的节点作为锁，一旦本地 NN 失效，
   > 这个节点就会被删除
3. ZooKeeper-based election
   > 如果本地 NN 为健康的，且 zkfc 发现并没有其他 NN 持有"ephemeral"。那么他将试图获> 取该znode，一旦成功，zkfc 需要执行 failover，然后成为 acitve。
   - Failover
     1. 对之前的 NN 执行 fence
     2. 将本地 NN 转换为 acitve

## HDFS 在 zk 中的 znode

> HDFS 在 zk 中存有两个节点，目录为 /hadoop-ha/cluster

- ActiveStandbyElectorLock
   > 临时节点，持有该节点的 nn 为 active nn

- ActiveBreadCrumb
   > 持久节点，负则在会话关闭后，下次能够正确分配 active nn
