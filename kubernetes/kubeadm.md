# Kubeadm

## 初始化设置

1. yum 源配置

2. hostname 设置

3. 内核参数配置
   > `modprobe: FATAL: Module br_netfilter not found.` 问题.
   > 安装 br_netfilter 模块 `yum install -y bridge-utils.x86_64` 后重启.

4. 清空 iptables 规则, 关闭 firewalld, selinux

5. 安装 kubeadm, kubelet, kubectl, docker
   > 需要配置 kubelet 的 cgroup 驱动与 docker 驱动一致(默认为 cgroupfs).

## haproxy(nginx) + keepalived

### 安装

`ansible master -m yum -a'name=haproxy state=installed'`
`ansible master -m yum -a'name=keepalived state=installed'`

### 配置

keepalived:

```shell
! Configuration File for keepalived

global_defs {
}

vrrp_instance VI_1 {
    state MASTER          # (BACKUP)
    interface eth0        # 根据实际环境填写
    virtual_router_id 51  # 多个集群时需要修改
    priority 100          # different
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 1111
    }
    virtual_ipaddress {
        ${VIP}
    }
}
```

haproxy:

```shell
global
    daemon
    stats socket /var/lib/haproxy/stats
    maxconn 4000

defaults
    log global
    mode http
    option dontlognull
    timeout connect 5000ms
    timeout client 600000ms
    timeout server 600000ms

listen stats
   bind :9090
   mode http
   balance
   stats enable
   stats refresh 10s
   stats uri /haproxy_stats
   stats auth admin:admin123
   stats admin if TRUE

frontend kube-apiserver-https
   mode tcp
   bind ${vip}:6443
   default_backend kube-apiserver-backend

backend kube-apiserver-backend
    mode tcp
    balance roundrobin
    stick-table type ip size 200k expire 30m
    stick on src
        server ${server_name} ${server_ip}:6443 check
        server ${server_name} ${server_ip}:6443 check
        server ${server_name} ${server_ip}:6443 check
```

nginx:

```nginx
stream {
    upstream kube-apiserver {
       server ${server1}:6443;
       server ${server2}:6443;
       server ${server3}:6443;
    }
    server {
       listen 6443;
       proxy_pass kube-apiserver;
    }
}
```

## etcd 高可用

kubeadm 有两种集群高可用 etcd 部署方式, 分别为: 堆叠 etcd, 外部 etcd.

### 堆叠 etcd

![stacked etcd ha](./iamges/ha_stacked.png)

Stacked 高可用方式将 etcd 部署在 kubernetes 控制平面上, 静态 Pod 的方式运行 etcd 组件.

每个控制平面上都会部署 apiserver, scheduler, controller-manger 的实例. apiserver 通过负载均衡器暴露给集群中的 worker 节点.
每个控制平面上的 etcd, scheduler, controller-manager 都直接与该平面上的 apiserver 通信.


### 外部 etcd

![external etcd ha](./images/ha_external.png)

## kubeadm init

**需要先将 haproxy 关闭, 释放 6443 端口**

```shell
kubeadm init --log-file=kubeadm.log \
--image-repository=registry.aliyuncs.com/google_containers \
--apiserver-advertise-address=172.16.14.157 \
--control-plane-endpoint=172.16.14.146:6443 \
--pod-network-cidr=10.244.0.0/16 \
--service-cidr=192.168.200.1/24 --upload-certs=true
```

## 安装网络插件

![network-plugins](https://kubernetes.io/docs/concepts/cluster-administration/networking/)

安装完成之后 node 节为 Ready 状态.

## 重启 haproxy

## Problems

### static pod

kubelet 加载 /etc/kubernetes/manifests/ 目录下文件的方式类似与 kubectl apply -f.
**因此当目录中存在多个文件声明同一个资源时会出现后面的文件的配置覆盖前面文件的配置的情况.**

### nginx 监听 vip 失败

nginx: [emerg] bind() to ${vip}:6443 failed (99: Cannot assign requested address);
需要设置: net.ipv4.ip_nonlocal_bind = 1

### haproxy 无法启动, 端口被占用

/etc/kubernetes/manifests/kube-apiserver.yaml 的 command 中添加一项 --bind-address=${host_ip}