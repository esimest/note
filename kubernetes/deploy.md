# Deployment

## RS RC 的区别

> 新版本使用 RS + Deploy 来代替 RC

## 升级/更新策略

> 对 deploy 执行升级时有两种策略, RollingUpdate(滚动升级, 默认策略) 和 Recreate(删除旧版本后创建新版本)

### RollingUpdate(type: RollingUpdate)

> 使用 RollingUpdate 策略时有以下几个选项

- maxUnavailable
   > 最多有几个 pod 处于无法工作的状态，默认值是25%

- maxSurge
   > 升级过程中可以比预设的 pod 的数量多出的个数，默认值是25%

- minReadySeconds

## 使用 deploy 实现几种常用的升级策略

### 滚动升级 (默认支持)

### 蓝绿部署

1. 将新版本的容器定义在新的 deploy 中(标签和旧版本一样)
2. 新版本状态 OK 对新版本执行扩缩容，将旧版本 deploy 删除

### 灰度发布/金丝雀发布

1. 将新版本的容器定义在新的 deploy 中(标签和旧版本一样). 副本数不通
2. 逐步调整两个版本的副本数，直到旧版本的副本数为 0