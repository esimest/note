# Kubeadm


## Step

### 初始化设置

1. yum 源配置

2. hostname 设置

3. 内核参数配置
   > 安装 br_netfilter 模块 `yum install -y bridge-utils.x86_64`

4. 清空 iptables 规则, 关闭 firewalld, selinux

5. 安装 kubeadm, kubelet, kubectl, docker
   > 需要配置 kubelet 的 cgroup 驱动与 docker 驱动一致(默认为 cgroupfs).

### kubeadm init

```shell
kubeadm init --image-repository=registry.aliyuncs.com/google_containers \
--control-plane-endpoint=172.16.14.146:6443 \
--pod-network-cidr=10.244.0.0/16 \
--service-cidr=192.168.200.1/24 --upload-certs=true
```

## 集群高可用

kubeadm 有两种集群高可用部署方式, 分别为: 堆叠 etcd, 外部 etcd.

### 堆叠 etcd

![stacked etcd ha](./iamges/ha_stacked.png)

Stacked 高可用方式将 etcd 部署在 kubernetes 控制平面上, 静态 Pod 的方式运行 etcd 组件.

每个控制平面上都会部署 apiserver, scheduler, controller-manger 的实例. apiserver 通过负载均衡器暴露给集群中的 worker 节点.
每个控制平面上的 etcd, scheduler, controller-manager 都直接与该平面上的 apiserver 通信.


### 外部 etcd

![external etcd ha](./images/ha_external.png)
