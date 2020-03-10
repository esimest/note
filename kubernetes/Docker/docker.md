# Docker 笔记

> [docker daemon 配置参数参考](https://docs.docker.com/engine/reference/commandline/dockerd/)

2019.3.25

----

- 删除标签(tag)的两种方式

  1. 直接删除镜像，相关的所有tag会被删除 `docker rmi -f img_id`
  2. 删除repository:tag `docker rmi repository:tag`

2019.4.25

----

**<font color=red>容器内没有前台进程会自动关闭</font>**

- 查看docker 版本信息
  1. docker version
  2. docker info

- 运行容器 (docker run [opt] img_name [command] [command_args])
  1. -t --tty (添加终端，不添加无法与容器进行交互)
  2. -i --interactive (进入交互模式)

- 启动停止的容器 (docker start [opt] container_id/name)
  1. -a --attach （尝试启动停止的容器）
  2. -i （进入交互式）

- 查看容器元数据
  1. docker insepct container_id/name

- 向运行中的容器发送命令
  1.docker exec [opt] container_id/name command [command_args]
  2. docker exec -it containerr_id/name /bin/sh 进入容器

- 打包镜像
  1. docker save img_1 img_2 img_3 -o output_file

- 加载镜像
  2. docker load -i tar_file

- 容器的几种状态
  1. created
  2. started
  3. runnig
  4. paused
  5. stopped
  6. deleted

2019.5.15

----

> docker rm/rmi/stop/start等命令的参数都可以是list
> 如：docker rmi $(docker images -a -q)其中socker images -a -q 通常会返回多个值

![docker架构](./images/docker架构.png)

```shell
# Only display numeric IDs
docker ps -q/--quite docker images -q/--quite

# 进入正在运行的容器
docker exec -it container_id /bin/bash
# Usage:  docker attach [OPTIONS] CONTAINER, 打开容器的stdin，如果输入exit会结束容器
# ctrl + p + q 退出不终止容器
docker attach

#  Copy files/folders between a container and the local filesystem
- docker cp
```

- 构建镜像
  1. docker commit
  2. docker build

## docker 网络

```shell
# 创建容器时指定容器ip（只能在自定义网络场景中使用）
run --ip ip_address img
```

### docker 默认的四种网络模式

- bridge模式

> docker默认的网络模式，该模式创建容器时会为容器分配一个network namespace,。
> 容器会虚拟出一个自己的网卡，默认会连接到宿主机上一个虚拟网桥docker0上，容器的网关就是docker0的IP

- host 模式

> 该模式创建容器时不会为容器分配一个网络名称空间，而是和宿主机公用一个网络名称空间。
> 容器也不会虚拟出自己的网卡，配置自己的IP等，而是使用宿主机的 IP 和端口

- container 模式

> 该模式新创建的容器和已经存在的一个容器共享网络名称空间
> 因此容器的 IP 端口都是和已存在的容器共享的

- none 模式

> 该模式创建的容器会拥有自己的网络名称空间，但是不会进行任何网络配置。
> 因此这样创建的容器再不进行网络配置的前提下是无法进行网络通信的

#### 其他网络模式

- flannel + etcd

> 需要修改docker启动配置，使其使用flannel进行IP分配
> 每台运行docker守护进程的宿主机运行flannel，并使用etcd保存flannel的数据

----

> 原理：
>> 在etcd中规划所有宿主机的docker0子网范围
>> 每台宿主机上的flanneld进程根据etcd的配置信息，为主机的docker0分配子网，保证所有docker0网段不重复，并将docker0与宿主机IP的映射关系保存至etcd中
>> 当不同宿主机上的容器需要通信时，首先由flanneld查找etcd并获取目的容器的宿主机的IP
>> flanneld将源容器发送的报文封装成UPD报文，由宿主机以目的宿主机IP封装成IP报文
>> 由于目的IP是宿主机IP因此上面封装的IP报文是路由可达的
>> IP发送到目的宿主机后，由宿主机解析并获取原始数据包，然后通过docker0转发至目的容器

2019.07.31

----

```shell
# load 名字为 img_name.release.tar.gz 的镜像
docker load -i ig_name.release.tar.gz

# push 上面 load 的镜像
docker push $(docker images | grep $(echo "${img_name}" |cut -d '.' -f1) |awk '{print $1":"$2}')
```

2019.09.01

----

```shell
# 容器互联
## --link 会在新容器内添加对 ${container_name} 和 ${alias} 的 hosts 解析
docker run --link ${container_name}:${alias} img_name

# 查看主机端口到容器端口映射情况
docer port ${container_name} [port_in_container]

# 共享容器数据卷
# 新容器使用 src_container 容器的数据卷
docker run --volumes-from ${src_container} img_name
```

2019.09.03

----

```shell
# jenkins 构建时报错 Couldn't connect to Docker daemon at http+docker://localhost - is it running?
/etc/docker/daemon.json 添加 "hosts": ["fd://", "tcp://0.0.0.0:2375"],
添加 export DOCKER_HOST='TCP://127.0.0.1:2375'

# jenkins 构建时找不到 /usr/local/bin 目录下的 docker-compse
软链 到 /usr/bin 目录下

```
