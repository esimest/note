# Helm

```
# 安装 tiller 依赖
yum install -y socat
# 安装 tiller
helm init --upgrade -i registry.cn-hangzhou.aliyuncs.com/google_containers/tiller:v2.14.0  --stable-repo-url https://kubernetes.oss-cn-hangzhou.aliyuncs.com/charts
```