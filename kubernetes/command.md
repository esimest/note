# Kubernetes Docker 命令

## 常用 kubectl 命令

```shell
# 执行 yaml 文件
kubectl apply -f ${yaml_file}

# 单个 pod 含有多个 container 时进入容器
kubectl exec -it ${pod_name} -c ${container_name} bash

# 进入容器
kubectl exec -it $(kubectl get po -n ${ns} |grep ${img_name} | awk 'NR==1{print $1}') -n ${ns} bash

# 命令行创建 svc
kubectl expose deploy ${deploy_name} --port=${dest_port} --target-port=${expose_port}

# 删除 pod
kubectl delete po ${pod_name}

# 删除 ReplicaSet
kubectl delete rs ${rs_name}

# node 打标签
kubectl label nodes ${node_name} ${key}=${value}

# 覆盖 node 上的标签
kubectl label nodes ${node_name} ${key}=${value} --over-write
```

## 常用别名

```shell
alias kd='kubectl delete  pod --all-namespaces'
alias kds='kubectl delete svc --all-namespaces'
alias kg='kubectl get pod --all-namespaces -o wide |grep '
alias kgs='kubectl get svc --all-namespaces -o wide |grep '

function ke(){
  kubectl exec -it $1 --all-namespaces bash;
}
alias ke=ke
alias ka="kubectl get pod --all-namespaces -o wide"
alias kas="kubectl get svc --all-namespaces -o wide"
alias kc="kubectl --all-namespaces describe pod"
alias kl="kubectl logs"
```

## Kubernetes 一些对象的简写(可直接在命令行中使用)

```shell
* all
* certificatesigningrequests (aka 'csr')
* clusterrolebindings
* clusterroles
* componentstatuses (aka 'cs')
* configmaps (aka 'cm')
* controllerrevisions
* cronjobs
* customresourcedefinition (aka 'crd')
* daemonsets (aka 'ds')
* deployments (aka 'deploy')
* endpoints (aka 'ep')
* events (aka 'ev')
* horizontalpodautoscalers (aka 'hpa')
* ingresses (aka 'ing')
* jobs
* limitranges (aka 'limits')
* namespaces (aka 'ns')
* networkpolicies (aka 'netpol')
* nodes (aka 'no')
* persistentvolumeclaims (aka 'pvc')
* persistentvolumes (aka 'pv')
* poddisruptionbudgets (aka 'pdb')
* podpreset
* pods (aka 'po')
* podsecuritypolicies (aka 'psp')
* podtemplates
* replicasets (aka 'rs')
* replicationcontrollers (aka 'rc')
* resourcequotas (aka 'quota')
* rolebindings
* roles
* secrets
* serviceaccounts (aka 'sa')
* services (aka 'svc')
* statefulsets (aka 'sts')
* storageclasses (aka 'sc')
```
