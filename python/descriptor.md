# Python 描述符

> 描述符是定义了 __set__(self, obj, vale) -> None, __get__(self, obj, type=None) -> None, __delete__(self, obj) -> None
> 其中一个方法的类。其中 self为描述符的实例，obj为使用描述符实例作为属性的类的实例，val 为要给改实例设置的值，type为 obj 的类型
> 描述符实例，主要用于作为类属性存在。用于给属性添加特殊行为
> 描述符可以作为类属性的装饰器如 property

## 描述符简单实现

```python
"""
##################### 描述符相关的几个概念 #################
描述符类：实现了描述符协议的类
描述符实例：描述符类的实例（管理托管属性的读写）
托管类：把描述符实例声明为类属性的类
托管实例：托管类的实例
托管属性：托管类中由描述符实例处理的公开属性
存储属性：托管实例中存储自身托管属性的属性（存储托管属性的值）
"""

class Quantity: # 实现了描述符协议的类就是描述符
    """"
    由于托管属性与存储属性的名称一样，所以调用 instance.key
    就可以获取对应属性的值，因此无需定义 __get__ 方法
    """
    def __init__(self, storage_name):
        """
        storage_name: 对应为托管实例的存储值属性的名称
        """
        self.storage_name = storage_name

    def __set__(self, instance, value):
        """
        当尝试为托管属性赋值时，会调用描述符实例的 __set__ 方法
        self: 描述符实例自身
        instance: 托管实例
        value: 要给托管属性设置的值
        """
        if value > 0:
            instance.__dict__[self.storage_name] = value
        else:
            raise ValueError('value must be > 0')


class LineItem:

    weight = Quantity('weight')
    price = Quantity('price')

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

############################################


class Quantity:
    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = '_{}#{}'.format(prefix, index)
        cls.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        if value > 0:
            setattr(instance, self.storage_name, value)
        else:
            raise ValueError('value must be > 0')


class LineItem:
    weight = Quantity()
    price = Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

##########################################3

import abc


class AutoStorage:
    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = '{}#{}'.format(prefix, index)
        cls.__counter += 1

    def __get__(self, isinstance, owner):
        if isinstance is None:
            return self
        else:
            return getattr(isinstance, self.storage_name, value)

    def __set__(self, isinstance, value):
        setattr(isinstance, self.storage_name, value)


class Validated(abc.ABC, AutoStorage):
    def __set__(self, isinstance, value):
        value = self.validate(isinstance, value)
        super().__set__(isinstance, value)

    @abc.abstractmethod
    def validate(self, isinstance, value):
        """return validated value or raise ValueError"""


class Quantity(Validated):
    """a number greater than zero"""

    def validate(self, isinstance, value):
        if value <= 0:
            raise ValueError('value must be >0')
        return value


class NonBlank(Validated):
    """"a string with at least one non-space character"""

    def validate(self, isinstance, value):
        value = value.strip()
        if len(value) == 0:
            raise ValueError('value cannot be empty or blank')
        return value


class LineItem:
    description = NonBlank()
    weight = Quantity()
    price = Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

```

## 描述符分类

```python
def cls_name(obj_or_cls):
    cls = type(obj_or_cls)
    if cls is type:
        cls = obj_or_cls
    return cls.__name__.split('.')[-1]


def display(obj):
    cls = type(obj)
    if cls is type:
        return '<class {}>'.format(obj.__name__)
    elif cls in [type(None), int]:
        return repr(obj)
    else:
        return '<{} object>'.format(cls_name(obj))


def print_args(name, *args):
    pseudo_args = ', '.join(display(x) for x in args)
    print('-> {}.__{}__({})'.format(args[0], name, pseudo_args))


class Overriding:
    """"
    也称数据描述符或强制描述符 -->
    对托管实例或托管类的属性的读写都是通过描述符实例的
    __get__ __set__ 方法来实现
    """

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class OverridingNoGet:
    """
    没有```__get__```方法的覆盖型描述符
    对托管实例的和托管类属性的写操作使用描述符实例的 __set__
    方法来实现。读取托管实例的属性时返回实例属性(
        如果实例属性不存在，返回同名的描述符实例
    )。读取托管类的属性直接返回描述符实例
    """

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class NonOverriding:
    """
    也称非数据描述符或遮盖型描述符
    对托管实例属性的访问采用以下原则(
        如果存在该实例属性，使用实例属性覆盖描述符实例
        如果不存在实例属性：
            读值时返回描述符实例
            写值时使用新的属性值覆盖描述符实例
    )
    """

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)


class Managed:
    over = Overriding()
    over_no_get = OverridingNoGet()
    nono_over = NonOverriding()

    def spam(self):
        print('-> Managed.spam({})'.format(display(self)))
```

