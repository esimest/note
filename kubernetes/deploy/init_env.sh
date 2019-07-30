#!/bin/bash

# init_env.sh --- 初始化集群环境

# 关闭防火墙和 selinux
systemctl stop firewalld && systemctl disable firewalld
setenforce 0
sed -i 's/SELINUX=enabled/SELINUX=disabled/g' /etc/selinux/config

# 关闭 swap
swapoff -a && sysctl -w vm.swappiness=0

# 设置 Docker 参数
tee /etc/sysctl.d/kubernetes.conf << EOF > /dev/null
net.ipv4.ip_forward = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
sysctl -p /etc/sysctl.d/kubernetes.conf

# 安装 docker 依赖
yum install -y wget screen yum-utils device-mapper-persistent-data lvm2

modprobe br_netfilter
