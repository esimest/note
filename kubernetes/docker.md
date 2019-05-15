2019.3.25
----
- 删除标签(tag)的两种方式
1. 直接删除镜像，相关的所有tag会被删除` docker rmi -f img_id `
2. 删除repository:tag ` docker rmi repository:tag`
2019.4.25
----
**<font color=red>容器内没有前台进程会自动关闭</font>**
- 查看docker 版本信息
  1. docker version
  2. docker info

- 创建容器 (docker run [opt] img_name [command] [command_args])
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
  5. deleted

2019.5.15
----
> <font color=red></font> docker rm/rmi/stop/start等命令的参数都可以是list
> 如：docker rmi $(docker images -a -q)其中socker images -a -q 通常会返回多个值
- docker架构
![](./images/docker架构.png)

- docker ps -q/--quite docker images -q/--quite
> Only display numeric IDs

- 构建镜像
  1. docker commit 
  2. docker build

- docker exec -it container_id /bin/bash
> 进入正在运行的容器

- docker attach
> Usage:  docker attach [OPTIONS] CONTAINER, 打开容器的stdin，如果输入exit会结束容器
> ctrl + p + q 退出不终止容器

- docker cp 
> Copy files/folders between a container and the local filesystem

### docker 网络
- 创建容器时指定容器ip（只能在自定义网络场景中使用）
> run --ip ip_address img