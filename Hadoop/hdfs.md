# HDFS

## 基础架构

### Block

1. 基本存储单位，一般大小为 64M（配置大的块主要是因为：
   1. 减少搜寻时间，一般硬盘传输速率比寻道时间要快，大的块可以减少寻道时间
   2. 减少管理块的数据开销，每个块都需要在 NameNode 上有对应的记录
   3. 对数据块进行读写，减少建立网络的连接成本）
2. 一个大文件会被拆分成一个个的块，然后存储于不同的机器。如果一个文件少于 Block 大小，那么实际占用的空间为其文件的大小
3. <font color=red>每个块都会被复制到多台机器，默认复制 3 份</font>

### NameNode

> 对 namenode 高可用测试可以先下掉一个 namenode 然后观察 hdfs 是否可以正常工作
> nn 会将 clinet 对数据的操作写入 edits log 中

1. 存储文件的 metadata，运行时所有数据都保存到内存，整个 HDFS 可存储的文件数受限于 NameNode 的内存大小
2. 一个 Block 在 NameNode 中对应一条记录（一般一个 block 占用 150 字节），如果是大量的小文件，会消耗大量内存。同时 map task 的数量是由 splits 来决定的，所以用 MapReduce 处理大量小文件时，就会产生过多的 map task，线程管理开销将会增加作业时间。处理大量小文件的速度远远小于处理同等大小的大文件的速度。因此 Hadoop 建议存储大文件
3. 数据会定时保存到本地磁盘，但不保存 block 的位置信息，而是由 DataNode 注册时上报和运行时维护（NameNode 中与 DataNode 相关的信息并不保存到 NameNode 的文件系统中，而是 NameNode 次重启后，动态重建）
4. <font color=red>NameNode 失效则整个 HDFS 都失效了，所以要保证 NameNode 的可用性</font>

### Secondary NameNode

1. 定时与 NameNode 进行同步（定期合并文件系统镜像和编辑日志，然后把合并后的传给 NameNode，替换其镜像，并清空编辑日志，类似于 CheckPoint 机制），<font color=red>但 NameNode 失效后仍需要手工将其设置成主机</font>

### DataNode

1. 保存具体的 block 数据
2. 负责数据的读写操作和复制操作
3. DataNode 启动时会向 NameNode 报告当前存储的数据块信息，后续也会定时报告修改信息
4. DataNode 之间会进行通信，复制数据块，保证数据的冗余性

## 文件写入过程

1. 客户端将文件写入本地磁盘的临时文件中
2. 当临时文件大小达到一个 block 大小时，HDFS client 通知 NameNode，申请写入文件
3. NameNode 在 HDFS 的文件系统中创建一个文件，并把该 block id 和要写入的 DataNode 的列表返回给客户端
4. 客户端收到这些信息后，将临时文件写入 DataNodes
   1. 客户端将文件内容写入第一个 DataNode（一般以 4kb 为单位进行传输）
   2. 第一个 DataNode 接收后，将数据写入本地磁盘，同时也传输给第二个 DataNode
   3. 依此类推到最后一个 DataNode，数据在 DataNode 之间是通过 pipeline 的方式进行复制的
   4. 后面的 DataNode 接收完数据后，都会发送一个确认给前一个 DataNode，最终第一个 DataNode 返回确认给客户端
   5. 当客户端接收到整个 block 的确认后，会向 NameNode 发送一个最终的确认信息
   6. 如果写入某个 DataNode 失败，数据会继续写入其他的 DataNode。然后 NameNode 会找另外一个好的 DataNode 继续复制，以保证冗余性
   7. 每个 block 都会有一个校验码，并存放到独立的文件中，以便读的时候来验证其完整
5. 文件写完后（客户端关闭），NameNode 提交文件（这时文件才可见，֘#x5982; 如果提交前，NameNode 垮掉，那文件也就丢失了。fsync：只保证数据的信息写到 NameNode 上，但并不保证数据已经被写到 DataNode 中）

## 机器感知

> 通过配置文件指定机架名和 DNS 的对应关系
> 假设复制参数是 3，在写入文件时，会在本地的机架保存一份数据，然后在另外一个机架内保存两份数据（同机架内的传输速度快，从而提高性能）
> 整个 HDFS 的集群，最好是负载平衡的，这样才能尽量利用集群的优势

## 文件读取过程

1. 客户端向 NameNode 发送读取请求
2. NameNode返回文件的所有 block 和这些 block 所在的 DataNodes（包括复制节点）
3. 客户端直接从 DataNode 中读取数据，如果该 DataNode 读取失败（DataNode 失效或校验码不对），则从复制节点中读取（如果读取的数据就在本机，则直接读取，否则通过网络读取）

## 可靠性

- DataNode可失效
  1. DataNode 会定时发送心跳到 NameNode。如果一段时间内 NameNode 没有收到 DataNode 的心跳消息，则认为其失效。此时 NameNode 就会将该节点的数据（从该节点的复制节点中获取）复制到另外的 DataNode 中

- 数据可以毁坏
  1. 无论是写入时还是硬盘本身的问题，只要数据有问题（读取时通过校验码来检测），都可以通过其他的复制节点读取，同时还会再复制一份到健康的节点中

- <font color=red> NameNode不具备可靠性，需要做高可用</font>

## NN 间数据同步

> NN 间数据同步，通过 JN 进行数据通信

## command

[hdfs 命令手册](http://hadoop.apache.org/docs/r1.0.4/cn/commands_manual.html)

> hdfs 以 hadoop fs 或 hdfs dfs 开始，后接参数
> admin 将 dfs 替换成 dfsadmin
> 检查命令将 fs 替换成 fsck

```shell
# 查看 datanode 信息
hdfs dfsadmin -report

# 查看机架感知
hdfs  dfsadmin  -printTopology

# 查看 NN 状态
hdfs haadmin -getServiceState namenode1/namenode2

# 查看数据损坏
hdfs fsck -list-corruptfileblocks

# 平衡 datanode 数据
hdfs balancer -policy datanode
```
