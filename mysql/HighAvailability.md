# MySQL 高可用

> 高可用的核心目的是减少数据库服务的不可用时间（包括数据库宕机；数据库进程正常，但是响应不正常等）
> 高可用的一个原则是，减少数据库不可用的开销不能大于可用状态下数据库带来的盈利。
> 将大的系统，合理分割成多个子系统，逐个对子系统做高可用设计会比对整体做高可用设计要容易实现，分析

## 数据库宕机原因分析

### 数据库运行环境（操作系统，磁盘，内存，网络等）

- 磁盘空间不足（最常见）

### 性能问题

- schema 和 index 设计不规范

- Write SQL 编写不合理

### Replication（本意是提高数据库的可用性）

- master 与 replica 数据不一致

### 数据丢失或损坏，以及其它各类原因

- 数据丢失(drop table), 备份策略不完善

## 高可用实现

### 避免宕机

> 通过平均故障时间来衡量(mean time between failures: MTBF)

- Test your recovery tools and procedures, including restores from backups.
- Follow the principle of least privilege.
- Keep your systems clean and neat.
- Use  good  naming  and  organization  conventions  to  avoid  confusion,  such  aswhether servers are for development or production use.
- Upgrade your database server on a prudent schedule to keep it current.
- Test  carefully  with  a  tool  such  as pt- upgrade  from  Percona  Toolkit  beforeupgrading.
- Use InnoDB, configure it properly, and ensure that it is set as the default storageengine and the server cannot start if it is disabled.
- Make sure the basic server settings are configured properly.
- Disable DNS with skip_name_resolve.
- Disable the query cache unless it has proven beneficial.
- Avoid complexity, such as replication filters and triggers, unless absolutely needed.
- Monitor important components and functions, especially critical items such asdisk space and RAID volume status, but avoid false positives by alerting only onconditions that reliably indicate problems.
- Record as many historical metrics as possible about server status and performance,and keep them forever if you can.
- Test replication integrity on a regular basis.
- Make replicas read- only, and don’t let replication start automatically.
- Perform regular query reviews.
- Archive and purge unneeded data.
- **Reserve some space in filesystems. In GNU/Linux, you can use the –m option toreserve space in the filesystem itself. You can also leave space free in your LVMvolume group. Or, perhaps simplest of all, just create a large dummy file that youcan delete if the filesystem becomes completely full.**
- Make a habit of reviewing and managing system changes and status and performance information.

### 宕机发生时，快速恢复

> 通过平均恢复时间来衡量(mean time to recovery: MTTR)

- 构建冗余

- 故障转移
