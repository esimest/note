# Docker Command

## 常用命令

```shell
# 在新的容器运行指定的命令(默认为 /bin/bash)
docker run [options] ${image} [command]

# 容器停止时自动删除容器
docker run --rm [options] ${image} [command]
```

## Alias

```shell
# 刪除所有停止的容器
alias drms='docker rm $(docker ps -q -f "status=exited")'
```
