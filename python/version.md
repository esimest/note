# Python3 和 Pyton2 的区别

## 关键字

```python3
# nonlocal, async, await 为新增关键字
# exec 之前是关键字，现在是内置函数
```

## 编码

> 之前是 ASCII 现在是 UTF-8 编码

## 内置函数

> ascii(), exec(), breakpoint()
> reduce() 移动到了 functools 模块下

## 语法特性

1. 添加了类型注解
2. 字典有序插入


## 包管理

## 协程

> 之前使用 yield + gevent, 现在使用 asyncio + async + await

## 迭代

> range zip map 等函数放回迭代器而不列表

## 字符串格式化

> Python3 支持 str.format(*args, **kwargs) 和 f'{str}'

## 模块

### 新增

1. asyncio
2. enmu
3. pathlib