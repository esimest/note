#  比较 [] 和 list() 两个创建列表的优略性
#  总结： [] 比 list() 更 pythonic
from timeit import timeit

print(f"timeit('[]'): {timeit('[]')} \
        \ntimeit('list()'): {timeit('list()')}")


def list_comp():
    """
        dirrerent between [] and list()
    >>> from dis import dis
    >>> dis('[]')
    1           0 BUILD_LIST               0
                2 RETURN_VALUE
    >>> dis('list()')
    1           0 LOAD_NAME                0 (list)
                2 CALL_FUNCTION            0
                4 RETURN_VALUE

        list() 和 [] 行为上的差异性
    list() 只接受一个可迭代的参数，或者参数为空
    [] 可以接受任意多个参数

    >>> foo_dict = {"1":"foo", "2":"bar"}
    >>> [foo_dict]
    [{'1': 'foo', '2': 'bar'}]

    >>> list(foo_dict)
    ['1', '2']

    """

"""
tuple 和 list 最主要的区别在于：
  tuple 是不可变的(immutable)，大小固定(静态)
  list 是可变的(mutable)，大小可变(动态)
>>> [].__sizeof__()
  20
>>> ().__sizeof__()
  12
4 位用来存储指针（动态），4位是额外分配的空间（防止列表改变时频繁申请空间）
"""

if __name__ == '__main__':
    import doctest
    doctest.testmod()
