# 二进制部署 Kuberntes

## ansible

> 安装 ansible, 并配置 hosts 和 修改 host_key_check

 `yum install -y epel-release && yum install -y ansible`

- 生成 ssh 密钥
`ssh-key-gen`

- 建立 ssh 信任
`ssh-copy-id ${dest_ip}`

## Environment init

> 修改环境配置(init_env.sh)

`ansible all -m script -a'${path}/init_env.sh`

## 创建安装目录(master)

```shell
# etcd 目录
ansible etcd -m shell -a'mkdir /data/etcd/{bin,conf,cfssl} -p'

# kubernetes 目录
ansible all -m shell -a'mkdir /data/kubernetes/{bin,conf,cfssl} -p'

# cfssl 证书生成目录
ansible all -m shell -a'mkdir -p /data/cfssl'

# 物料存放目录
mkdir -p /data/pkg
```

## 获取物料

```shell
# cfssl 物料(master)
wget https://pkg.cfssl.org/R1.2/cfssl_linux-amd64
wget https://pkg.cfssl.org/R1.2/cfssljson_linux-amd64
wget https://pkg.cfssl.org/R1.2/cfssl-certinfo_linux-amd64

# etcd 物料
wget https://github.com/etcd-io/etcd/releases/download/v3.3.10/etcd-v3.3.10-linux-amd64.tar.gz

# flannel 物料
wget https://github.com/coreos/flannel/releases/download/v0.10.0/flannel-v0.10.0-linux-amd64.tar.gz

# kubernetes 物料
wget https://github.com/kubernetes/kubernetes/releases/download/v1.14.0/kubernetes.tar.gz
```

## Docker-CE 安装

- 镜像仓库(mirrors.tuna.tsinghua.edu.cn清华大学镜像网站)

```shell
# 下载 docker yum 源
cd /etc/yum.repos.d && wget https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/centos/docker-ce.repo
# 修改 yum 源
vi docker-ce.repo
# 替换变量
sed -i 's/https:\/\/download.docker.com/https:\/\/mirrors.tuna.tsinghua.edu.cn\/docker-ce/g' /etc/yum.repos.d/docker-ce.repo

# 分发给所有节点
ansible all -m copy -a 'src=/etc/yum.repos.d/docker-ce.repo dest=/etc/yum.repos.d/'

# 安装 docker-ce
ansible all -m yum -a'name=docker-ce state=present'

# 配置阿里云镜像加速 /etc/docker/daemon.json(master)

## 如果没有 /etc/docker/daemon.json 文件,执行以下操作
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
"registry-mirrors": ["https://sx6i79oq.mirror.aliyuncs.com"]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker

## 如果已经存在该文件，则将 `"registry-mirrors": ["https://sx6i79oq.mirror.aliyuncs.com"]` 添加至daemon.json

# 分发 /etc/docker/daemon.json
ansible all -m file -a'path=/etc/docker state=directory'
ansible all -m copy -a'src=/etc/docker/daemon.json dest=/etc/docker/daemon.json'

# 设置 Docker 参数
tee /etc/sysctl.d/kubernetes.conf << EOF > /dev/null
net.ipv4.ip_forward = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF

# 将 /etc/sysctl.d/kubernetes.conf 分发至所有节点
ansible node -m copy -a'src=/etc/sysctl.d/kubernetes.conf dest=/etc/sysctl.d/kubernetes.conf'
ansible node -m shell -a'sysctl -p /etc/sysctl.d/kubernetes.conf'
```

## master 安装配置 CFSSL

