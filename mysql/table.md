# MySQL 表管理

## Clone Table

```shell
# CREATE TABLE ... LIKE ... ;
# does not copy foreign key definitions
# dons't copy any DATA DIRECTORY or INDEX DIRECTORY table options
CREATE TABLE new_table LIKE original_table;

# INSERT INTO ... SELECT ... ;
INSERT INTO new_table SELECT * FROM original_table;
INSERT INTO dst_tbl (i, s) SELECT val, name FROM src_tbl WHERE val > 100 AND name LIKE 'A%' GROUP BY name;

# CREATE TABLE ... SELECT ... ;
# 这种方式创建的表，不会同步源表的约束，和默认值以及自增长等属性
CREATE TABLE dst_tbl SELECT * FROM src_tbl;
CREATE TABLE dst_tbl SELECT b, d FROM src_tbl;
CREATE TABLE dst_tbl SELECT c, a, b FROM src_tbl;

# 创建表并添加列
CREATE TABLE dst_tbl
(
    id INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (di)
)
SELECT a, b, c FROM src_tbl;

CREATE TABLE dst_tbl
SELECT inv_no, SUM(unit_cost*quantity) AS total_cost
FROM src_tbl GROUP BY inv_no;

# 显示声明段的约束，以及修改其默认值
CREATE TABLE dst_tbl (PRIMARY KEY (id)) SELECT * from src_tbl;
ALTER TABLE dst_tbl MODIFY id INT UNSIGNED NOT NULL AUTO_INCREMENT;
```

## 创建临时表（自动删除）

> 临时表是会话相关的，多个不同的会话可以同时创建相同名称的临时表而相互不影响
> 临时表可以与非临时表同名，这种情况下使用该表名实际操作的是临时表
> 会话结束时自动删除临时表

CREATE TEMPORARY TABLE tbl_name (... column definitions... );
CREATE TEMPORARY TABLE new_table LIKE original_table;
CREATE TEMPORARY TABLE tbl_name SELECT ... ;

> 不能在一次会话中多次创建同一个临时表

DROP TEMPORARY TABLE IF EXISTS tbl_name;

## 常用的构建唯一表名的方法

```shell
# 随机数
SELECT RAND();
# 进程 ID

# mysql 的 connect_id。每个数据库连接的 connect_id 同
SELECT CONNECTION_ID();

# 使用预执行语句，多次处理类似语句
SET @tbl_name = CONCAT('tmp_tbl_', CONNECTION_ID());
SET @stmt = CONCAT('DROP TABLE IF EXISTS ', @tbl_name);
PREPARE stmt FROM @stmt;
EXECUTE stmt;
DEALLOCATEPREPARE stmt;
SET @stmt = CONCAT('CREATE TABLE ', @tbl_name, ' (i INT)');PREPARE stmt FROM @stmt;
EXECUTE stmt;
DEALLOCATEPREPARE stmt;
```

## 查询表使用的存储引擎

```shell
# 从 information_schema.tables 中查询
SELECT ENGINE FROM information_schema.`TABLES` WHERE TABLE_NAME = 'profile' AND TABLE_SCHEMA = 'cookbook';

# 查询建表语句
SHOW CREATE TABLE profile \G

# 显示表状态
SHOW TABLE STATUS LIKE 'profile' \G
SHOW TABLE STATUS WHERE name = 'profile' \G

# 修改存储引擎为 MyISAM
ALTER TABLE profile ENGINE = MyISAM;
```

## 使用 mysqldump 备份数据

> mysqldump 生成的 SQL 文件，不包含如 CREATE DATABASE 等关于数据库对象的操作
> 使用 mysqldump 生成的 SQL 文件包含 DROP TABLE IF EXISTS ...;

```shell
# 备份 cookbook.mail 表
mysqldump cookbook mail > mail.sql

# 备份 cookbook 所有表
mysqldump cookbook > cookbook.sql

# 拷贝 cookbook 中所有表至 other_db
mysqldump cookbook | mysql other_db

# 重命名 mail
RENAME mail TO new_name;

# 拷贝cookbook 至其他 数据库实例的数据库中
mysqldump cookbook | mysql -uroot -hother-host.com -ppasswd other_db
mysqldump cookbook | ssh other-host.com mysql other_db
```
