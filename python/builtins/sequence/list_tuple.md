# List Tuple

## ('a') 和 ('a',)

```python
In [24]: a = ('a')

In [25]: a
Out[25]: 'a'

In [26]: b = ('a',)

In [27]: b
Out[27]: ('a',)
```

## li += [1] 与 li = li + [1]

```python
# li += [1] 与 li.append(1) 的作用是一样的，在列表的最后添加一个元素
# li = li + [1] 的具体实现是,创建一个新的列表，将 li 和 1 插入新列表，并赋值给 li
In [5]: li = [1, 2, 3]

In [6]: id(li)
Out[6]: 98655008

In [7]: li.append(4)

In [8]: id(li)
Out[8]: 98655008

In [9]: li += [4]

In [10]: id(li)
Out[10]: 98655008

In [11]: li
Out[11]: [1, 2, 3, 4, 4]

In [12]: li + [5]
Out[12]: [1, 2, 3, 4, 4, 5]

In [13]: li
Out[13]: [1, 2, 3, 4, 4]

In [14]: li = li + [5]

In [15]: li
Out[15]: [1, 2, 3, 4, 4, 5]

In [16]: id(li)
Out[16]: 98362352
```
