1、某个组件的功能，是干什么的，能解决什么问题（在TCE全局是怎样的位置）；
2、部署前要准备什么，依赖什么；  
3、部署过程的注意项；
4、部署完的验证过程；
5、一般运维的方法
> 本文侧重介绍HDFS工作原理，通过对HDFS工原理的介绍，来解释平时部署过程中遇到的一些问题的原因，以及解决方向。

### 基础架构
- Block
  1. 基本存储单位，一般大小为 64M（配置大的块主要是因为：
    1. 减少搜寻时间，一般硬盘传输速率比寻道时间要快，大的块可以减少寻道时间
    2. 减少管理块的数据开销，每个块都需要在 NameNode 上有对应的记录
    3. 对数据块进行读写，减少建立网络的连接成本）
  2. 一个大文件会被拆分成一个个的块，然后存储于不同的机器。如果一个文件少于 Block 大小，那么实际占用的空间为其文件的大小
  3. <font color=red>每个块都会被复制到多台机器，默认复制 3 份</font>

- NameNode
  1. 存储文件的 metadata，运行时所有数据都保存到内存，整个 HDFS 可存储的文件数受限于 NameNode 的内存大小
  2. 一个 Block 在 NameNode 中对应一条记录（一般一个 block 占用 150 字节），如果是大量的小文件，会消耗大量内存。同时 map task 的数量是由 splits 来决定的，所以用 MapReduce 处理大量的小文件时，就会产生过多的 map task，线程管    理开销将会增加作业时间。处理大量小文件的速度远远小于处理同等大小的大文件的速度。因此 Hadoop 建议存储大文件
  3. 数据会定时保存到本地磁盘，但不保存 block 的位置信息，而是由 DataNode 注册时上报和运行时维护（NameNode 中与 DataNode 相关的信息并不保存到 NameNode 的文件系统中，而是 NameNode 每次重启后，动态重建）
  4. <font color=red>NameNode 失效则整个 HDFS 都失效了，所以要保证 NameNode 的可用性</font>

- Secondary NameNode
  1. 定时与 NameNode 进行同步（定期合并文件系统镜像和编辑日志，然后把合并后的传给 NameNode，替换其镜像，并清空编辑日志，类似于 CheckPoint 机制），<font color=red>但 NameNode 失效后仍需要手工将其设置成主机</font>

- DataNode
  1. 保存具体的 block 数据
  2. 负责数据的读写操作和复制操作
  3. DataNode 启动时会向 NameNode 报告当前存储的数据块信息，后续也会定时报告修改信息
  4. DataNode 之间会进行通信，复制数据块，保证数据的冗余性

### 文件写入过程
  1. 客户端将文件写入本地磁盘的临时文件中
  2. 当临时文件大小达到一个 block 大小时，HDFS client 通知 NameNode，申请写入文件
  3. NameNode 在 HDFS 的文件系统中创建一个文件，并把该 block id 和要写入的 DataNode 的列表返回给客户端
  4. 客户端收到这些信息后，将临时文件写入 DataNodes
    1. 客户端将文件内容写入第一个 DataNode（一般以 4kb 为单位进行传输）
    2. 第一个 DataNode 接收后，将数据写入本地磁盘，同时也传输给第二个 DataNode
    3. 依此类推到最后一个 DataNode，数据在 DataNode 之间是通过 pipeline 的方式进行复制的
    5. 后面的 DataNode 接收完数据后，都会发送一个确认给前一个 DataNode，最终第一个 DataNode 返回确认给客户端
    6. 当客户端接收到整个 block 的确认后，会向 NameNode 发送一个最终的确认信息
    7. 如果写入某个 DataNode 失败，数据会继续写入其他的 DataNode。然后 NameNode 会找另外一个好的 DataNode 继续复制，以保证冗余性
    8. 每个 block 都会有一个校验码，并存放到独立的文件中，以便读的时候来验证其完整
5. 文件写完后（客户端关闭），NameNode 提交文件（这时文件才可见，֘#x5982; 如果提交前，NameNode 垮掉，那文件也就丢失了。fsync：只保证数据的信息写到 NameNode 上，但并不保证数据已经被写到 DataNode 中）


<font color=red> Rack aware (机架感知)</font>
---

> 通过配置文件指定机架名和 DNS 的对应关系
> 假设复制参数是 3，在写入文件时，会在本地的机架保存一份数据，然后在另外一个机架内保存两份数据（同机架内的传输速度快，从而提高性能）
> 整个 HDFS 的集群，最好是负载平衡的，这样才能尽量利用集群的优势

### 文件读取过程
1. 客户端向 NameNode 发送读取请求
2. NameNode返回文件的所有 block 和这些 block 所在的 DataNodes（包括复制节点）
3. 客户端直接从 DataNode 中读取数据，如果该 DataNode 读取失败（DataNode 失效或校验码不对），则从复制节点中读取（如果读取的数据就在本机，则直接读取，否则通过网络读取）

### 可靠性
- DataNode可失效
  1. DataNode 会定时发送心跳到 NameNode。如果一段时间内 NameNode 没有收到 DataNode 的心跳消息，则认为其失效。此时 NameNode 就会将该节点的数据（从该节点的复制节点中获取）复制到另外的 DataNode 中

- 数据可以毁坏
  1. 无论是写入时还是硬盘本身的问题，只要数据有问题（读取时通过校验码来检测），都可以通过其他的复制节点读取，同时还会再复制一份到健康的节点中

