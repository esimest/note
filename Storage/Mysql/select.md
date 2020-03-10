# MySQL 查询

> cookbook.mail 表

## 基本查询

```shell
# 拼接字符串
SELECT t, CONCAT(srcuser, '@', srchost), size FROM mail;

# 格式化日期
SELECT DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i:%s');

# 别名 (AS)
SELECT DATE_FORMAT(t, '%M %e, %Y') AS 'Date of message', CONCAT(srcuser, '@', srchost) AS 'Mesage sender' size AS 'Number of bytes' FROM mail;

# 排序（升序）
SELECT * FROM mail WHERE dstuser = 'tricia' ORDER BY srchost, srcuser;

# 排序（倒序）
SELECT * FROM mail WHERE size > 50000 ORDER BY size DESC;

# 按第 n 列排序（升序）
SELECT * FROM mail ORDERBY n;

# 去重（DISTINCT）
SELECT DISTINCT YEAR(t), MONTH(t), DAYOFMONTH(t) FROM mail;

# 统计不重复的行数
SELECT  COUNT(DISTINCT srcuser) FROM mail;

# NULL 比较( IS 或 <=> )
SELECT NULL IS NULL, NULL <=> NULL, 'A' IS NOT NULL, 'A' <=> 'A';

# 判断 IF(express, true_result, false_result)
return ture_result if express else false_result
SELECT IF('A' IS NULL, 'ture', 'false') AS result;  ==> 'ture'
SELECT IF('A' > 'B', 'A', 'B')                      ==> 'B'

# 判断 NULL: IFNULL(express, true_result)  == IF(express IS NULL, true_result, express)
return true_result if express esle express;
SELECT IFNULL(NULL, 'yes')  ==> 'yes'
SELECT IFNULL('no', 'yes')  ==> 'no'

# 使用视图(view) 保存常用查询。动态更新
CREATE VIEW mail_view AS
SELECT
DATE_FORMAT(t, '%M %e, %Y') AS date_sent,
CONCAT(srcuser, '@', srchost) AS sender,
CONCAT(dstuser, '@', dsthost) AS recipient,
size FROM mail;

# 多表查询（关联）。ON 子句指定的是要进行匹配的列
SELECT id, name, service, contact_name FROM profile INNER JOIN profile_contact ON id = profile_id;

# 多表查询（子查询）
SELECT * FROM profile_contact WHERE profile_id = (SELECT id FROM profile WHERE name = 'Nancy')

# 查询指定数量的行
SELECT * FROM profile LIMIT n;

# 获取表的总行数  LIMIT 子句中不能使用行数，可以使用变量和算数表达式
SELECT SQL_CALC_FOUND_ROWS 8 FROM profile LIMIT 4;  # SQL_CALC_FOUND_ROWS 计算行数
SELECT FOUND_ROWS();                                # 获取行数
```

## 多表查询

### 子查询

### 表关联