```shell
# 安装 cfssl
chmod +x cfssl_linux-amd64 cfssljson_linux-amd64 cfssl-certinfo_linux-amd64
mv cfssl_linux-amd64 /usr/local/bin/cfssl
mv cfssljson_linux-amd64 /usr/local/bin/cfssljson
mv cfssl-certinfo_linux-amd64 /usr/bin/cfssl-certinfo

cd /data/cfssl
# CA 配置
tee ca-csr.json << EOF
{
    "CN": "My CA",
    "key": {
        "algo": "rsa",
        "size": 2048
    },
    "names": [
        {
            "C": "CN",
            "L": "Shenzhen",
            "ST": "Shenzhen"
        }
    ]
}
EOF

tee ca-config.json << EOF
{
  "signing": {
    "default": {
      "expiry": "87600h"
    },
    "profiles": {
      "etcd": {
         "expiry": "87600h",
         "usages": [
            "signing",
            "key encipherment",
            "server auth",
            "client auth"
        ]
      },
       "kubernetes": {
         "expiry": "87600h",
         "usages": [
            "signing",
            "key encipherment",
            "server auth",
            "client auth"
        ]
      }
    }
  }
}
EOF

# ETCD 证书请求
tee etcd-csr.json << EOF
{
    "CN": "etcd",
    "hosts": [
    "172.16.111.70",
    "172.16.111.71",
    "172.16.111.72"
    ],
    "key": {
        "algo": "rsa",
        "size": 2048
    },
    "names": [
        {
            "C": "CN",
            "L": "Shenzhen",
            "ST": "Shenzhen"
        }
    ]
}
EOF

# Kube-apiserver 证书请求
tee kube-apiserver-csr.json << EOF
{
    "CN": "kubernetes",
    "hosts": [
      "10.0.0.1",
      "127.0.0.1",
      "172.16.111.70",
      "kubernetes",
      "kubernetes.default",
      "kubernetes.default.svc",
      "kubernetes.default.svc.cluster",
      "kubernetes.default.svc.cluster.local"
    ],
    "key": {
        "algo": "rsa",
        "size": 2048
    },
    "names": [
        {
            "C": "CN",
            "L": "Shenzhen",
            "ST": "Shenzhen",
            "O": "kubernetes",
            "OU": "System"
        }
    ]
}
EOF

# kube-proxy 证书请求
tee kube-proxy-csr.json << EOF
{
  "CN": "system:kube-proxy",
  "hosts": [],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "L": "Shenzhen",
      "ST": "Shenzhen",
      "O": "kubernetes",
      "OU": "System"
    }
  ]
}
EOF
# 创建 CA
cfssl gencert -initca ca-csr.json | cfssljson -bare ca -
# 创建 ETCD 证书
cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=etcd etcd-csr.json | cfssljson -bare etcd

# 创建 Kube-apiserver 证书
cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=kubernetes kube-apiserver-csr.json | cfssljson -bare kube-apiserver

# 创建 Kube-proxy 证书
cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=kubernetes kube-proxy-csr.json | cfssljson -bare kube-proxy

```

## 安装 etcd

