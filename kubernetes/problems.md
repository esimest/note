# kubernetes 问题记录

- 没有权限查看容器日志
  *这是一个通用问题，各种报错没有权限，都可以先查看角色绑定的问题，注意大小写哈哈哈*
  > 报错 `Error from server (Forbidden): Forbidden (user=system:anonymous, verb=get, resource=nodes, subresource=proxy) ( pods/log volume-pod)`
  > 解决 `kubectl create clusterrolebinding system:anonymous   --clusterrole=cluster-admin   --user=system:anonymous`

- Pod 一直处于 Pending 状态，describe 报错 NoMatchedLocalDisk
   > 查看 kubelet 的配置，查看磁盘对应的配置的路径
