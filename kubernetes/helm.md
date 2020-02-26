# Helm

```shell
# 安装 tiller 依赖
yum install -y socat

# 获取 helm(3 版本不需要 tiller)
wget https://get.helm.sh/helm-v3.0.1-linux-amd64.tar.gz

# 添加仓库源
helm repo add ${repo_name} https://kubernetes.oss-cn-hangzhou.aliyuncs.com/charts
helm repo add ${repo_name} https://burdenbear.github.io/kube-charts-mirror

# install 时设置资源的名称空间(需要提前创建 ns)
helm install ${name} ${path} --namespace=${ns}

```
