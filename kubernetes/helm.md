# Helm

```shell
# 安装 tiller 依赖
yum install -y socat

# 获取 helm
wget https://get.helm.sh/helm-v2.16.1-linux-amd64.tar.gz

# 安装 tiller(helm 服务端)
helm init --upgrade -i registry.cn-hangzhou.aliyuncs.com/google_containers/tiller:v2.16.1  --stable-repo-url https://kubernetes.oss-cn-hangzhou.aliyuncs.com/charts
```