```shell
################ 测试结果 ################
[3]: # 覆盖型描述符：读写托管属性时实例属性与类属性的行为

In [4]: obj = Managed()

In [5]: obj.over  # 获取托管实例属性 --> 描述符的 __get__ 方法
-> <__main__.Overriding object at 0x054C59D0>.__get__(<Overriding object>, <Managed object>, <class Managed>)

In [6]: Managed.over # 获取托管类的属性 --> 描述符的 __get__ 方法
-> <__main__.Overriding object at 0x054C59D0>.__get__(<Overriding object>, None, <classManaged>)

In [7]: obj.over = 7  # 对托管实例属性的写值操作 --> 描述符的 __set__ 方法
-> <__main__.Overriding object at 0x054C59D0>.__set__(<Overriding object>, <Managed object>, 7)

In [8]: obj.over  # 再次获取托管实例的属性  --> 描述符的 __get__ 方法
-> <__main__.Overriding object at 0x054C59D0>.__get__(<Overriding object>, <Managed object>, <class Managed>)

In [9]: # 没有 __get__ 方法的覆盖型描述符的读写行为

In [10]: obj.over_no_get  # 实例属性不存在时，返回类属性 --> 描述符实例
Out[10]: <__main__.OverridingNoGet at 0x54c5e30>

In [11]: Managed.over_no_get  # 读取类属性 --> 直接返回类属性
Out[11]: <__main__.OverridingNoGet at 0x54c5e30>

In [12]: obj.over_no_get = 7  # 写入实例属性 --> 使用描述符实例的 __set__
-> <__main__.OverridingNoGet object at 0x054C5E30>.__set__(<OverridingNoGet object>, <Managed object>, 7)

In [13]: obj.over_no_get # 由于上一步的 __set__ 方法并没有实际写入属性的值，因此该属性任然不存在
Out[13]: <__main__.OverridingNoGet at 0x54c5e30>

In [14]: obj.__dict__['over_no_get'] = 9 # 通过 __dict__ 将属性写入实例

In [15]: obj.over_no_get # 实例属性存在，直接返回实例属性的值
Out[15]: 9


In [17]: obj.nono_over  # 实例属性不存在，使用描述符的 __get__ 替代
-> <__main__.NonOverriding object at 0x054C5E90>.__get__(<NonOverriding object>, <Manage
d object>, <class Managed>)

In [18]: obj.non_over = 7 # 写入实例属性

In [19]: obj.non_over  # 实例属性存在，返回属性的值
Out[19]: 7

In [20]: Managed.nono_over # 类属性读取，调用描述符实例的 __get__ 方法
-> <__main__.NonOverriding object at 0x054C5E90>.__get__(<NonOverriding object>, None, <class Managed>)

In [21]: del obj.non_over # 删除实例属性

In [22]: obj.nono_over  # 实例属性不存在，使用描述符的 __get__ 方法
-> <__main__.NonOverriding object at 0x054C5E90>.__get__(<NonOverriding object>, <Managed object>, <class Managed>)


# 对类属性的写操作，不会调用 __set__ 方法，直接覆盖描述符
In [28]: obj = Managed()

In [29]: Managed.over = 1

In [30]: Managed.over_no_get = 2

In [31]: Managed.nono_over = 3

In [32]: obj.over, obj.over_no_get, obj.nono_over
Out[32]: (1, 2, 3)

```

## Python 方法是描述符

> 用户自定义函数都有 __get__ 方法，所以依附到类上时，相当于描述符。

```shell

In [37]: obj = Managed()

In [38]: obj.spam # obj.spam 获取的是绑定方法对象
Out[38]: <bound method Managed.spam of <__main__.Managed object at 0x062E6AF0>>

In [39]: Managed.spam # 通过托管类访问函数时，返回的是函数自身的引用
Out[39]: <function __main__.Managed.spam(self)>

In [40]: obj.spam = 7 # 函数没有实现 __set__ 方法，所以该方法是非覆盖型描述符

In [41]: obj.spam
Out[41]: 7


```
