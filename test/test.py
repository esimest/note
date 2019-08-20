""" 辅助函数，仅限于显示 """


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
    对托管实例的属性的读写行为通过描述符实例的 __get__ 和
    __set__ 方法来实现 --> 类属性覆盖实例属性的行为
    """

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class OverridingNoGet:
    """
    没有```__get__```方法的覆盖型描述符
    对托管实例的属性的写操作使用描述符实例的 __set__
    方法来实现。读取托管实例的属性时返回实例属性(
        如果实例属性不存在，返回同名的描述符实例
    )
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
