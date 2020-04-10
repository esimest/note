# ip 命令

[文档](http://www.policyrouting.com/iproute2.doc.html)
[ip a 输出解读](https://linux.cn/article-9476-1.html)

## 单网卡多 IP 配置(eth0为例)

### 配置文件配置

1. `cp /etc/sysconfig/network-scripts/ifcfg-eth0 /etc/sysconfig/network-scripts/ifcfg-eth0:1`
   > 其中 ifcfg-eht0:1 表示第二个配置
2. 修改 ifcfg-eth0:1 文件将 ip 信息修改为需要设置的 ip mask gateway..
3. `systemctl restart network`

### ip 命令设置

`ip a add ${ip/mask} dev eth0`

## ip route/r/ro

