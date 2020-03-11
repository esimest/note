# kubernetes 问题记录

## apiserver 日志不输出到日志目录

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

## harbor 推送镜像

1. 由于项目名称包含多个下划线，导致项目可以创建但是**无法推送镜像**。
