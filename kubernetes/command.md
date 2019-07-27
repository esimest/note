# Kubernetes Docker 命令

```shell
# 进入容器
kubectl exec -it $(kubectl get po -n ${ns} |grep ${img_name} | awk 'NR==1{print $1}') -n ${ns} bash

# load 名字为 img_name.release.tar.gz 的镜像
docker load -i ig_name.release.tar.gz

# push 上面 load 的镜像
docker push $(docker images | grep $(echo "${img_name}" |cut -d '.' -f1) |awk '{print $1":"$2}')
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