- <font color=red> NameNode不具备可靠性，需要做高可用</font>

## 部署过程

### 环境准备 
- 系统要求 ：CentOS7.
- 机器数量要求：物理机三台

### 物料包准备
1. ansible_r1813.tar.gz
> hdfs通过ansible进行自动化安装部署，因此需要提前部署好合适版本的ansible
> 主要工具 ansible/install.sh，安装执行程序（需要管理员权限）

2. hdfs-2.6.5.tar.gz 
> 主安装包，内含hdfs安装包以及自动化部署工具
> 主要工具展示
`tar -tvf hdfs-2.6.5.tar.gz `
```
...
-rwxrwxrwx 0/0             390 2018-03-05 19:07 hdfs/pkgs/clean_hdfs.sh
-rwxrwxrwx 0/0       199635269 2017-10-18 21:07 hdfs/pkgs/hadoop-2.6.5.tar.gz
-rwxrwxrwx 0/0            2950 2018-02-27 17:16 hdfs/pkgs/install_jdk_for_ansible.sh
-rwxrwxrwx 0/0       185515842 2017-10-18 21:07 hdfs/pkgs/jdk-8u144-linux-x64.tar.gz
...
-rwxrwxrwx 0/0            1100 2018-07-17 21:56 hdfs/scripts/core-site.xml.j2
-rwxrwxrwx 0/0            4289 2017-10-19 13:52 hdfs/scripts/hadoop-env.sh.j2
-rwxrwxrwx 0/0            4263 2018-07-17 21:56 hdfs/scripts/hdfs-site.xml.j2
-rwxrwxrwx 0/0             477 2018-03-01 13:22 hdfs/scripts/hdfs_clean.yml
...
-rwxrwxrwx 0/0             481 2018-03-05 19:30 hdfs/scripts/hdfs_hosts
-rwxrwxrwx 0/0           10657 2018-07-17 22:37 hdfs/scripts/hdfs_install.yml
-rwxrwxrwx 0/0            1060 2018-04-10 14:57 hdfs/scripts/vars.yml
```
> clean_hdfs.sh 部署安装失败时用于还原系统环境的工具
> hadoop-2.6.5.tar.gz hadoop官方安装包
> install_jdk_for_ansible.sh jdk检测安装程序。执行时会检测环境中是否有java环境，如果有则提示已存在，然后退出安装
> jdk-8u144-linux-x64.tar.gz jdk安装包
> *.j2配置文件的模板文件，用于根据实际环境生成特定的配置文件
> hdfs_clean.yml 清除环境中hdfs的文件
> hdfs_host ansible inventory文件，指定安装hdfs的文件以及安装了zookeeper的服务器列表和连接ansible连接服务器时所使用的参数
> hdfs_install.yml 主安装文件
> vars.yml 变量配置文件：安装包的路径变量，端口变量。以及指定使用路径安装还是裸磁盘安装
**<font color=red>注裸磁盘与路径不能同时为true</font>**

### 安装步骤
> 安装之前需要先修改好主机名，并配置到/etc/hosts文件
> 进入到各个主机并执行hostnamectl set-hostname hdfsnamenode[1/2/3]
> 并将主机名与ip的映射关系添加至/etc/hosts

#### 安装ansible 
- 将ansible安装包拷贝到管理节点/tmp目录下，解压缩并安装
  1. cd /tmp && tar -zxvf ansible_r1813.tar.gz
  2. cd /tmp/ansible && bash +x install.sh

#### 安装hdfs
1. 将hdfs-2.6.5.tar.gz 拷贝到管理节点/tmp目录下，解压缩至/data目录
> `cd /tmp && tar -zxvf hdfs-2.6.5.tar.gz -C /data`
2. 根据实际环境修改 /data/hdfs/scripts/hdfs_hosts文件
> namenode需要做高可用，因此需要设置两台，journal一般设置三台，datanode可根据实际需求设置合适的数量
3. 修改/data/hdfs/scripts/vars.yml 
> 需要根据实际环境选择裸磁盘安装还是路径安装

4. 查看环境中是否存在java环境，以及jps工具是否可用
> 如果都可用需要做一个软连接 `ln -s /usr/local/services/barad_java-1.0 $JAVA_HOME`否则部署工具会重新安装jdk可能会影响环境中其他正在运行的程序

5. 执行主安装程序，并需要显示的制定inventory文件，不然会使用默认的inventory文件
> `  cd /data/hdfs/scripts/ && ansible-playbook -i hdfs_hosts hdfs_install.yml | tee install_hdfs_output.txt `

6. 如果安装执行失败则先执行 ansible-playbook -i hdfs_hosts hdfs_clean.yml 进行环境清理，之后修复bug重新安装
> 如果装成功则需要对hdfs进行验证
> 调用jps命令查看是否有 JournalNode DataNode QuorumPeerMain ResourceManager这些java进程在运行，如果缺少了则需要排错
> 进入namenode 并执行` cd /usr/local/services/hadoop-2.6.5/bin/ && ./hdfs haadmin -getServiceState nn1  ` , 若其中一个为active一个为stanby则表明namenode安装成功
> 进入datanode 执行`hdfs dfsadmin -report` 如果有成功则表明datanode安装成功

### 命令行工具
- fsck: 检查文件的完整性
- start-balancer.sh: 重新平衡 HDFS
- hdfs dfs -copyFromLocal 从本地磁盘复制文件到 HDFS

>对namenode高可用测试可以先下掉一个namenode然后观察hdfs是否可以正常工作