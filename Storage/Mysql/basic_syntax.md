# SQL 基本语法

## 增(INSERT INTO)

```sql
# 基本语法
INSERT INTO ${table} VALUES (val_1, val_2,..., val_n),(第二行),(第三行)...,();
INSERT INTO ${table} (col_1, col_2, ..., col_n) VALUES (val_1, val_2,..., val_n),...(第n行);

# 插入查询结果(不能有 VALUES 关键字)
INSERT INTO ${t_dest} SELECT ${columns} FROM ${t_source};
INSERT INTO ${t_dest} ${columns} SELECT ${columns} FROM ${t_source};

SELECT ${columns} INTO ${table_dest} FROM ${table_source};

# 插入关联查询的结果时，必须设置别名
INSERT INTO ${t_dest} FROM SELECT * FROM (SELECT ${columns} FROM ${t_source1} t1 LEFT JOIN ${t_source2} t2 ON t1.col = t2.col) AS ${t_tmp};
```

## 删(DELETE)

```sql
# 基本语法
DELETE FROM ${table}; # 删除所有行
DELETE FROM ${table} WHERE ${key}=${value}; # 删除指定条件的行
```

## 改(UPDATE ... SET)

```sql
# 基本语法
UPDATE ${table} SET col_1=val_1, col_2=val_2 WHERE ${key}=${value};

```

## 查

```sql
# 基本语法
# 单表
SELECT [ALL|DISTINCT|DISTINCTROW]
col_1, col_2, ..., col_n
FROM ${table} [JOIN ...]
[WHERE ...]
[GROUP BY ...]
[HAVING ...]
[ORDER BY ...]
[LIMIT m,n]

```

## 关联

### 内关联(INNER JOIN/JOIN)
```sql

```

### 外关联(OUTER JOIN)

#### 左关联(LEFT OUTTER JOIN/LEFT JOIN)


#### 右关联(RIGHT OUTER JOIN/RIGHT JOIN)


### 全关联(FULL JOIN)