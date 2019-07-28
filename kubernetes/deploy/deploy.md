# 二进制部署 Kuberntes

## ansible

> 安装 ansible, 并配置 hosts 和 修改 host_key_check

 `yum install -y epel-release && yum install -y ansible`

## Environment init

> 修改环境配置(init_env.sh)

`ansible all -m script -a'${path}/init_env.sh`
