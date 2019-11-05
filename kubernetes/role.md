# Kubernetes 用户与角色

Kubernetes 使用 RBAC 实现对集群资源的访问控制。权限与角色 (Role ClusterRole) 绑定，
将用户指定为特定角色，从而服务其相关权限。

## Role 与 ClusterRole

- role 具有 namespace 属性，即 role 所具备的权限只适用于 role 所属的 ns。
- clusterrole 为集群通用角色属性，即 clusterrole 所具备的权限适用于集群内所有 ns。

```shell
# 获取 kube-system 名称空间中的所有角色
kubectl get role -n kube-system

# 获取集群的所有角色
kubectl get clusterrole
```

## RoleBinding 与 ClusterRoleBinding

通过创建角色绑定将用户与某个角色绑定，从而使用户具备某种权限。
```shell
# 创建匿名用户使其具备管理员权限
kubectl create clusterrolebinding system:anonymous \
--clusterrole=cluster-admin --user=system:anonymous

# 删除角色绑定
kubectl delete clusterrolebinding system:anonymous
```

## Kubeconfig

集群开启 TLS 认证后，与集群交互都需要身份认证。
kubeconfig 用于配置认证系统，使得可以通过 kubeconfig 与多个集群交互

```
# 设置集群信息，当需要配置多个集群时，通过集群名指定特定的集群
kubectl config set-cluster cluster_name --server='127.0.0.1:8080'

# 定义用于身份认证时的凭据
## 有多种认证方式：用户名/密码，token，客户端证书，客户端密钥
kubectl config set-credentials cre_name --username=admin --password=secert

# 设置默认的上下文
kubectl config set-context default --cluster=cluster_name --user=cre_name
```