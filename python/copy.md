# Python 拷贝

> 每个对象都具有 编号、类型和值三个属性，对象的 x 的编号可以通过 id(x) 获取
> 每个对象在创建完成后其编号和类型就固定了。x is y 判断 x 和 y 所引用的对象的编号是否相同，即是否引用同一个对象
> 可变类型与不可变类型的不同在于：可变类型的对象的值是可以改变的，不可变类型的对象的值是无法改变的。
> (一个不可变容器对象如果包含对可变对象的引用，当后者的值改变时，前者的值也会改变；但是该容器仍属于不可变对象，因为它所包含的对象集是不会改变的。因此，不可变并不严格等同于值不能改变，实际含义要更微妙。)

**一个对象的可变性由该对象的类型决定**

## == 和 is

一般情况下对象的比较都用 == ，当和单例对象进行比较是多用 is 如 None, True, False

> is 是 == 的特殊情况，当且仅当两个变量 a,b 符合 id(a) == id(b) 则 (a is b) 为真
> 等价于变量 a,b 指向同一个对象的时候 a is b
> a == b 是 a.__eq__(b) 的另一种写法

```python
a = obj
b = obj

# id 函数，返回变量所指向的对象的地址

# 由于 python 内部维护了一个 -5 ~ 256 的整形数组，每次访问这个范围内的数字时都会返回对应数字的索引。所以 a = 1, b = 1 ==> id(a) == id(b)
In [16]: a, b = 1, 1

In [17]: id(a), id(b)
Out[17]: (1784010928, 1784010928)

In [26]: a, b = 257, 257

In [27]: id(a), id(b)
Out[27]: (85027808, 82616192)

In [18]: c, d = {1}, {1}

In [19]: id(c), id(d)
Out[19]: (85070952, 86872112)

In [21]: id(e), id(f)
Out[21]: (89652240, 89537072)
# 两个相同的字符串的内存地址是相同的
In [23]: g, h = "hello", "hello"

In [24]: g is h
Out[24]: True

In [25]: id(g), id(h)
Out[25]: (86096960, 86096960)
```

## immutable mutable compound atomic

> Python 对象可分为 集合(collections)/混合(compound) 对象与原子(atomic)对象
> atomic obj 都是 immutable ???
> 所以 atomic 是 immutable 的子集 ???

## 可变对象与不可变对象的浅拷贝

> 对于copy.copy 来说，可变对象的 copy 与不可变对象的 copy，操作是不一样的
> immutable obj 的 copy.copy 直接返回原对象的引用
> 而 mutable obj 的 copy.copy 先创建一个新对象，对象内的元素的值都是原对象元素的引用

## 深浅拷贝

> 深浅拷贝的不同只会体现在 compound object(混合对象，包含其它对象的对象) 上
> 对于 atomic 对象来说，深浅拷贝都是返回的原对象的引用
> 而对于 compound 对象来说，深拷贝创建了一个值(即 == 成立)与原对象一样的新对象，除此之外两者没有其它任何关联

### 浅拷贝

```python
def copy(x):
    """Shallow copy operation on arbitrary Python objects.

    See the module's __doc__ string for more info.
    copy.copy
    对于 mutable 对象来说，copy 返回的是一个新对象的引用，
    该对象内部的属性(元素) 是原对象的引用，
    因此，会导致多个对象对同一个可变对象进行修改操作。
    从而影响到其它对象。
    """

    cls = type(x)
    # _copy_dispatch 字典，存储了内置类型的拷贝方法的具体实现
    # 对于 immutable 对象，直接返回该对象的引用
    # 对于 mutable 对象，使用该对象的 copy 方法
    copier = _copy_dispatch.get(cls)
    if copier:
        return copier(x)

    # 对于元类的对象 <==> 类的拷贝，直接返回类的引用
    if issubclass(cls, type):
        # treat it as a regular class:
        return _copy_immutable(x)

    # 对于其他类型的对象，如果定义了 __copy__ 方法，使用该对象的 __copy__ 方法
    copier = getattr(cls, "__copy__", None)
    if copier is not None:
        return copier(x)

    # 如果不符合上述情况则先获取该对象的属性(元素) 的引用
    reductor = dispatch_table.get(cls)
    if reductor is not None:
        rv = reductor(x)
    else:
        reductor = getattr(x, "__reduce_ex__", None)
        if reductor is not None:
            rv = reductor(4)
        else:
            reductor = getattr(x, "__reduce__", None)
            if reductor:
                rv = reductor()
            else:
                raise Error("un(shallow)copyable object of type %s" % cls)

    if isinstance(rv, str):
        return x
    # 然后通过属性(元素) 的引用，从新构造一个对象
    return _reconstruct(x, None, *rv)


# 用于存储内置类型的拷贝方法
_copy_dispatch = d = {}

# 用于 immutable 对象的 拷贝方法 <==> 直接返回对象的引用
# 元组的 x[:] 与 _copy_immutable(x) 是一样的
def _copy_immutable(x):
    return x
for t in (type(None), int, float, bool, complex, str, tuple,
          bytes, frozenset, type, range, slice,
          types.BuiltinFunctionType, type(Ellipsis), type(NotImplemented),
          types.FunctionType, weakref.ref):
    d[t] = _copy_immutable
t = getattr(types, "CodeType", None)
if t is not None:
    d[t] = _copy_immutable

# mutable 对象的拷贝方法：使用可变对象自己的 copy 函数
# 对于可变的对象使用类的构造函数也可以产生浅拷贝，如: li_copy = list(li) dic_copy = dict(dic) ...
# 对于可变的序列来说， x.copy 与 x[:] 是一样的
d[list] = list.copy
d[dict] = dict.copy
d[set] = set.copy
d[bytearray] = bytearray.copy

if PyStringMap is not None:
    d[PyStringMap] = PyStringMap.copy

del d, t

```

