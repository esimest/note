# 证书与加密

## HTTPS 与 SSL/TLS

http 报文是明文的，因此报文内容很容器被网络中的黑客或不法组织获取。
通过使用 SSL(Secure Sockets Layer) 协议将 http 报文加密从而提高安全性。
TLS(Transport Layer Security) 是 SSL 的升级版本
HTTPS = HTTP + SSL/TLS

- TLS
  1. 客户端明文请求 + 随机数(rand_c)
  2. 服务端返回公钥 + 随机数(rand_s)
  3. 客户端验证公钥，生成随机数(rand_peer)使用公钥加密发送给服务端。(服务端也可以验证客户端)
     计算得出协商密钥 Func(rand_c, ranc_s, rand_peer)
  4. 服务端也算出协商密钥(用于特定的客户端与服务端使用，因为公钥都是一样的，无法区分客户端)

## 加密算法与哈希

- 对称加密：加密解密使用同一个密钥

- 非对称加密：加密和解密使用不通的密钥

- 哈希算法：可将明文加密成指定长度的 hash 值，无法使用 hash 值还原明文


## 证书

- X509: TLS 证书的标准(确定了证书内应该包含哪些内容)
- CA(Certificate Authority 证书颁发机构): 用于颁发证书，验证证书的合法性

## 使用 openssl 生成 x509 证书 + 密钥
