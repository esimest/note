# Pod 笔记

## Pod 是什么

官方介绍:

      A Pod (as in a pod of whales or pea pod) is a group of one or more containers
    (such as Docker containers), with shared storage/network, and a specification for
    how to run the containers. A Pod’s contents are always co-located and co-scheduled,
    and run in a shared context. A Pod models an application-specific “logical host” - it
    contains one or more application containers which are relatively tightly coupled — in
    a pre-container world, being executed on the same physical or virtual machine would mean
    being executed on the same logical host.

翻译:

      Pod 是由一个或多个容器构成的容器组，这些容器共享存储/网络空间(或则资源),
    和使用相同的容器运行策略(故障恢复、镜像拉取原则等). 一个 Pod 中的容器都是一同落地与调度的,
    并且共享上下文环境. Pod 相对其中的容器就像是特定应用的逻辑主机 - Pod 中包含的容器都是
    有紧密联系的 - 对于每个独立容器而言，运行在同一个物理/虚拟机上意味着这些容器运行在同一个逻辑主机上.

## Pod 而不是 Container

### 容器的单进程模型

Linux 容器的“单进程”模型，指的是容器的生命周期等同于 PID=1 的进程（容器应用进程）的生命周期.

### Container 的不足

超亲密关系:

1. 容器之间会发生直接的文件交换

2. 容器之间使用 localhost 或 Socket 文件进行本地通信.

3. 容器之间会发生频繁的 RPC 调用(使用 pod 来减少开销)

4. 容器之间需要共享名称空间.

> 当有多个容器具备超亲密度时, 他们需要相互共享资源以及一同调度.
> 如果以容器为基本调度单元, 会面临多个容器之间协同调度的问题.
> 使用 Pod 可以从根本上解决此类问题, 因为 Pod 中的容器都是一同调度的.
> 即: 只有当计算节点满足 Pod 内所有容器的运行条件时, 才会将容器一同调度至计算节点.

### Pod 解决的问题

1. 网络共享
   > 通过 Infra Container(镜像为: k8s.gcr.io/pause, 大小为 100-200k) 解决.
   > 每一个 Pod 都会启动一个 Infra Container 容器(pause 状态), Pod 内所有容器
   > 都与 Infra Container 共享名称空间, 从而达到所有的容器可以通过 localhost
   > 进行交互.
   > Pod 的生命周期与 Infra Container 生命周期一致.

2. 存储卷共享

### SideCar (边车) 设计模式

通过在 Pod 内定义专门的容器, 来执行对主容器需要的辅助工作.

优点: 解耦, 复用

1. 日志收集
   > 业务容器将日志写入 Volume 里,
   > 日志容器将日志从 Volume 转存至远端存储.
  ![日志 sidecar](./images/log_sidecar.png)

2. 代理容器
   > 代理容器对业务容器屏蔽被代理的服务集群
   > 简化业务代码的实现逻辑
   ![代理 sidecar](./images/proxy_sidecar.png)

3. 适配器容器
   > 适配器容器将业务容器暴露出的接口转换为另一种格式
   ![适配器 sidecar](./images/adapter_sidecar.png)

## Kubernetes 创建 Deployment 流程

1. 客户端向 api-server 发送创建 deploy 的请求

2. 通过认证后，把 pod 数据存储到 etcd，然后创建 deploy 资源并初始化

3. 控制器管理器 watch api-server, 发现新的 deploy 将其加入工作队列中。
   发现没有关联资源的 pod 和 rs。创建 rs 的控制器然后通过 rs 的管理器
   创建 pod 的管理器

4. 所有的 Controller 都 OK 后，将资源更新存储到 etcd

5. scheduler watch api-server, 发现没有调度的 pod，经过主机过滤打分规则，
   将 pod 绑定到合适的主机

6. kubelet 每隔一段时间通过 nodename 向 api-server 同步对应 node 所需要运行
   的 pod 清单。通过内部缓存和清单比较，对 pod 进行增减

7. kubelet 通过 CRI 调用具体容器引擎启动容器

8. 将本节点的 pod 信息同步到 etcd
