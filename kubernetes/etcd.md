### 配置
```
cat << EOF | tee /etc/etcd
#[Member]
ETCD_NAME="etcd01"
ETCD_DATA_DIR="/var/lib/etcd/default.etcd"
ETCD_LISTEN_PEER_URLS="https://172.16.14.151:2380"
ETCD_LISTEN_CLIENT_URLS="https://172.16.14.151:2379"

#[Clustering]
ETCD_INITIAL_ADVERTISE_PEER_URLS="https://172.16.14.151:2380"
ETCD_ADVERTISE_CLIENT_URLS="https://172.16.14.151:2379"
ETCD_INITIAL_CLUSTER="etcd01=https://172.16.14.151:2380,etcd02=https://172.16.14.152:2380,etcd03=https://172.16.14.157:2380"
ETCD_INITIAL_CLUSTER_TOKEN="etcd-cluster"
ETCD_INITIAL_CLUSTER_STATE="new"

EOF
```
```
cat << EOF | tee /etc/etcd
#[Member]
ETCD_NAME="etcd02"
ETCD_DATA_DIR="/var/lib/etcd/default.etcd"
ETCD_LISTEN_PEER_URLS="https://172.16.14.152:2380"
ETCD_LISTEN_CLIENT_URLS="https://172.16.14.152:2379"

#[Clustering]
ETCD_INITIAL_ADVERTISE_PEER_URLS="https://172.16.14.152:2380"
ETCD_ADVERTISE_CLIENT_URLS="https://172.16.14.152:2379"
ETCD_INITIAL_CLUSTER="etcd01=https://172.16.14.151:2380,etcd02=https://172.16.14.152:2380,etcd03=https://172.16.14.157:2380"
ETCD_INITIAL_CLUSTER_TOKEN="etcd-cluster"
ETCD_INITIAL_CLUSTER_STATE="new"

EOF
```
```
cat << EOF | tee /etc/etcd
#[Member]
ETCD_NAME="etcd03"
ETCD_DATA_DIR="/var/lib/etcd/default.etcd"
ETCD_LISTEN_PEER_URLS="https://172.16.14.157:2380"
ETCD_LISTEN_CLIENT_URLS="https://172.16.14.157:2379"

#[Clustering]
ETCD_INITIAL_ADVERTISE_PEER_URLS="https://172.16.14.157:2380"
ETCD_ADVERTISE_CLIENT_URLS="https://172.16.14.157:2379"
ETCD_INITIAL_CLUSTER="etcd01=https://172.16.14.151:2380,etcd02=https://172.16.14.152:2380,etcd03=https://172.16.14.157:2380"
ETCD_INITIAL_CLUSTER_TOKEN="etcd-cluster"
ETCD_INITIAL_CLUSTER_STATE="new"

EOF
```

### 启动文件
```
cat << EOF | tee /usr/lib/systemd/system/etcd.service 
[Unit]
Description=Etcd Server
After=network.target
After=network-online.target
Wants=network-online.target

[Service]
Type=notify
EnvironmentFile=/etc/etcd
ExecStart=/usr/local/bin/etcd \
--name=${ETCD_NAME} \
--data-dir=${ETCD_DATA_DIR} \
--listen-peer-urls=${ETCD_LISTEN_PEER_URLS} \
--listen-client-urls=${ETCD_LISTEN_CLIENT_URLS},http://127.0.0.1:2379 \
--advertise-client-urls=${ETCD_ADVERTISE_CLIENT_URLS} \
--initial-advertise-peer-urls=${ETCD_INITIAL_ADVERTISE_PEER_URLS} \
--initial-cluster=${ETCD_INITIAL_CLUSTER} \
--initial-cluster-token=${ETCD_INITIAL_CLUSTER_TOKEN} \
--initial-cluster-state=new \
--cert-file=/root/ca/etcd.pem \
--key-file=/root/ca/etcd-key.pem \
--peer-cert-file=/root/ca/etcd.pem \
--peer-key-file=/root/ca/etcd-key.pem \
--trusted-ca-file=/root/ca/ca.pem \
--peer-trusted-ca-file=/root/ca/ca.pem
Restart=on-failure
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target

EOF
```

### 启动etcd
```
systemctl daemon-reload
systemctl enable etcd
systemctl start etcd
```