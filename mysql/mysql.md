#### 数据库范式
1. 第一范式 
>> 属性不可拆分(无重复的列)
2. 第二范式
>> (每行必须有一个唯一的主键，非主属性对其完全依赖)
3. 第三范式
>> 消除传递依赖，非主属性只能依赖与候选码，而不能依赖于其它非主属性
4. BC范式
>> 存在多个候选码时(即多个可唯一标识一行的属性时)  需满足一下条件
1. 所有非主属性对每一个码都是完全函数依赖；
2. 所有的主属性对于每一个不包含它的码，也是完全函数依赖；
3. 没有任何属性完全函数依赖于非码的任意一个组合。

#### 数据库优化
1. sql优化
   - 对于使用like的查询，查询如果是  ‘%aaa’ 不会使用到索引，‘aaa%’ 会使用到索引。
   - 使用where时 避免对索引使用!= <> 或者函数，会导致索引失效，进而使用全表扫描
   - 对有null判断的语句会使用全表扫描
   - 用where代替having, having是在结果查询完之后进行过滤
   - 多表关联时，尽量不要超过三到四个。如果超过可以使用中间表过度
2. 数据库结构优化
   - 范式优化：如消除冗余
   - 反范式优化： 适当冗余以减少关联
   - 使用分区： 加快查询速度

3. 索引优化
    - 添加适当的索引

4. mysql配置    
   - 配置最大并发数
   - 调整缓存大小

> `show variables like 'long_query_time';` 慢查询时间变量

> `show status like 'slow_queries';` 查看慢查询语句

> explain用于分析sql如何执行

> `alter tbale tab_name add primary key column_name` 添加约束

> `create index index_name on table_name(column_name)` 添加索引

> `alter table tab_name drop index index_name` 删除索引

> `show index(es) from tab_name; show keys from tab_name;` 查询索引

> 建索引的条件：*where子句常用，字段值不止几个，内容不经常变化*
---
#### 数据库备份
##### mysqldump(全量)
> 备份时会锁表，适合在业务较少时操作
```
mysqldump [OPTIONS] database [tables]
mysqldump [OPTIONS] --databases [OPTIONS] DB1 [DB2 DB3...]
mysqldump [OPTIONS] --all-databases [OPTIONS]

-F 备份前刷新二进制日志(等同于mysql> flush logs;)
```
##### mysqlbinlog(增量)
> my.conf 配置 bin_log=log_name mysql8默认开启
```
mysqlbinlog [options] log-files
--start-position=953                   起始操作节点
--stop-position=1437                   结束操作节点
--start-datetime="yyyy-mm-dd hh:MM:ss" 起始时间点
--stop-datetime="yyyy-mm-dd hh:MM:ss"  结束时间点
--database=datebase_name               指定恢复的数据库

定位节点对应的数据库操作(文件过大只能查看全部, 不能指定范围)
show binlog events [IN 'log_name'] [FROM pos] [LIMIT [offset,] row_count];
```