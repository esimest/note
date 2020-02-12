# Docker Command

## Command

### run

```shell
# 在新的容器运行指定的命令(默认为 /bin/bash)
docker run [options] ${image} [command]

# 容器停止时自动删除容器
docker run --rm

# 以分离模式运行容器
## 默认会附着 stdin stdout sdterr
docker run -d

# 设置容器的 hostname
docker run --hostname=${hostname}

# 特权模式运行容器, 容器可以以 root 权限访问宿主机.
docker run --periviledged
```

#### NameSpace

```shell
# --mount(设置挂载点)

# 共享宿主机 IPC 名称空间
docker run --ipc=host

# 共享其他容器 IPC 名称空间
docker run --ipc=container:${name|id}

# 使用桥接网络模式( 默认)
docker run --network=bridge

# 共享宿主机网络名称空间
docker run --network=host

# 共享其他容器网络名称空间
docker run --network=container:${name|id}

# 共享宿主机 PID 名称空间
docker run --pid=host

# 共享其他容器 PID 名称空间
docker run --pid=container:

# 共享宿主机 UTS 名称空间
docker run --uts=host

# 共享宿主机用户名称空间
docker run --userns=host
```

### inspect

```shell
# 查看容器 IP 地址
docker inspect -f='{{.NetworkSettings.IPAddress}}' ${name|id}

# 查看容器的所有镜像层目录
docker inspect ${container} -f={{.GraphDriver.Data.LowerDir}}| awk 'BEGIN{RS=":"}{print}'
```

## Alias

```shell
# 刪除所有停止的容器
alias drms='docker rm $(docker ps -q -f "status=exited")'
```
