# Python 描述符

> 描述符是定义了 __set__(self, obj, vale) -> None, __get__(self, obj, type=None) -> None, __delete__(self, obj) -> None
> 其中一个方法的类。其中 self为描述符的实例，obj为使用描述符实例作为属性的类的实例，val 为要给改实例设置的值，type为 obj 的类型
> 描述符实例，主要用于作为类属性存在。用于给属性添加特殊行为
> 描述符可以作为类属性的装饰器如 property

## 描述符简单实现

```python
class Quantity:

    def __init__(self, storage_name):
        print('hello')
        self.storage_name = storage_name

    def __set__(self, instance, value):
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
        slef.price = price

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

## descriptorkinds.py

```python

```
