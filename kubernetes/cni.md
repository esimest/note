# Kubernetes Container Network Interface

## CNI 约束

- 所有 Pod 可以与其它 Pod 直接通信, 无需显式的 NAT.

- 所有 Node 可以与 Pod 直接通信, 无需显式的 NAT.

- Pod 可见的 IP 地址确为其它 Pod 与其通信时使用, 无需显式的转换.

学习网络插件需要关注的点:

- 如何实现数据包端到端的路径(Overlay/Underlay, 经过封包还是使用路由策略).

## Flannel

[](./flannel.md)

## Calico

## WavNet