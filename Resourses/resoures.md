# 下载资源

## yum 源

- ansible

> `rpm -ivh https://mirror.webtatic.com/yum/el7/epel-release.rpm`

- git

> `rpm -ivh https://centos7.iuscommunity.org/ius-release.rpm`

- Python
   `yum -y install https://centos7.iuscommunity.org/ius-release.rpm`
   `yum install -y python36u python36u-pip python36u-devel`

- Docker

```shell
# 下载 docker yum 源
cd /etc/yum.repos.d && wget https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/centos/docker-ce.repo
# 替换变量
sed -i 's/https:\/\/download.docker.com/https:\/\/mirrors.tuna.tsinghua.edu.cn\/docker-ce/g' /etc/yum.repos.d/docker-ce.repo

# 安装 docker 依赖
yum install -y wget screen yum-utils device-mapper-persistent-data lvm2

modprobe br_netfilter

# 安装dokcer
yum install -y docker-ce

# 镜像加速
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
"registry-mirrors": ["https://sx6i79oq.mirror.aliyuncs.com"]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker

```

- pip 源

```shell
# pip.conf/pip.ini
[global]
timeout = 60
index-url = https://pypi.doubanio.com/simple

# linux 存放目录
$HOME/.config/pip/pip.conf 或 $HOME/.pip/pip.conf

# windows 存放目录
%APPDATA%\pip\pip.ini 或%HOME%\pip\pip.ini
```

## 软件下载链接

- [flannel](https://github.com/coreos/flannel/releases)

- [etcd](https://github.com/coreos/etcd/releases)
