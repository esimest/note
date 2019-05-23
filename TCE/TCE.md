##
> tce整体包含哪些产品；
> 部署一个tce包含哪些步骤；
> 基础支撑，gaiastack的部署详细方法；
> 拉管控的方法；
> 熟悉某一类产品生产节点的部署方法。

### 运营端与租户端的作用
#### 运营端
> 资源管理
> 规格管理
> 客户管理
> 如 母机投放，创建资源（如CVM CBS ...）
#### 租户端
> 云资源使用
> 云资源监控

### 产品
#### 计算
- CVM
#### 网络
- VPC
**<font color=red>     NATGW     </font>**
> 点到点 PCGW
> 专线  DCGW
> VPN  PVGW
> JNSGW
> VPCGW

- LB
> TGW

#### 存储
- CBS
- COS
- CFS
- CAS

#### 数据库
- 关系型数据库
> MariaDB(TDSQL)

- 文档型数据库
> MongoDB

- 缓存型数据库
> Redis

#### 运维工具
- 织云
- 云拨测
- 密码库

#### 监控工具
- barad **<font color=red> barad_agent 所有物理机都要安装</font>**

#### 安全
- 主机安全 云镜
- 网站安全 WAF

#### 中间件
- TSF
- CMQ
- CKAFKA
- APIGW

### 部署 TCE 的完整步骤
1. 物料，环境（机器/网络/VPN/服务器开电）
2. Gaia + 支撑 的 OS 安装
3. Gaia，支撑 部署
4. 拉管控（VStation，DCOS,Ingress, DNS, CBS）
5. 生产节点 OS 安装
> 5 张表导入CDB
> OK 后 使用 DCOS装机 --> 母机投放：VPC母机（租户端）/非VPC母机（运营端）
6. 生产节点软件部署
> CVM 母机部署哪些软件，CBS 母机需要部署哪些软件 等
7. 部署联调