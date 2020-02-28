# Kubernetes 使用 Ceph 作为后端存储

Kubernetes 使用 Ceph 需要准备:

- Ceph Monitor(ip:port) 列表

- UserId(默认为 admin)

- keyring(做 base64 加密)

- 部署 rbd-provisioner
   > kuernetes 使用 ceph 作为后端存储时, controller-manger 管理 ceph 需要用到 ceph-common.
   > kubeadm 安装的 controller-manager 无法直接受用宿主机的$PATH 目录.
   > 因此需要部署 [rbd-provisioner](./yamls/volume/rbd-provisioner.yaml) 以提供 ceph 支持
   > 详见 [kubernetes issues38923](https://github.com/kubernetes/kubernetes/issues/38923)

## Static Volume Provision

1. [创建 ns, secret](./yamls/volume/ceph_secret.yaml)

2. [创建 pv](./yamls/volume/ceph_pv.yaml)

3. [创建 pvc](./yamls/volume/static_pvc.yaml)

4. [创建 pod 使用 pv](./yamls/volume/ceph_pod.yaml)

kubernetes 创建 pvc 后自动创建 pv 并 bound.

## Dynamic Volume Provision

1. [创建 StorageClass](./yamls/volume/storage_class.yaml)

## ceph-command

```shell
# 查看集群健康状态
ceph status
ceph -s

# df
osd df
ceph df
rados df
```

## ceph-alias

```shell
alias osd='ceph osd'
alias mon='ceph mon'
```

## ceph-deploy

```shell
# 配置代理
export CEPH_DEPLOY_REPO_URL=http://mirrors.aliyun.com/ceph/rpm-jewel/el7
export CEPH_DEPLOY_GPG_URL=http://mirrors.aliyun.com/ceph/keys/release.asc

# ceph-deploy mon create-initial 之前需要 yum redhat-lsb

# 删除旧的 osd 卷
ceph-volume lvm zap /dev/sdb --destroy
```

## Problems

### pool full(pool 空间不足)

[Cpeh 关于 backfill 参数的建议](https://ceph.com/planet/%E5%85%B3%E4%BA%8Ebackfill%E5%8F%82%E6%95%B0%E5%BB%BA%E8%AE%AE/)

```shell
# 查看 OSD 阈值
cephs osd dump | grep full

# 设置 OSD 阈值
ceph osd set-full-ratio [0-1]
ceph osd set-nearfull-ratio [0-1]
ceph osd set-backfillfull-ratio [0-1]
```

### service

```shell
# ceph-deploy 版本过低导致以下报错. 更新 ceph-deploy 即可
Running command: /usr/sbin/service ceph -c /etc/ceph/ceph.conf start mon.node-151
The service command supports only basic LSB actions (start, stop, restart, try-restart, reload, force-reload, status). For other actions, please try to use systemctl.
```

### rbd map

**注意: map操作使用的是krbd k8s使用的是rdb, krbd是内核rbd 走的是内核  rbd是走的librbd**
因此, k8s 动态 pv 不需要关闭 ceph 新特性.

```shell
# rbd map rbd/bar
rbd: sysfs write failed
RBD image feature set mismatch. You can disable features unsupported by the kernel with "rbd feature disable bar object-map fast-diff deep-flatten".
In some cases useful info is found in syslog - try "dmesg | tail".

# 原因是内核不支持一些 ceph 的新特性. 关掉即可
# 针对每个 img 执行 disable 操作(需要对每个 img 都执行)
rbd feature disable ${img_name} exclusive-lock, object-map, fast-diff, deep-flatten
# 修改 ceph.conf 重启 ceph 后永久生效
rbd_default_features = 1
```
