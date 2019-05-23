- 项目地址
> https://github.com/cloudflare/cfssl

> mv /usr/local/bin/cfssl_linux-amd64 /usr/local/bin/cfssl
> mv cfssl_linux-amd64 cfssl

> mv /usr/local/bin/cfssljson_linux-amd64 /usr/local/bin/cfssljson
> mv cfssljson_linux-amd64 cfssljson
### CA 请求
```
cat << EOF | tee ca-csr.json
{
"CN": "virtual",
"key": {
    "algo": "rsa",
    "size": 2048
},
"names": [
    {
        "C": "CN",
        "L": "Shenzhen",
        "ST": "Shenzhen"         
    }    ]
}
EOF
```
### 术语介绍
> CN: Common Name，浏览器使用该字段验证网站是否合法，一般写的是域名。非常重要。浏览器使用该字段验证网站是否合法

> C: Country， 国家

> L: Locality，地区，城市

> O: Organization Name，组织名称，公司名称

> OU: Organization Unit Name，组织单位名称，公司部门

> ST: State，州，省

- 生成 CA 证书和 CA 私钥和 CSR (证书签名请求):
> ` cfssl gencert -initca ca-csr.json | cfssljson -bare ca  ## 初始化 ca `
> ` ls ca* `
> ca.csr  ca-csr.json  ca-key.pem  ca.pem

> 该命令会生成运行 CA 所必需的文件 ca-key.pem（私钥）和 ca.pem（证书），还会生成 ca.csr（证书签名请求），用于交叉签名或重新签名。
### CA 证书生成策略

```
cat << EOF | tee ca-config.json
{
  "signing": {
    "default": {
      "expiry": "87600h"
    },
    "profiles": {
      "kubernetes": {
        "usages": [
            "signing",
            "key encipherment",
            "server auth",
            "client auth"
        ],
        "expiry": "87600h"
      },
      "www": {
        "usages": [
            "signing",
            "key encipherment",
            "server auth",
            "client auth"
        ],
        "expiry": "87600h"
      },
      "etcd": {
        "usages": [
            "signing",
            "key encipherment",
            "server auth",
            "client auth"
        ],
        "expiry": "87600h"
      }
    }
  }
}
EOF
```
> 这个策略，有一个默认的配置，和一个 profiles，可以设置多个 profile，
> 默认策略，指定了证书的有效期是一年 (8760h)

> etcd 策略，指定了证书的用途

> signing, 表示该证书可用于签名其它证书；生成的 ca.pem 证书中 CA=TRUE

> server auth：表示 client 可以用该 CA 对 server 提供的证书进行验证

> client auth：表示 server 可以用该 CA 对 client 提供的证书进行验证
### 常用命令
> cfssl gencert -initca ca-csr.json | cfssljson -bare ca ## 初始化 ca

> cfssl gencert -initca -ca-key key.pem ca-csr.json | cfssljson -bare ca ## 使用现有私钥，重新生成

> cfssl certinfo -cert ca.pem

> cfssl certinfo -csr ca.csr

### etcd 证书请求
```
cat << EOF | tee etcd-csr.json
{
    "CN": "etcd",
    "hosts": [
    "172.16.14.151",
    "172.16.14.152",
    "172.16.14.157"
    ],
    "key": {
        "algo": "rsa",
        "size": 2048
    },
    "names": [
        {
            "C": "CN",
            "L": "Shenzhen",
            "O": "etcd",
            "OU": "System",
            "ST": "Shenzhen"
        }
    ]
}
EOF
```

### kube-apiserver 证书请求
```
cat << EOF | tee kube-apiserver-csr.json
{
    "CN": "kubernetes",
    "hosts": [
      "10.0.0.1",
      "127.0.0.1",
      "172.16.14.151",
      "kubernetes",
      "kubernetes.default",
      "kubernetes.default.svc",
      "kubernetes.default.svc.cluster",
      "kubernetes.default.svc.cluster.local"
    ],
    "key": {
        "algo": "rsa",
        "size": 2048
    },
    "names": [
        {
            "C": "CN",
            "L": "Shenzhen",
            "ST": "Shenzhen",
            "O": "k8s",
            "OU": "System"
        }
    ]
}
EOF
```

### kube-proxy 证书请求
```
cat << EOF | tee kube-proxy-csr.json
{
  "CN": "system:kube-proxy",
  "hosts": [],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "L": "Shenzhen",
      "ST": "Shenzhen",
      "O": "k8s",
      "OU": "System"
    }
  ]
}
EOF
```

- 生成ca证书
> cfssl gencert -initca ca-csr.json | cfssljson -bare ca -

- 生成服务证书
  1. kube-apiserver
  > cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=kubernetes kube-apiserver-csr.json | cfssljson -bare kube-apiserver
  2. kube-proxy
  > cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=kubernetes kube-proxy-csr.json | cfssljson -bare kube-proxy
  2. etcd
  > cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=etcd etcd-csr.json | cfssljson -bare etcd
