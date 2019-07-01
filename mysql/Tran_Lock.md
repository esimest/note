# Mysql 事务与锁

## 事务特性（ACID）

- 原子性(atomicity)
- 一致性(consistency):完整性约束
- 隔离性(isolation):使用锁机制来实现
- 持久性(durability)

> 原子性，一致性，持久性通过redo和undo来实现

## 隔离级别

> 不同事务是相互隔离的
>> 事物之间的隔离是通过锁来实现的，对锁不同程度的应用会产生不同等级的隔离
>> 隔离级别越高，事务之间的相互影响就越小。但是数据库事务的并发性会降低

### read uncommit

> 在提交事物前，就释放了锁
> read uncommit 隔离级别的并发性是最高的（对数据做出改变后立即释放了锁），但是会有以下几种现象会发生

- 脏读：一个事务会读取到另一个事务未提交的数据

- 不可重复读：两个事物同事对一条记录执行更新。在一次事务内多次读取会获得不同的值。

- 幻读：一个事物在数据库中插入或删除数据，导致其他事物的查询记录的数量与之前不同

### read commit

> 提交事务后，然后再释放锁

- 解决了脏读

### repeatable read

> 通过对事务做快照，来实现可重复读取被修改的记录的原始值

- 在 read commit 的基础上解决了不可重复读的问题

> 但是插入操作还是会产生幻读现象

#### 在 repeatable read 基础上解决幻读

> 通过添加 GAP 锁来解决幻读现象

#### GAP

> 当我们用范围条件检索数据而不是相等条件检索数据，并请求共享或排他锁时，InnoDB会给符合范围条件的已有数据记录的索引项加锁；对于键值在条件范围内但并不存在的记录，叫做“间隙（GAP)”。InnoDB也会对这个“间隙”加锁，这种锁机制就是所谓的间隙锁。

### serializable;串行化

> 事务按序执行（并发性为 0）

写数据之前先写日志，通过日志来实现redo
通过数据库内部的segment段(undo段)来实现undo.undo段位于共享表空间

显示开启事务
START TRANSACTION(存储过程中只能使用这种方式开启事务) | BEGIN
提交事务
COMMIT
回滚事务
ROLLBACK
创建一个保存点
SAVEPOINT name
删除保存点
RELEASE SAVEPOINT name
回滚至莫保存点
ROLLBACK TO name
查看事务隔离级别
SELECT @@TRANSACTION_ISOLATION;
设置事务的隔离级别
SET TRANSACTION_ISOLATION=0~3

设置自动提交
SET AUTOCOMMIT = 1
不自动提交
SET AUTOCOMMIT = 0
SELECT @@AUTOCOMMIT;
