# MySql 锁机制

> 锁机制用于管理对共享资源的并发访问，提供数据的完整性和一致性。可以实现事务的隔离性
> 开销和性能无法同时达到最优，所以要选择一种对当前环境性价比最高的策略/机制。

## InnoDB 锁分类

> SELECT 隐式添加一致性非锁定行读

### 行级锁

- 共享锁(S Lock)       读锁
   > 允许事务读取一行数据。S Lock 兼容 S Lock
- 排它锁(X Lock)       写锁
   > 允许事务删除或更改一行数据。X Lock 不兼容任何锁

### 表级锁(意向锁)

- 意向共享锁(IS Lock)
   > 事务想获取一张表中某几行的共享锁
- 意向排他锁(IX Lock )
   > 事务想获取一张表中某几行的排他锁

information_shcema.(innodb_trx,innodb_locks,innodb_lock_waits)

```shell
# 显示添加 S Lock
SELECT $column LOCK IN SHARE MODE;
# 显示添加 X Lock
SELECT $column FOR UPDATE

```

## 锁带来的问题

1. 丢失更新（添加X Lock)
2. 脏读
3. 不可重复读
4. 阻塞
5. 死锁（并行（事务）情况下）：InnoDB在大部分异常情况下不会回滚数据库。但是发生死锁时，会进行回滚

## 所相关操作

```mysql
# 查找所有和 lock 有关信息
show status like '%lock%'

# 查看当前运行的 mysql 线程
SHOW PROCESSLIST;

# 查看所有当前运行的 mysql 线程
SHOW FULL PROCESSLIST;

# 清除 3 天前的 BINLOG
PURGE MASTER LOGS BEFORE DATE_SUB(CURRENT_DATE, INTERVAL 3 DAY);
```