```shell
# 解压安装 etcd
cd /data/pkg
tar -xvf etcd-v3.3.10-linux-amd64.tar.gz
cd etcd-v3.3.10-linux-amd64/
cp etcd etcdctl /data/etcd/bin/

# 创建 etcd 配置文件
## 172.16.111.70
cd /data/etcd/conf/ && tee etcd << EOF
#[Member]
ETCD_NAME="etcd01"
ETCD_DATA_DIR="/var/lib/etcd/default.etcd"
ETCD_LISTEN_PEER_URLS="https://172.16.111.70:2380"
ETCD_LISTEN_CLIENT_URLS="https://172.16.111.70:2379"

#[Clustering]
ETCD_INITIAL_ADVERTISE_PEER_URLS="https://172.16.111.70:2380"
ETCD_ADVERTISE_CLIENT_URLS="https://172.16.111.70:2379"
ETCD_INITIAL_CLUSTER="etcd01=https://172.16.111.70:2380,etcd02=https://172.16.111.71:2380,etcd03=https://172.16.111.72:2380"
ETCD_INITIAL_CLUSTER_TOKEN="etcd-cluster"
ETCD_INITIAL_CLUSTER_STATE="new"
EOF
## 172.16.111.71
cd /data/etcd/conf/ && tee etcd << EOF
#[Member]
ETCD_NAME="etcd02"
ETCD_DATA_DIR="/var/lib/etcd/default.etcd"
ETCD_LISTEN_PEER_URLS="https://172.16.111.71:2380"
ETCD_LISTEN_CLIENT_URLS="https://172.16.111.71:2379"

#[Clustering]
ETCD_INITIAL_ADVERTISE_PEER_URLS="https://172.16.111.71:2380"
ETCD_ADVERTISE_CLIENT_URLS="https://172.16.111.71:2379"
ETCD_INITIAL_CLUSTER="etcd01=https://172.16.111.70:2380,etcd02=https://172.16.111.71:2380,etcd03=https://172.16.111.72:2380"
ETCD_INITIAL_CLUSTER_TOKEN="etcd-cluster"
ETCD_INITIAL_CLUSTER_STATE="new"
EOF
## 172.16.111.72
cd /data/etcd/conf/ && tee etcd << EOF
#[Member]
ETCD_NAME="etcd03"
ETCD_DATA_DIR="/var/lib/etcd/default.etcd"
ETCD_LISTEN_PEER_URLS="https://172.16.111.72:2380"
ETCD_LISTEN_CLIENT_URLS="https://172.16.111.72:2379"

#[Clustering]
ETCD_INITIAL_ADVERTISE_PEER_URLS="https://172.16.111.72:2380"
ETCD_ADVERTISE_CLIENT_URLS="https://172.16.111.72:2379"
ETCD_INITIAL_CLUSTER="etcd01=https://172.16.111.70:2380,etcd02=https://172.16.111.71:2380,etcd03=https://172.16.111.72:2380"
ETCD_INITIAL_CLUSTER_TOKEN="etcd-cluster"
ETCD_INITIAL_CLUSTER_STATE="new"
EOF

## 创建 ETCD 启动文件(不能用 << EOF 因为变量会被替换)
vim /usr/lib/systemd/system/ && tee etcd.service
[Unit]
Description=Etcd etcd
After=network.target
After=network-online.target
Wants=network-online.target

[Service]
Type=notify
EnvironmentFile=/data/etcd/conf/etcd
ExecStart=/data/etcd/bin/etcd \
--name=${ETCD_NAME} \
--data-dir=${ETCD_DATA_DIR} \
--listen-peer-urls=${ETCD_LISTEN_PEER_URLS} \
--listen-client-urls=${ETCD_LISTEN_CLIENT_URLS},http://127.0.0.1:2379 \
--advertise-client-urls=${ETCD_ADVERTISE_CLIENT_URLS} \
--initial-advertise-peer-urls=${ETCD_INITIAL_ADVERTISE_PEER_URLS} \
--initial-cluster=${ETCD_INITIAL_CLUSTER} \
--initial-cluster-token=${ETCD_INITIAL_CLUSTER_TOKEN} \
--initial-cluster-state=new \
--cert-file=/data/etcd/cfssl/etcd.pem \
--key-file=/data/etcd/cfssl/etcd-key.pem \
--peer-cert-file=/data/etcd/cfssl/etcd.pem \
--peer-key-file=/data/etcd/cfssl/etcd-key.pem \
--trusted-ca-file=/data/etcd/cfssl/ca.pem \
--peer-trusted-ca-file=/data/etcd/cfssl/ca.pem
Restart=on-failure
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target

# 拷贝 etcd 相关证书至 /data/etcd/cfssl
cd /data/cfssl && cp ca*pem etcd*pem /data/etcd/cfssl

# 将启动文件分发至其他 etcd 节点
ansible etcd -m copy -a'src=/usr/lib/systemd/system/etcd.service dest=/usr/lib/systemd/system/etcd.service'

# 将 /data/etcd 分发至其他 etcd 节点
ansible etcd -m copy -a'src=/data/etcd/ dest=/data/etcd'

# etcd 证书分发至所有节点
ansible all -m copy -a 'src=/data/etcd/cfssl/ dest=/data/etcd/cfssl'

# 添加执行权限
ansible all -m shell -a'chmod +x /data/etcd/bin/*'

# 启动 etcd
ansible etcd -m shell -a'systemctl daemon-reload && systemctl enable etcd && systemctl start etcd'

# 将 /data/etcd/bin 加入 PATH
# 验证 etcd
etcdctl \
--ca-file=/data/etcd/cfssl/ca.pem \
--cert-file=/data/etcd/cfssl/etcd.pem \
--key-file=/data/etcd/cfssl/etcd-key.pem \
--endpoints="https://172.16.111.70:2379,\
https://172.16.111.71:2379,\
https://172.16.111.72:2379" cluster-health

# 为 etcdctl 添加别名
alias etcdctl='etcdctl \
--ca-file=/data/etcd/cfssl/ca.pem \
--cert-file=/data/etcd/cfssl/etcd.pem \
--key-file=/data/etcd/cfssl/etcd-key.pem \
--endpoints="https://172.16.111.70:2379,\
https://172.16.111.71:2379,\
https://172.16.111.72:2379"'
```

