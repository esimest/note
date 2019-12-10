# Pod 笔记

## Pod 是什么

官方介绍:

A Pod (as in a pod of whales or pea pod) is a group of one or more containers (such as Docker containers), with shared storage/network, and a specification for how to run the containers. A Pod’s contents are always co-located and co-scheduled, and run in a shared context. A Pod models an application-specific “logical host” - it contains one or more application containers which are relatively tightly coupled — in a pre-container world, being executed on the same physical or virtual machine would mean being executed on the same logical host.

翻译:

Pod 是由一个或多个容器构成的容器组，这些容器共享存储/网络空间(或则资源), 和使用相同的容器运行策略(故障恢复、镜像拉取原则等). 一个 Pod
中的容器都是一同落地与调度的，并且共享上下文环境. Pod 相对其中的容器就像是特定应用的逻辑主机 - Pod 中包含容器都是有紧密联系的 - 对于每个独立容器而言，
运行在同一个物理/虚拟机上意味着这些容器运行在同一个逻辑主机上.


## 使用 Pod 而不是 Container 的原因

- 解耦具体容器实现

- 网络、IPC、存储资源共享(Pod 存活资源就不释放)
   > 可以通过 localhost:port 访问内部其它容器
   > 可以使用相同存储卷

- 使用相同的容器运行策略(故障恢复、镜像拉取、探针等)

## Kubernetes 创建 Deployment 流程

1. 客户端向 api-server 发送创建 deploy 的请求
2. 通过认证后，把 pod 数据存储到 etcd，然后创建 deploy 资源并初始化
3. 控制器管理器 watch api-server, 发现新的 deploy 将其加入工作队列中。
   发现没有关联资源的 pod 和 rs。创建 rs 的控制器然后通过 rs 的管理器
   创建 pod 的管理器
4. 所有的管理器都 OK 后，将资源更新存储到 etcd
5. scheduler watch api-server, 发现没有调度的 pod，经过主机过滤打分规则，
   将 pod 绑定到合适的主机。
6. kubelet 每隔一段时间通过 nodename 向 api-server 同步对应 node 所需要运行
   的 pod 清单。通过内部缓存和清单比较，对 pod 进行增减
7. kubelet 通过 CRI 调用具体容器引擎启动容器
8. 将本节点的 pod 信息同步到 etcd