# kubernetes 问题记录

- 没有权限查看容器日志
  > 报错 `Error from server (Forbidden): Forbidden (user=system:anonymous, verb=get, resource=nodes, subresource=proxy) ( pods/log volume-pod)`
  > 解决 `kubectl create clusterrolebinding system:anonymous   --clusterrole=cluster-admin   --user=system:anonymous`