## 部署 Flannel

```shell
# 将 pod 网段信息写入 etcd
etcdctl set /coreos.com/network/config  '{ "Network": "172.18.0.0/16", "Backend": {"Type": "vxlan"}}'

# 解压 flannel
cd /data/pkg && tar -xvf flannel-v0.10.0-linux-amd64.tar.gz
mv flanneld mk-docker-opts.sh /data/kubernetes/bin/

# 配置 flanneld
tee /data/kubernetes/conf/flanneld << EOF
FLANNEL_OPTIONS="--etcd-endpoints=https://172.16.111.70:2379,https://172.16.111.71:2379,https://172.16.111.72:2379 -etcd-cafile=/data/etcd/cfssl/ca.pem -etcd-certfile=/data/etcd/cfssl/etcd.pem -etcd-keyfile=/data/etcd/cfssl/etcd-key.pem"
EOF

# 配置 flanneld 启动文件
vim /usr/lib/systemd/system/flanneld.service
[Unit]
Description=Flanneld overlay address etcd agent
After=network-online.target network.target
Before=docker.service

[Service]
Type=notify
EnvironmentFile=/data/kubernetes/conf/flanneld
ExecStart=/data/kubernetes/bin/flanneld --ip-masq $FLANNEL_OPTIONS
ExecStartPost=/data/kubernetes/bin/mk-docker-opts.sh -k DOCKER_NETWORK_OPTIONS -d /run/flannel/subnet.env
Restart=on-failure

[Install]
WantedBy=multi-user.target

# 配置 Docker 启动文件
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

将配置文件启动文件分发至 其他节点
ansible node -m copy -a'src=/data/kubernetes/bin/flanneld dest=/data/kubernetes/bin/flanneld'
ansible node -m copy -a'src=/data/kubernetes/bin/mk-docker-opts.sh dest=/data/kubernetes/bin/mk-docker-opts.sh'
ansible node -m copy -a'src=/data/kubernetes/conf/flanneld dest=/data/kubernetes/conf/flanneld'
ansible node -m copy -a'src=/usr/lib/systemd/system/flanneld.service dest=/usr/lib/systemd/system/flanneld.service'

# 将 docker 启动文件分发至所有节点
ansible node -m copy -a'src=/usr/lib/systemd/system/docker.service dest=/usr/lib/systemd/system/docker.service'

# 添加执行权限
ansible all -m shell -a'chmod +x /data/kubernetes/bin/*'

# 启动服务
ansible all -m shell -a'systemctl daemon-reload && systemctl start flanneld && systemctl enable flanneld && systemctl restart docker'
```

```shell


# 安装 docker 依赖
yum install -y yum-utils device-mapper-persistent-data lvm2
```
