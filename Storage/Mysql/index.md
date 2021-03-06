# Mysql 索引

## 优缺点

### 优点

有点:

索引的出现就是用来解决查询慢的问题，所以一个索引必带的优点就是提高查询效率

缺点(难点):

B-Tree 索引是一个平衡树，因此当增加或删除数据时需要维护索引的结构。频繁的增减操作会影响性能

## 原理

> 只有叶子节点存储具体索引的相关信息。非叶子节点只是引导到具体的索引

> 模糊查询，大于小于会使索引失效
> 最左匹配: a=1 and b>2 and c=3, 最会用到索引 a; a=1 and c=3 and b>2 会用到索引 a b

## 类别

- 聚集索引
   > 表数据按照索引的顺序来存储的。对于聚集索引，叶子结点即存储了真实的数据行，不再有另外单独的数据页。
- 非聚集索引
   > 表数据存储顺序与索引顺序无关。对于非聚集索引，叶结点包含索引字段值及指向数据页数据行的逻辑指针，该层紧邻数据页，其行数量与数据表行数据量一致。

### B-Tree 索引
- 主键索引
   > 唯一、NOT NULL

- 唯一索引
   > 唯一

- 普通索引

- 组合索引

### R-Tree 索引

### Hash 索引

### Full-text 索引

- 全文索引