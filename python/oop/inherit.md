# 关于 Python 继承

## super

[super 文档](https://mozillazg.com/2016/12/python-super-is-not-as-simple-as-you-thought.html)

> super 是个类， super(__class__) 返回的是 __class__ 的代理

### 调用方式

```python
super() -> same as super(__class__, <first argument>)
super(type) -> unbound super object
super(type, obj) -> bound super object; requires isinstance(obj, type)
super(type, type2) -> bound super object; requires issubclass(type2, type) Typical use to call a cooperative superclass method: class C(B):
    def meth(self, arg):
        super().meth(arg) This works for class methods too:
class C(B):
    @classmethod
    def cmeth(cls, arg):
        super().cmeth(arg)
```

## 菱形继承问题

问题:
当子类继承自多个类时，其中有多个父类定义了一个同名方法(例如:foo() 方法)。
当子类使用 super().foo() 或子类的实例直接调用 foo 方法时，实际是如何实现的？

MRO:
Method Resolution Order

解决:
每个类都有一个 __mro__ 属性，该属性是一个 tuple，其中的项为类本身以及它的所有父类。该元组使用 3C 算法进行排序。
当子类调用父类的方法时，按从左到有顺序遍历 __mro__ 检查父类是否具有 foo 方法，如果有就是用该类的 foo 方法，如果没有就继续寻找

### super 的不同构造方法，对 __mro__ 的影响

```python
super(cls, obj)
# 当使用上述构造方法时，super 所指定的 __mro__ 元组为 type(obj).__mro__，super 所指定的类为 type(obj)。意味着 issubclass(type(obj), cls) is True

super(cls1, cls2)
# 当使用上述构造方法时，super 所指向的 __mro__ 为 cls2.__mro__，
# super 所指定的类为 cls1。意味着 issubclass(cls2, cls1) is True
```

#### super(cls, obj)

```python
class Base():
    def __init__(self):
        print('Base.__init__')

class A(Base):
    def __init__(self):
        print('A.__init__')
        super().__init__()

class B(Base):
    def __init__(self):
        print('B.__init__')
        super().__init__()

class C(A, B):
    def __init__(self):
        print('C.__init__')
        super().__init__()

>>> C.__mro__
(<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>, <class '__main__.Base'>, <class 'object'>)
>>> C()
C.__init__
A.__init__
B.__init__
Base.__init__
<__main__.C object at 0x03837A70>

c = C() 所导致的 __init__ 执行过程如下:
1. C.__init__ -> print('C.__init')

2. C._init__ -> super().__init__() <==> super(C, c).__init__()
  即此时的 __mro__ 为 type(c).__mro__ == C.__mro__，类为 C == C.__mro__[0]

3. 此时按照 C.__mro__  和 super 所对应的类(C)。访问 C.__mro__ 中下一位即 A.__init__，执行 print('A.__init__')

4. A.__init__ -> super().__init() <==> super(A, c).__init__()
  即此时的 __mro__ 依然为 type(c).__mro__，但是此时的类为 A == C.__mro__[1]

5. 此时按照 C.__mro__ 和 super 所对应的类(A)。访问 B.__init__，执行 print('B.__init__')

6. B.__init__ -> super(B, c).__init__()。此时的 __mor__ 依然为 type(c).__mro__，super 对应的类为 B == C.__mro__[2]


7. 访问 Base.__init__()
```
