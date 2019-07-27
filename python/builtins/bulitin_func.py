"""
内置函数
"""

# abs(x)

# all(iterable)

# any(iterable)

# ascii(object)

# bin(x)

# bool([x]) []代表可有可无


def breakpoint_builtin(*args, **kwargs):
    # breakpoint(*args, **kwargs)
    # In builtins.
    import sys
    missing = object()
    hook = getattr(sys, 'breakpointhook', missing)
    if hook is missing:
        raise RuntimeError('lost sys.breakpointhook!')
    return hook(*args, **kwargs)


def breakpoint_sys(*args, **kwargs):
    # In sys.
    import importlib
    import os
    import warnings
    hookname = os.getenv('PYTHONBREAKPOINT')
    if not hookname:
        hookname = 'pdb.set_trace'
    elif hookname == '0':
        return None
    modname, dot, funcname = hookname.rpartition('.')
    if dot == '':
        modname = 'builtins'
    try:
        module = importlib.import_module(modname)
        hook = getattr(module, funcname)
    except:
        warnings.warn(
            'Ignoring unimportable $PYTHONBREAKPOINT: {}'.format(
                hookname
            ), RuntimeWarning
        )
    return hook(*args, **kwargs)


def divide(e, f):
    breakpoint(header='进入调试器')
    return e / f


a, b = 1, 9
print(divide(a, b))

#  class bytearray([source[, encoding[, errors]]])

# class bytes([source[, encoding[, errors]]])

# callable(obj)

# chr(i) 0 <= i <= 1,114,111

# @classmethod

# compile(source, filename, mode, flags=0, dont_inherit=False, optimize=-1)

# class complex([real[, imag]])

# delattr(object, name)

# dir([object])

# divmod(a, b)

# enumerate(iterable, start=0)

# eval(expression, globals=None, locals=None)

# exec(object[, globals[, locals]])

# filter(function, iterable) 可用列表生成式替代

# class float([x])

# format(value[, format_spec])

#  class frozenset([iterable])

# getattr(object, name[, default])

# globals()

# hasattr(object, name)

# hash(object)

# help([object])

# hex(x)

# id(object)

# input([prompt])

# class int([x])

# class int(x, base=10)

# isinstance(object, classinfo)

# issubclass(class, classinfo)

# iter(object[, sentinel])

# len(s)

#  class list([iterable])

# locals()

# map(function, iterable, ...) 可用列表生成式替代

# max(iterable, *[, key, default]) key 为排序方法
# 当 iterable 为空时返回 default 的值，如果未定义引发 ValueError
# max(arg1, arg2, *args[, key])

#  memoryview(obj)

# min(iterable, *[, key, default])
# min(arg1, arg2, *args[, key])

# next(iterator[, default]) 迭代器耗尽返回 default 的值，如果未定义 引发 StopIteration

# class object

#  oct(x)

#  open(file, mode='r', buffering=-1,
#       encoding=None, errors=None, newline=None,
#       closefd=True, opener=None)

# ord(c)

# pow(x, y[, z]) 返回 x 的 y 次方 对 z 取余

# print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)

# class property(fget=None, fset=None, fdel=None, doc=None)

# range(stop)
# range(start, stop[, step])

# repr(object)

# reversed(seq) [::-1]

# round(number[, ndigits])

# class set([iterable])

# setattr(object, name, value)

# class slice(stop)
# class slice(start, stop[, step])

# sorted(iterable, *, key=None, reverse=False)

# @staticmethod

# class str(object='')
# class str(object=b'', encoding='utf-8', errors='strict')

# sum(iterable[, start])

# tuple([iterable])

# class type(object)
# class type(name, bases, dict)

# vars([object])

# zip(*iterables)