### 深拷贝

> 浅拷贝的问题在与，浅拷贝与原对象使用的是内存里的同一份数据。因此会导致数据在不知情的情况下被修改

深拷贝:
创建一个对象的深拷贝是通过创建一个新对象，然后递归的对子对象进行拷贝操作。
因此：深拷贝与原对象物理上没有任何关系

深拷贝的问题:
深拷贝使用的是递归的方式对原对象的子对象进行拷贝，因此会造成循环拷贝的现象

> 深拷贝可以通过 copy.deepcopy() 来实现

```python
def deepcopy(x, memo=None, _nil=[]):
    """Deep copy operation on arbitrary Python objects.

    See the module's __doc__ string for more info.
    """
    # memo 相关信息，详见 _keep_alive 函数
    if memo is None:
        memo = {}

    d = id(x)
    y = memo.get(d, _nil)
    if y is not _nil:
        return y

    cls = type(x)

    copier = _deepcopy_dispatch.get(cls)
    if copier is not None:
        y = copier(x, memo)
    else:
        if issubclass(cls, type):
            y = _deepcopy_atomic(x, memo)
        else:
            copier = getattr(x, "__deepcopy__", None)
            if copier is not None:
                y = copier(memo)
            else:
                reductor = dispatch_table.get(cls)
                if reductor:
                    rv = reductor(x)
                else:
                    reductor = getattr(x, "__reduce_ex__", None)
                    if reductor is not None:
                        rv = reductor(4)
                    else:
                        reductor = getattr(x, "__reduce__", None)
                        if reductor:
                            rv = reductor()
                        else:
                            raise Error(
                                "un(deep)copyable object of type %s" % cls)
                if isinstance(rv, str):
                    y = x
                else:
                    y = _reconstruct(x, memo, *rv)

    # If is its own copy, don't memoize.
    if y is not x:
        memo[d] = y
        _keep_alive(x, memo) # Make sure x lives at least as long as d
    return y

_deepcopy_dispatch = d = {}

# 与 copy 函数所使用的 _copy_immutable 函数一样
## 因此，对于 atomic 对象(不包含其它对象的对象)而言，copy.copy 与 copy.deepcopy 作用是一样的
def _deepcopy_atomic(x, memo):
    return x
d[type(None)] = _deepcopy_atomic
d[type(Ellipsis)] = _deepcopy_atomic
d[type(NotImplemented)] = _deepcopy_atomic
d[int] = _deepcopy_atomic
d[float] = _deepcopy_atomic
d[bool] = _deepcopy_atomic
d[complex] = _deepcopy_atomic
d[bytes] = _deepcopy_atomic
d[str] = _deepcopy_atomic
d[types.CodeType] = _deepcopy_atomic
d[type] = _deepcopy_atomic
d[types.BuiltinFunctionType] = _deepcopy_atomic
d[types.FunctionType] = _deepcopy_atomic
d[weakref.ref] = _deepcopy_atomic

# 对于内置 component 对象(包含其它对象的对象如：list tuple dict ...)而言
## copy.deepcopy 的实现是通过对子对象递归调用 deepcopy 来实现深度拷贝

def _deepcopy_list(x, memo, deepcopy=deepcopy):
    y = []
    memo[id(x)] = y
    append = y.append
    # 循环对列表中的子项进行深度拷贝
    for a in x:
        append(deepcopy(a, memo))
    return y
d[list] = _deepcopy_list

def _deepcopy_tuple(x, memo, deepcopy=deepcopy):
    y = [deepcopy(a, memo) for a in x]
    # We're not going to put the tuple in the memo, but it's still important we
    # check for it, in case the tuple contains recursive mutable structures.
    try:
        return memo[id(x)]
    except KeyError:
        pass
    for k, j in zip(x, y):
        if k is not j:
            y = tuple(y)
            break
    else:
        y = x
    return y
d[tuple] = _deepcopy_tuple

def _deepcopy_dict(x, memo, deepcopy=deepcopy):
    y = {}
    memo[id(x)] = y
    for key, value in x.items():
        y[deepcopy(key, memo)] = deepcopy(value, memo)
    return y
d[dict] = _deepcopy_dict
if PyStringMap is not None:
    d[PyStringMap] = _deepcopy_dict

def _deepcopy_method(x, memo): # Copy instance methods
    return type(x)(x.__func__, deepcopy(x.__self__, memo))
d[types.MethodType] = _deepcopy_method

del d

def _keep_alive(x, memo):
    """Keeps a reference to the object x in the memo.

    Because we remember objects by their id, we have
    to assure that possibly temporary objects are kept
    alive by referencing them.
    We store a reference at the id of the memo, which should
    normally not be used unless someone tries to deepcopy
    the memo itself...
    使用 memo 来保存已经进行过深拷贝的对象，防止循环拷贝
    循环拷贝: 多个对象产生了拷贝闭环或者，单个对象递归拷贝自身
    """
    try:
        memo[id(memo)].append(x)
    except KeyError:
        # aha, this is the first one :-)
        memo[id(memo)]=[x]
```
