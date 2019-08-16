# 函数装饰器

## 常规函数装饰器（装饰器函数只接受一个函数名作为参数）

```python
'''
函数装饰器就是一个函数，它接受一个函数作为参数，返回一个新的函数
以下两种写法效果是一样的

@timethis
def countdown(n):
    pass

def countdown(n):
    pass
countdown = timethis(countdown)
'''
import time
from functools import wraps

def timethis(func):
    '''
    计算函数执行时间的装饰器
    '''
    '''
    @wraps(func)
    def wrapper():
        pass
    将 wrapper 的 ('__module__', '__name__', '__qualname__', '__doc__',
                   '__annotations__') 属性的值设置为 func 的对应值
    没有被修饰的 func 可以通过 wrapper.__wrapped__ 属性获取
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end-start)
        return result
    return wrapper

@timethis
def countdown(n):
    '''
    Counts down
    '''
    while n > 0:
        n -= 1

```

## 带参函数装饰器

```python
'''
以下两种写法效果是一样的
@decorator(*args, **kwargs)
def func(*args1, **kwargs1):
    pass

def func(*args1, **kwargs1):
    pass
func = decorator(*args, **kwargs)(func)
'''

import logging
from functools import wraps

def logged(level, name=None, message=None):
    '''
    给函数添加日志功能
    level : 日志的等级
    name : 记录器的名字，默认使用函数的模块名
    message : 日志发送的消息，默认使用函数的名称
    '''
    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)
        return wrapper
    return decorate

# Example use
@logged(logged.DEBUG)
def add(x, y):
    return x + y

@logged(logging.CRITICAL, 'example')
def spam():
    print('Spam!')

```
