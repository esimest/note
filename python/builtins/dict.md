# dict

## 关于 dict 的键

> 所有可 Hash 的对象都可作为 dict 的键 <==> isinstance(var, collections.abc.Hashable)

- 特殊的字典 key
  1. None
  2. True, False(数据类型的实例，True, False, None 都为单例类型的实例),(其它的关键字都不能作为字典的 key 使用，也不能当作变量使用)
  3. 所有类名(包括内置类型如:int float str ...)(但是不包括 class 关键字)
  4. 所有函数名(包括内置函数: len sorted ...)
  5. 空元组 '()'
  6. 空字符串 '' ""

## dict 基本操作

```yaml
# 字典的键由具有唯一的 hashable 对象组成
# 构造方法 :  class dict(**kwarg)  class dict(mapping, **kwarg)  class dict(iterable, **kwarg)
- 构造方法:
  - dict(mapping, **kwg): >
      dict((('name', 'json'),))
      dict((('name', 'json'), ('age', 20), ('gender', 'male')))
      dict([('name', 'json'), ('age', 20), ('gender', 'male')])
      dict(zip(['name', 'age', 'gender'], ['json', 20, 'male']))
      ... 还有其它的，只要符合 mapping 是可迭代的，其中每项也是可迭代
  - dict(iterable, **kwg): >
      dict({"name": "json", "age": 20, "gender": "male"})
      ...
  - dict(**kwg):
      dict(name="json", age="20", gender="male")
- 内置字典操作:
  - len(d) : 字典长度
  - d[key] : 根据 key 获取 valuea
  - d[key] = value : 修改 key 对应的 value
  - del d[key] : 删除 key-value 对
  - (key in d) (key not in d) : 键是否在字典中
  - iter(d) : 返回键组成的迭代器
- 字典方法:
  - d.clear() : 清空字典
  - d.copy() : 浅拷贝
  - classmethod fromkeys(iterable[, value]) : 使用iterable的元素为键，value为值创建新字典
  - d.get(key[, default]): 根据 key 获取value,如果 key 不存在 返回default
  - d.items(): 返回 (key, value) 构成的新视图
  - d.keys() : 返回键构成的视图
  - d.pop(key[, default]) : 取出 key-value, 返回value,如果key不存在返回 default
  - d.popitem(): 取出 (key, value) 顺序为 LIFO
  - d.setdefault(key[, default]): 如果存在 key 返回 value, 否则插入 (key,default)
  - d.update(other): 更新字典
  - d.values(): 返回 value 构成的视图
- 字典视图对象:
  - dict_keys
  - dict_items
  - dict_values
- 字典视图对象操作: len iter in
```
