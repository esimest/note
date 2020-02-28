# Helm

```shell
# 添加仓库源
helm repo add ${repo_name}(charts) https://kubernetes.oss-cn-hangzhou.aliyuncs.com/charts
helm repo add ${repo_name}(stable) https://burdenbear.github.io/kube-charts-mirror

# install 时设置资源的名称空间(需要提前创建 ns)
helm install ${name} ${path} --namespace=${ns}

# 显示 default 名称空间的 helm releases
helm list

# 显示指定名称空间的 hlem releases
helm list --namespace=${ns}
helm list -n${ns}
```

## charts

```shell
# 安装 ingress-nginx chart
helm install --generate-name stable/nginx-ingress \
--namespace=ingress-nginx \
--set defaultBackend.image.repository=mirrorgooglecontainers/defaultbackend-amd64 \
--set controller.service.type=NodePort \
--set controller.service.nodePorts.http=80 \
--set controller.service.nodePorts.https=443


## 安装 harobor chart
helm install --generate-name harbor/harbor \
--namespace=harbor \
--expose.ingress.hosts.core=core.esimest.com \
--expose.ingress.hosts.notary=notary.esimest.com \
--persistence.resourcePolicy=delete \
--externalURL=https://core.esimest.com
```