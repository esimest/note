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

## ceph-deploy

```shell
# 配置代理
export CEPH_DEPLOY_REPO_URL=http://mirrors.aliyun.com/ceph/rpm-jewel/el7
export CEPH_DEPLOY_GPG_URL=http://mirrors.aliyun.com/ceph/keys/release.asc
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
