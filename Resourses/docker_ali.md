# Docker 阿里仓库

## 镜像仓库

```shell
# 登录阿里云仓库
docker login --username=esimes registry.cn-hangzhou.aliyuncs.com

# 从仓库拉取镜像
docker pull registry.cn-hangzhou.aliyuncs.com/esimet/rep1:[镜像版本号]

# 将镜像推送至阿里仓库
docker login --username=esimes registry.cn-hangzhou.aliyuncs.com
docker tag [ImageId] registry.cn-hangzhou.aliyuncs.com/esime/rep1:[镜像版本号]
sudo docker push registry.cn-hangzhou.aliyuncs.com/esime/rep1:[镜像版本号]
```
