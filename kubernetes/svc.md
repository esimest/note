# Kubernetes Service

## 作用

> 通过 label selector 将 pod 与 service 绑定(多对一), 从而实现了应用的一个统一访问入口
> 以及解决了 pod 重新调度导致 ip 变化不可控的问题


## 分类

### ClusterIP

> 提供了集群内部的服务发现以及负载均衡能力
> 内部 Pod 可以通过 ClusterIP 访问指定的应用

### NodePort

> 在所有 node 节点暴露指定 ip(s)，通过 node_ip + nodeport
> 可以访问对应的应用，可以实现集群外部访问

### Loadbalancer

> 将服务以公网 IP + port 形式暴露出来
> 有一个很大的缺点(浪费公网 IP)
