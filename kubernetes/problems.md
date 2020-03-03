# kubernetes 问题记录

- 没有权限查看容器日志
  *这是一个通用问题，各种报错没有权限，都可以先查看角色绑定的问题，注意大小写哈哈哈*
  > 报错 `Error from server (Forbidden): Forbidden (user=system:anonymous, verb=get, resource=nodes, subresource=proxy) ( pods/log volume-pod)`
  > 解决 `kubectl create clusterrolebinding system:anonymous   --clusterrole=cluster-admin   --user=system:anonymous`

- Pod 一直处于 Pending 状态，describe 报错 NoMatchedLocalDisk
   > 查看 kubelet 的配置，查看磁盘对应的配置的路径

## 日志不输出到日志目录

### 问题描述

配置选项添加了 --log-dir=${log_dir}, 并且创建了日志目录.
但是日志不输出至日志目录中.

### 解决

需要将 --logtostderr 选项显示的置为 false.

## kubectl cp 报错

### 问题描述

```shell
# kubectl cp kube-system/etcd-node-151:/usr/local/bin/etcd /usr/bin/etcd
tar: Removing leading `/' from member names
```

### 解决

容器中的目录应该为 ${work_dir} 的相对路径, 如果没指定 work_dir 则使用绝对路径表示.
**注: `kubectl cp` 命令需要 `tar` 的支持**
