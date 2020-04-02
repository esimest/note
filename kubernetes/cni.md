# Kubernetes Container Network Interface

## CNI 约束

- 所有 Pod 可以与其它 Pod 直接通信, 无需显式的 NAT.

- 所有 Node 可以与 Pod 直接通信, 无需显式的 NAT.

- Pod 可见的 IP 地址确为其它 Pod 与其通信时使用, 无需显式的抓换.

学习网络插件需要关注的点:

- 如何实现数据包端到端的路径(Overlay/Underlay, 经过封包还是使用路由策略).

## Flannel

[](https://www.cnblogs.com/rexcheny/p/10960233.html)

[](https://ggaaooppeenngg.github.io/zh-CN/2017/09/21/flannel-%E7%BD%91%E7%BB%9C%E6%9E%B6%E6%9E%84/)

flannel 做两件事:

1. 分配子网(通过 subnet manager)

2. 使用相应的 backend 进行报文封装

3. 将封装的报文在 flanneld 之间传输

### vxlan backend 数据包流向

- vxlan:
  [](https://support.huawei.com/enterprise/zh/doc/EDOC1100023543?section=j016)

### Flannel 运行参数

- `--public-ip=""`
   > IP accessible by other nodes for inter-host communication. Defaults to the IP of the interface being used for communication.
- `--etcd-endpoints=http://127.0.0.1:4001`
   > a comma-delimited list of etcd endpoints.
- `--etcd-prefix=/coreos.com/network`
   > etcd prefix.(etcd 存储数据 key 的前缀)
- `--etcd-keyfile=""`
   > SSL key file used to secure etcd communication.
- `--etcd-certfile=""`
   > SSL certification file used to secure etcd communication.
- `--etcd-cafile=""`
   > SSL Certificate Authority file used to secure etcd communication.
- `--kube-subnet-mgr`
   > Contact the Kubernetes API for subnet assignment instead of etcd.
   > 设置此项使用 kubernetes 接口分配 subnet 取代 etcd.
- `--iface=""`
   > interface to use (IP or name) for inter-host communication. Defaults to the interface for the default route on the machine. This can be - specified multiple times to check each option in order. Returns the first match found.
- `--iface-regex=""`
   > regex expression to match the first interface to use (IP or name) for inter-host communication. If unspecified, will default to the - interface for the default route on the machine. This can be specified multiple times to check each regex in order. Returns the first match found. This - option is superseded by the iface option and will only be used if nothing matches any option specified in the iface options.
- `--iptables-resync=5`
   > resync period for iptables rules, in seconds. Defaults to 5 seconds, if you see a large amount of contention for the iptables lock - increasing this will probably help.
- `--subnet-file=/run/flannel/subnet.env`
   > filename where env variables (subnet and MTU values) will be written to.
- `--net-config-path=/etc/kube-flannel/net-conf.json`
   > path to the network configuration file to use
- `--subnet-lease-renew-margin=60`
   > subnet lease renewal margin, in minutes.
- `--ip-masq=false`
   > setup IP masquerade for traffic destined for outside the flannel network. Flannel assumes that the default policy is ACCEPT in the NAT - POSTROUTING chain.
- `-v=0`
   > log level for V logs. Set to 1 to see messages related to data path.
- `--healthz-ip="0.0.0.0"`
   > The IP address for healthz server to listen (default "0.0.0.0")
- `--healthz-port=0`
   > The port for healthz server to listen(0 to disable)
- `--version`
   > print version and exit

## Calico

## WavNet