# Python 描述符

> 描述符是定义了 __set__(self, obj, vale) -> None, __get__(self, obj, type=None) -> None, __delete__(self, obj) -> None
> 其中一个方法的类。其中 self为描述符的实例，obj为使用描述符实例作为属性的类的实例，val 为要给改实例设置的值，type为 obj 的类型
> 描述符实例，主要用于作为类属性存在。用于给属性添加特殊行为
> 描述符可以作为类属性的装饰器如 property
