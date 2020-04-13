# flannel 工作原理及源码解析

[flannel.yaml](./yamls/cni/flannel.yaml)

```json
// cni-conf.json
{
  "name": "cbr0",
  "cniVersion": "0.3.1",
  "plugins": [
    {
      "type": "flannel",
      "delegate": {
        "hairpinMode": true,
        "isDefaultGateway": true
      }
    },
    {
      "type": "portmap",
      "capabilities": {
        "portMappings": true
      }
    }
  ]
}

// net-conf.json
{
  "Network": "10.244.0.0/16",
  "Backend": {
    "Type": "vxlan"
  }
}
```

[](https://www.cnblogs.com/rexcheny/p/10960233.html)


## flannel 工作流程

**[flannel 流程及流量转发流程分析](http://www.sel.zju.edu.cn/?p=690)**
[](https://ggaaooppeenngg.github.io/zh-CN/2017/09/21/flannel-%E7%BD%91%E7%BB%9C%E6%9E%B6%E6%9E%84/)

创建 node 时会配置相应的 spec.podCIDR 用于管理 pod 网段信息。每个 node.spec.podCIDR 不会冲突；

1. 节点初始化

问题点:

1. 如何选择宿主机之间的通信方式，ip、网卡等;

2. 初始化过程会对宿主机做什么改变。添加network interface、route、fdb、bridge 等;

3. 网段信息的分配、同步和租约;

4. 各类对象对应的接口/类型，及提供的方法;

5. 相关的几个配置文件;

6. 如何写入相应的路由信息

初始化做了以下工作:

1. 读取/设置参数值

2. 获取宿主机网卡信息保存至 `*backend.ExternalInterface` 结构体中

3. 创建子网管理器 `kubeSubnetManager`，包含 nodeController

4. 创建对应的 backend 及 network

5. watch lease 并调用对应的 event handler.

子网管理器的作用:

相关的注解:

```yaml
#kubectl get no node01 -oyaml | yq r -P - 'metadata.annotations'
flannel.alpha.coreos.com/backend-data: '{"VtepMAC":"a6:f4:cb:d7:bc:14"}' # backend 的附加信息
flannel.alpha.coreos.com/backend-type: vxlan # 使用 vxlan 作为 backend
flannel.alpha.coreos.com/kube-subnet-manager: "true" # 此注解表明使用 apiserver 管理租约信息
flannel.alpha.coreos.com/public-ip: 172.16.14.147
...
```

```shell
# 1. 分配子网(通过 subnet manager)

# 2. 使用相应的 backend 进行报文封装

# 3. 将封装的报文在 flanneld 之间传输```

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
