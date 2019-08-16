# 元类

## 概念

> 类的实例是对象
> 元类的实例是类
> 对类 A 的调用 A()，用的是 type 的 __call__ 方法

## type

```python
type(object_or_name, bases, dict)
param object_or_name

type(object) -> the object's type
type(name, bases, dict) -> a new type(class object)
```

## 创建类

> 创建 Python 类有两种方式(1. 使用 class 定义类，2. 使用 type构造类)

```python
In [1]: class MyClass:
   ...:     data = 1
   ...:

In [2]: instance = MyClass()

In [3]: MyClass, instance
Out[3]: (__main__.MyClass, <__main__.MyClass at 0x5010b90>)

In [4]: instance.data
Out[4]: 1

In [5]: del MyClass

In [6]: MyClass
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
<ipython-input-6-f8ab73cdaae1> in <module>
----> 1 MyClass

NameError: name 'MyClass' is not defined

In [7]: MyClass = type('MyClass', (), {'data':1})

In [8]: instance1 = MyClass()

In [9]: MyClass, instance1
Out[9]: (__main__.MyClass, <__main__.MyClass at 0x5e6b4b0>)

In [10]: instance1.data
Out[10]: 1

```

## __init__ 与 __call__

- 执行条件与顺序

```python
# 正常定义的类（继承自obj），对类名进行调用，会使用 __init__ 方法
class Normal():
    def __init__(self):
        print("There is __init__")
        self.init = 'init'
        print(dir(self))

    def __call__(self):
        print("There is __call__")
        self.call = 'call'
        print(dir(self))

Normal()

```

```python
class Meta(type):
    def __init__(self, *args, **kwargs):
        print("There is __init__")
        self.init = 'init'
        print(dir(self))

    def __call__(self, *args, **kwargs):
        print("There is __call__")
        self.call = 'call'
        print(dir(self))

Meta()

```
