# Kubernetes 安装配置笔记

## Docker-CE 安装

- 镜像仓库(mirrors.tuna.tsinghua.edu.cn清华大学镜像网站)

```shell
# 下载 docker yum 源
cd /etc/yum.repos.d && wget https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/centos/docker-ce.repo
# 修改 yum 源
vi docker-ce.repo
# 替换变量
1,$s/https:\/\/download.docker.com/https:\/\/mirrors.tuna.tsinghua.edu.cn\/docker-ce/g
```

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

### Git2.x安装

```shell
yum install -y epel-release
rpm -ivh https://centos7.iuscommunity.org/ius-release.rpm
yum install -y git2u
```

## Kubernetes 安装

- 同步时间
  1. yum install -y nptdate
  2. ntpdate -u cn.pool.ntp.org

- SSH认证
  1. ssh-keygen
  2. ssh-copy-id xxxx.xxxx.xxxx.xxxx

- 安装配置CFSSL

   ```shell
    wget https://pkg.cfssl.org/R1.2/cfssl_linux-amd64 -O /usr/local/bin/cfssl
    wget https://pkg.cfssl.org/R1.2/cfssljson_linux-amd64 -O /usr/local/bin/cfssljson
    wget https://pkg.cfssl.org/R1.2/cfssl-certinfo_linux-amd64 -O /usr/bin/cfssl-certinfo
    chmod +x /usr/local/bin/cfssl /usr/local/bin/cfssljson /usr/bin/cfssl-certinfo
    ```

- 安装etcd

  ```shell
  wget https://github.com/etcd-io/etcd/releases/download/v3.3.11/etcd-v3.3.11-linux-amd64.tar.gz
  tar -zxvf ./etcd-v3.3.11-linux-amd64.tar.gz -c /data
  ln -s /data/etcd-v3.3.11-linux-amd64/etcd /usr/bin/etcd
  ln -s /data/etcd-v3.3.11-linux-amd64/etcdctl /usr/bin/etcdctl
  etcd -name etcd \
  -data-dir /var/lib/etcd \
  -listen-client-urls http://0.0.0.0:2379,http://0.0.0.0:4001 \
  -advertise-client-urls http://0.0.0.0:2379,http://0.0.0.0:4001 \
  >> /var/log/etcd.log 2>&1 &

  # 查看健康状态
  etcdctl -C http://localhost:4001 cluster-health
  ```

- 安装kubernetes

  ```shell
  wget https://github.com/kubernetes/kubernetes/releases/download/v1.14.0/kubernetes.tar.gz
  tar -zxvf kubernetes.tar.gz -C /data
  cd /data/kubernetes/server && tar -zxvf ./kubernetes-manifests.tar.gz
  cd /data/kubernetes/server && find ./ -perm 755 | xargs -i cp {} /usr/bin/

  kube-proxy --logtostderr=true \
  --v=4 \
  --hostname-override=172.16.14.157 \
  --cluster-cidr=10.0.0.0/24 \
  --config=/k8s/kubernetes/cfg/kube-proxy.kubeconfig \
  --client-connection=/k8s/kubernetes/cfg/kube-apiserver.kubeconfig
  --kubeproxy.config.k8s.io/v1alpha1
  kubectl label node 172.16.14.152  node-role.kubernetes.io/node='node'
  kubectl label node 172.16.14.157  node-role.kubernetes.io/node='node'
  ```