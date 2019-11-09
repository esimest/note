# OPENSSL

## 使用

> 使用 openssl help 可以查看 openssl 的使用方式
> openssl help 的输出结果可以分为三部分

- Standard Commands
   > 所有可以使用的子命令

- Message Digest commands
   > 哈希算法子命令

- Cipher commands
   > 加密算法子命令(包括对称加密和非对称加密)

### 常用命令

```shell
# 查看使用方式
openssl help
man openssl

# 查看标准子命令使用方式
man ${standard command}
## 查看 openssl x509 子命令使用方式
man x509

# 查看版本
openssl version [-a 查看详细信息]

```

## 密码库

## 密钥和证书管理

### 生成证书

```
# 使用 RSA 算法生成私钥并使用 aes-128 算法加密私钥(创建过程中需要输入密码)
openssl genrsa -aes128 -out fd.key 2048

# 解析私钥结构
openssl rsa -text -in fd.key

# 查看私钥对应的公钥
openssl rsa -pubout -in fd.key

# 创建证书申请
openssl req -new -key fd.key -out fd.csr -subj "/C=GB/L=London/O=Feisty Duck Ltd/CN=www.feistyduck.com"

# 使用当前证书创建新的证书请求
opensssl x509 -x509toreq -in fd.crt -out fd.csr -signkey fd.key

# 创建自签证书
openssl x509 -req -days 365 -in fd.csr -signkey fd.key -out fd.crt

# 直接使用私钥创建证书(需要输入相关信息)
openssl req -new -x509 -days 365 -key fd.key -out fd.crt

# 使用私钥生成证书(非交互式, CN 必填)
openssl req -new -x509 -days 365 -key fd.key -out fd.crt  -subj "/C=GB/L=London/O=Feisty Duck Ltd/CN=www.feistyduck.com"

```

### 创建私有 CA


### 密钥和证书格式转换

#### 常见的几种证书和密钥存储格式

- DER(二进制格式)
   > 包含原始格式的 x509 证书，使用 DER ASN.1 编码

- PEM( ASCII 编码格式)
   > 包含 base64 编码过的 DER 证书
   >以-----BEGIN CERTIFICATE-----开头，以-----END CERTIFICATE-----结尾。
#### 常见格式之间相互转换

```
# PEM 转 DER
openssl x509 -inform PEM -in fd.pem -outform DER -out fd.der

# DER 转 PEM
openssl x509 -inform DER -in fd.der -outform PEM -out fd.pem
```