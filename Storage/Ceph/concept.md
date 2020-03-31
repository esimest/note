# Ceph 相关概念

## RADOS(reliable, autonomous, distributed object sotre)

> Ceph 的 RADOS 具体体现在哪里，又是通过什么来对这些特性进行支持的。

rados = mon(集群元数据管理) + osd(数据存储支持)

## ceph 集群的组成进程及其作用

> 通过起作用能够了解 ceph 客户端调用接口的执行过程

1. mon
   > mon 集群元数据的管理、维护者。类似于 k8s 的 etcd。
   > 用于实现分布式应用的数据一致性。主要维护了几个 `map`。

2. osd

3. mgr

4. mds

## ceph 数据存储涉及到的几个概念

> 通过这些概念，可以将存储的逻辑概念与实际的物理设施相对应，提升对集群的理解。

1. pool

2. image

3. object

4. placement gropu(obj 和 osd 的中间层)

5. osd, 主 osd, 次 osd

## 具体概念实现

1. ceph 通过主 osd 进行其它副本位置的确定及复制. 详见 [复制](http://docs.ceph.org.cn/architecture/)

2. ceph 通过 CRUSH 算法确定对象的存储位置. 详见[胖哥大话 ceph](http://www.xuxiaopang.com/2016/11/08/easy-ceph-CRUSH/)

3. 当某新增 osd 或 osd 故障时，ceph 如何维护副本数，且会不会使之前的数据存储位置变化。
