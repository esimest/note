# 下载资源

## yum 源

- Centos
  > curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.cloud.tencent.com/repo/centos7_base.repo

- Epel
  > curl -o /etc/yum.repos.d/epel.repo http://mirrors.cloud.tencent.com/repo/epel-7.repo

- git
  > `rpm -ivh https://centos7.iuscommunity.org/ius-release.rpm`

- Python
   > `yum -y install https://centos7.iuscommunity.org/ius-release.rpm`
   > `yum install -y python36u python36u-pip python36u-devel`

- Docker

```shell
# 下载 docker yum 源
curl -o /etc/yum.repos.d/docker-ce.repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

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

- go 环境变量

```shell
GOROOT  go 安装路径
GOBIN $GOROOT/bin

GOPATH 项目路径，可以有多个值。windows 下以分号分隔，linux 下以冒号分隔
go get 安装目录默认为 GOPATH 中的第一个路径
GOPROXY=https://goproxy.cn 代理源(需设置 GO111MODULE=on )
```
