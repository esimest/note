# Kubernetes Server 安装配置

- [链接地址](https://github.com/kubernetes/kubernetes/releases/download/v1.14.3/kubernetes.tar.gz)

## 安装

  ```shell
  # 下载
  wget https://github.com/kubernetes/kubernetes/releases/download/v1.14.0/kubernetes.tar.gz
  # 解压缩，获取组件
  tar -zxvf kubernetes.tar.gz -C /data
  cd /data/kubernetes/server && tar -zxvf ./kubernetes-manifests.tar.gz
  cd /data/kubernetes/server && find ./ -perm 755 | xargs -i cp {} /usr/bin/
  ```

## 部署 apiserver

### 创建TLS Bootstrapping Token

```shell
 head -c 16 /dev/urandom | od -An -t x | tr -d ' '
f2c50331f07be89278acdaf341ff1ecc

vim /k8s/kubernetes/cfg/token.csv
f2c50331f07be89278acdaf341ff1ecc,kubelet-bootstrap,10001,"system:kubelet-bootstrap"
# 创建 apiserver 配置文件
vim /k8s/kubernetes/cfg/kube-apiserver
KUBE_APISERVER_OPTS="--logtostderr=true \
--v=4 \
--etcd-servers=https://172.16.14.151:2379,https://172.16.14.152:2379,https://172.16.14.157:2379 \
--bind-address=172.16.14.151 \
--secure-port=6443 \
--advertise-address=172.16.14.151 \
--allow-privileged=true \
--service-cluster-ip-range=10.254.0.0/16 \
--enable-admission-plugins=NamespaceLifecycle,LimitRanger,ServiceAccount,ResourceQuota,NodeRestriction \
--authorization-mode=RBAC,Node \
--enable-bootstrap-token-auth \
--token-auth-file=/k8s/kubernetes/cfg/token.csv \
--service-node-port-range=30000-50000 \
--tls-cert-file=/k8s/kubernetes/ssl/server.pem  \
--tls-private-key-file=/k8s/kubernetes/ssl/server-key.pem \
--client-ca-file=/k8s/kubernetes/ssl/ca.pem \
--service-account-key-file=/k8s/kubernetes/ssl/ca-key.pem \
--etcd-cafile=/k8s/etcd/ssl/ca.pem \
--etcd-certfile=/k8s/etcd/ssl/server.pem \
--etcd-keyfile=/k8s/etcd/ssl/server-key.pem"
# 创建 apiserver 启动配置
vim /usr/lib/systemd/system/kube-apiserver.service

[Unit]
Description=Kubernetes API Server
Documentation=https://github.com/kubernetes/kubernetes

[Service]
EnvironmentFile=-/k8s/kubernetes/cfg/kube-apiserver
ExecStart=/k8s/kubernetes/bin/kube-apiserver $KUBE_APISERVER_OPTS
Restart=on-failure

[Install]
WantedBy=multi-user.target

# 启动 apiserver
systemctl daemon-reload
systemctl enable kube-apiserver
systemctl start kube-apiserver
```

## 部署 kube-schduler

```shell
vim  /k8s/kubernetes/cfg/kube-scheduler
KUBE_SCHEDULER_OPTS="--logtostderr=true --v=4 --master=127.0.0.1:8080 --leader-elect"

# 创建启动配置文件
vim /usr/lib/systemd/system/kube-scheduler.service

[Unit]
Description=Kubernetes Scheduler
Documentation=https://github.com/kubernetes/kubernetes

[Service]
EnvironmentFile=-/k8s/kubernetes/cfg/kube-scheduler
ExecStart=/k8s/kubernetes/bin/kube-scheduler $KUBE_SCHEDULER_OPTS
Restart=on-failure

[Install]
WantedBy=multi-user.target
# 启动服务
```

## 部署 kube-controller-manager

```shell
vim /k8s/kubernetes/cfg/kube-controller-manager
KUBE_CONTROLLER_MANAGER_OPTS="--logtostderr=true \
--v=4 \
--master=127.0.0.1:8080 \
--leader-elect=true \
--address=127.0.0.1 \
--service-cluster-ip-range=10.254.0.0/16 \
--cluster-name=kubernetes \
--cluster-signing-cert-file=/k8s/kubernetes/ssl/ca.pem \
--cluster-signing-key-file=/k8s/kubernetes/ssl/ca-key.pem  \
--root-ca-file=/k8s/kubernetes/ssl/ca.pem \
--service-account-private-key-file=/k8s/kubernetes/ssl/ca-key.pem"
# 创建启动配置
vim /usr/lib/systemd/system/kube-controller-manager.service

[Unit]
Description=Kubernetes Controller Manager
Documentation=https://github.com/kubernetes/kubernetes

[Service]
EnvironmentFile=-/k8s/kubernetes/cfg/kube-controller-manager
ExecStart=/k8s/kubernetes/bin/kube-controller-manager $KUBE_CONTROLLER_MANAGER_OPTS
Restart=on-failure

[Install]
WantedBy=multi-user.target
# 启动服务
```

## 验证 kubernetes 服务

```shell
kubectl get nodes（有数据代表服务正常工作）
```

## Node 节点部署

## Docker-CE 安装

- 镜像仓库(mirrors.tuna.tsinghua.edu.cn清华大学镜像网站)

```shell
# 下载 docker yum 源
cd /etc/yum.repos.d && wget https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/centos/docker-ce.repo
# 修改 yum 源
vi docker-ce.repo
# 替换变量
1,$s/https:\/\/download.docker.com/https:\/\/mirrors.tuna.tsinghua.edu.cn\/docker-ce/g
```shell

- 配置阿里云镜像加速 /etc/docker/daemon.json

  - 如果没有 /etc/docker/daemon.json 文件,执行以下操作

    ```shell
    sudo mkdir -p /etc/docker
    sudo tee /etc/docker/daemon.json <<-'EOF'
    {
    "registry-mirrors": ["https://sx6i79oq.mirror.aliyuncs.com"]
    }
    EOF
    sudo systemctl daemon-reload
    sudo systemctl restart docker
    ```

  - 如果已经存在该文件，则将 `"registry-mirrors": ["https://sx6i79oq.mirror.aliyuncs.com"]` 添加至daemon.json
```

## 安装组件

1. 将 kube-proxy, kubelet 拷贝至 node 节点

2. 将证书拷贝至 node 节点

3. 创建 kubelet bootstrap kubeconfig 文件

```shell
vim /k8s/kubernetes/cfg/environment.sh
#!/bin/bash
#创建kubelet bootstrapping kubeconfig
BOOTSTRAP_TOKEN=f2c50331f07be89278acdaf341ff1ecc
KUBE_APISERVER="https://172.16.14.151:6443"
#设置集群参数
kubectl config set-cluster kubernetes \
  --certificate-authority=/k8s/kubernetes/ssl/ca.pem \
  --embed-certs=true \
  --server=${KUBE_APISERVER} \
  --kubeconfig=bootstrap.kubeconfig

#设置客户端认证参数
kubectl config set-credentials kubelet-bootstrap \
  --token=${BOOTSTRAP_TOKEN} \
  --kubeconfig=bootstrap.kubeconfig

# 设置上下文参数
kubectl config set-context default \
  --cluster=kubernetes \
  --user=kubelet-bootstrap \
  --kubeconfig=bootstrap.kubeconfig

# 设置默认上下文
kubectl config use-context default --kubeconfig=bootstrap.kubeconfig

#----------------------

# 创建kube-proxy kubeconfig文件

kubectl config set-cluster kubernetes \
  --certificate-authority=/k8s/kubernetes/ssl/ca.pem \
  --embed-certs=true \
  --server=${KUBE_APISERVER} \
  --kubeconfig=kube-proxy.kubeconfig

kubectl config set-credentials kube-proxy \
  --client-certificate=/k8s/kubernetes/ssl/kube-proxy.pem \
  --client-key=/k8s/kubernetes/ssl/kube-proxy-key.pem \
  --embed-certs=true \
  --kubeconfig=kube-proxy.kubeconfig

kubectl config set-context default \
  --cluster=kubernetes \
  --user=kube-proxy \
  --kubeconfig=kube-proxy.kubeconfig

kubectl config use-context default --kubeconfig=kube-proxy.kubeconfig

# 执行 environment.sh
sh environment.sh

会生成 bootstrap.kubeconfig kube-proxy.kubeconfig

# 创建 kubelet 参数配置模板文件
vim /k8s/kubernetes/cfg/kubelet.config
kind: KubeletConfiguration
apiVersion: kubelet.config.k8s.io/v1beta1
address: 10.2.8.65
port: 10250
readOnlyPort: 10255
cgroupDriver: cgroupfs
clusterDNS: ["10.254.0.10"]
clusterDomain: cluster.local.
failSwapOn: false
authentication:
  anonymous:
    enabled: true

# 创建kubelet配置文件
vim /k8s/kubernetes/cfg/kubelet

KUBELET_OPTS="--logtostderr=true \
--v=4 \
--hostname-override=10.2.8.65 \
--kubeconfig=/k8s/kubernetes/cfg/kubelet.kubeconfig \
--bootstrap-kubeconfig=/k8s/kubernetes/cfg/bootstrap.kubeconfig \
--config=/k8s/kubernetes/cfg/kubelet.config \
--cert-dir=/k8s/kubernetes/ssl \
--pod-infra-container-image=registry.cn-hangzhou.aliyuncs.com/google-containers/pause-amd64:3.0"

# 创建 kubelet 启动配置文件
vim /usr/lib/systemd/system/kubelet.service

[Unit]
Description=Kubernetes Kubelet
After=docker.service
Requires=docker.service

[Service]
EnvironmentFile=/k8s/kubernetes/cfg/kubelet
ExecStart=/k8s/kubernetes/bin/kubelet $KUBELET_OPTS
Restart=on-failure
KillMode=process

[Install]
WantedBy=multi-user.target

# 将kubelet-bootstrap用户绑定到系统集群角色

kubectl create clusterrolebinding kubelet-bootstrap \
  --clusterrole=system:node-bootstrapper \
  --user=kubelet-bootstrap

# 启动服务
systemctl daemon-reload systemctl enable kubelet systemctl start kubelet
```


## 部署 kube-proxy

```shell
# 创建配置文件
vim /k8s/kubernetes/cfg/kube-proxy
KUBE_PROXY_OPTS="--logtostderr=true \
--v=4 \
--hostname-override=172.16.14.151 \
--cluster-cidr=10.254.0.0/16 \
--kubeconfig=/k8s/kubernetes/cfg/kube-proxy.kubeconfig"

# 创建 启动配置文件
vim /usr/lib/systemd/system/kube-proxy.service

[Unit]
Description=Kubernetes Proxy
After=network.target

[Service]
EnvironmentFile=-/k8s/kubernetes/cfg/kube-proxy
ExecStart=/k8s/kubernetes/bin/kube-proxy $KUBE_PROXY_OPTS
Restart=on-failure

[Install]
WantedBy=multi-user.target

# 启动服务
systemctl daemon-reload systemctl enable kube-proxy systemctl start kube-proxy

# 查看集群状态
 kubectl get nodes
```

## 部署 flaeeld 网络

```shell
# 注册网段
/k8s/etcd/bin/etcdctl --ca-file=/k8s/etcd/ssl/ca.pem --cert-file=/k8s/etcd/ssl/server.pem --key-file=/k8s/etcd/ssl/server-key.pem --endpoints="https://172.16.14.151:2379,https://172.16.14.152:2379,https://172.16.14.157:2379"  set /k8s/network/config  '{ "Network": "10.254.0.0/16", "Backend": {"Type": "vxlan"}}'

# 下载 flannel
wget https://github.com/coreos/flannel/releases/download/v0.11.0/flanneld-amd64

# 解压后将二进制文件前一直 /usr/local/

# 配置 flanneld
vim /k8s/kubernetes/cfg/flanneld
FLANNEL_OPTIONS="--etcd-endpoints=https://172.16.14.151:2379,https://172.16.14.152:2379,https://172.16.14.157:2379 -etcd-cafile=/k8s/etcd/ssl/ca.pem -etcd-certfile=/k8s/etcd/ssl/server.pem -etcd-keyfile=/k8s/etcd/ssl/server-key.pem -etcd-prefix=/k8s/network"

# 创建启动配置文件
vim /usr/lib/systemd/system/flanneld.service
[Unit]
Description=Flanneld overlay address etcd agent
After=network-online.target network.target
Before=docker.service

[Service]
Type=notify
EnvironmentFile=/k8s/kubernetes/cfg/flanneld
ExecStart=/k8s/kubernetes/bin/flanneld --ip-masq $FLANNEL_OPTIONS
ExecStartPost=/k8s/kubernetes/bin/mk-docker-opts.sh -k DOCKER_NETWORK_OPTIONS -d /run/flannel/subnet.env
Restart=on-failure

[Install]
WantedBy=multi-user.target

# 配置Docker启动指定子网 修改EnvironmentFile=/run/flannel/subnet.env，ExecStart=/usr/bin/dockerd $DOCKER_NETWORK_OPTIONS即可
vim /usr/lib/systemd/system/docker.service
[Unit]
Description=Docker Application Container Engine
Documentation=https://docs.docker.com
After=network-online.target firewalld.service
Wants=network-online.target

[Service]
Type=notify
EnvironmentFile=/run/flannel/subnet.env
ExecStart=/usr/bin/dockerd $DOCKER_NETWORK_OPTIONS
ExecReload=/bin/kill -s HUP $MAINPID
LimitNOFILE=infinity
LimitNPROC=infinity
LimitCORE=infinity
TimeoutStartSec=0
Delegate=yes
KillMode=process
Restart=on-failure
StartLimitBurst=3
StartLimitInterval=60s

[Install]
WantedBy=multi-user.target

# 重启服务
systemctl daemon-reload
systemctl stop docker
systemctl start flanneld
systemctl enable flanneld
systemctl start docker
systemctl restart kubelet
systemctl restart kube-proxy

# 验证服务
cat /run/flannel/subnet.env
```


