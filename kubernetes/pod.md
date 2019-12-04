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