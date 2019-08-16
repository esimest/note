# Python 协程

## yield 实现

- 协程中的一些概念
  1. 协程函数: (包含 a = yield b) 语句的函数
  2. 协程: 协程函数的返回值
  3. 调用方: 触发协程的对象

> 根本上，yield 通过流程控制来实现生成器和协程的功能
> 当将生成器的　yield express 表达式修改成 result = yield express 时，生成器就成了协程

### 生成器的状态

> 生成器有四种状态，分别为：GEN_CREATED GEN_RUNNING GEN_SUSPENDED GEN_CLOSED
> 只有当生成器处于 GEN_SUSPENDED 状态时，才能使用 gen.send(var) 将非 None 数据发送给携程

```python
In [1]: from inspect import getgeneratorstate as gen_state
   ...:
   ...: def simple_coro(a):
   ...:     print(f'-> Started: a = {a}')
   ...:     b = yield a
   ...:     print(f'-> Received: b = {b}')
   ...:     c = yield a + b
   ...:     print(f'-> Received: c = {c}')
   ...:

In [2]: my_coro = simple_coro(14)  # 通过生成器函数创建协程

In [3]: gen_state(my_coro)
Out[3]: 'GEN_CREATED'

In [4]: next(my_coro) # 预激生成器
-> Started: a = 14
Out[4]: 14

In [5]: gen_state(my_coro)
Out[5]: 'GEN_SUSPENDED'

In [6]: my_coro.send(28)
-> Received: b = 28
Out[6]: 42

In [7]: my_coro.send(99)
-> Received: c = 99
---------------------------------------------------------------------------
StopIteration                             Traceback (most recent call last)
<ipython-input-7-801ea47a7792> in <module>
----> 1 my_coro.send(99)

StopIteration:

In [8]: gen_state(my_coro)
Out[8]: 'GEN_CLOSED'

```

### 结束协程与协程的异常处理

- 使用 throw 或 close 方法时，是引发异常，而不是将异常赋值给 yield 的左值
- 使用 send() 方法可以将异常赋值

> 协程中未处理的异常会向上冒泡，传给 next 或 send 函数的调用者
> --> 所以终止协程的一种方法是：传递一个参数在协程内引发协程处理不了的异常

- 调用生成器的 throw 方法向生成器传递异常
  > generator.throw(exc_type[, exc_value[, traceback]]) 在协程的 yield 表达式处引发异常

- 显式关闭协程
  > 调用 generator.close(), 该函数会在 yield 表达式处引发 GeneratorExit 异常
  > 如果协程在该位置没有处理 GeneratorExit 或触发了 StopIteration 则协程正常结束，调用方不会接收到任何异常或消息
  > 如果协程在 yield 语句处，处理了该异常则在 except 语句处一定不能使用 yield(或者说产出值), 否则会引发 RunTimeError

### 使用 return 在协程中返回值

> 在协程的最后使用 return 返回值，但是获取返回值的方式不是通过赋值的方式
> 而是通过 StopIteration.value 来获取

### yield from

- 委派生成器
   > 包含 yield from <iterable> 语句的生成器函数

- 子生成器
   > yield from <iterable> 语句中的 iterable

- 调用方
   > 使用委派生成器的客户端代码

> yield from: 在子生成器结束之前，当调用方对委派生成器调用 send 时，将程序的控制权交给子生成器
> 子生成器的返回值为 yield from 表达式的值

```python
from collections import namedtuple


Result = namedtuple('Result', 'count average')
data = {
    'girls;kg':
        [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
    'girls;m':
        [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
    'boys;kg':
        [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
    'boys;m':
        [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46],
}


def averager():
    total, count, average = 0.0, 0, None
    while True:
        # main 函数通过 send 传递的值来到了这里
        term = yield
        if term is None:
            break
        total += term
        count += 1
        average = total / count
    # 子生成器的返回值，会在协程结束时作为 StopIteration.value
    # 返回给子生成器的调用方(委派生成器)
    return Result(count, average)


def grouper(results, key):
    while True:
        # 这里的左值不是调用方使用 send 方法传递的，而是 yield from 表达式的值
        # yield from 表达式的值为子生成器使用 return 返回的值
        # yield 会捕捉子生成器抛出的 StopIteration
        # 并获取 StopIteration.value 作为表达式的值
        results[key] = yield from averager()


def main(data):
    results = {}
    for key, values in data.items():
        group = grouper(results, key)
        next(group)
        for value in values:
            group.send(value)
        group.send(None)

    print(results)
    report(results)


def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{}'.format(
            result.count, group, result.average, unit
        ))

```

#### yield from 表达式的意义

1. 子生成器产出的值都直接传给委派生成器的调用方
2. 调用使用 send() 方法发给委派生成器的值都直接传给子生成器。
   如果发送的值是None，那么会调用子生成器的 __next__() 方法。
   如果发送的值不是 None，那么会调用子生成器的 send() 的方法。
   如果调用的方法导致子生成器抛出 StopIteration 异常，那么
   委派生成器恢复运行。任何其他异常都会向上冒泡，传给委派生成器。
3. 生成器退出时，生成器中的 return 表达式会触发 StopIteraion
   异常抛出
4. yield from 表达式的值是子生成器终止时传递给 Stopiteraion
   异常的第一个参数。
5. 传入委派生成器的异常，除了 GeneratorExit 之外都传给子生成器的
   throw 方法。如果调用子生成器的 throw 方法时抛出 StopIteration
   异常，委派生成器恢复运行。StopIteration 之外的异常会向上冒泡，
   传给委派生成器
6. 如果把 GeneratorExit 异常传入委派生成器，或者在委派生成器上调用
   close 方法，那么在子生成器上调用 close 方法。如果调用 close 方法导致
   异常抛出，那么异常会向上冒泡，传给委派生成器。否则，委派生成器抛出 GeneratorExit
   异常。

```python
# yield from 表达式干了啥
_i: 子生成器
_y: 子生成器产出的值 <==> 子生成器中 yield var 中的 var
_r: yield from 表达式的值
_s: 调用方发送给委派生成器的值，这个值会通过委派生成器直接传给子生成器
_e: 异常对象

# 以下伪代码相当于 RESULT = yield from EXPR 的内部实现
_i = iter(EXPR)
try:
    _y = next(_it) # 预激子生成器
except StopIteration as _e:
    _r = _e.value
else:
    while True:
        try:
             # 引发异常的部分在于 gen.throw/gen.close
            _s = yield _y
        except GeneratorExit as _e: # 委派生成器调用 throw/close
            try:
                _m = _i.close # 判断子生成器是否具备 close 方法
            except AttributeError:
                pass # 啥都不做就结束子生成器返回到委派生成器
            else:
                _m() # 调用子生成器的 close 方法
            raise _e # 如果 close 没有退出生成器则引发异常
        except BaseException as _e: # throw 方法传入其它的异常
            _x = sys.exc_info() # 暂时看不大懂
            try:
                _m = _i.throw # 判断存不存在 throw 方法
            except AttributeError:
                raise _e
            else:
                try:
                    _y = _m(*_x) # 调用子生成器的 throw 方法
                except StopIteration as _e:
                    # 如果子生成器中引发该异常，将 return 的返回值作为 StopIteration.value 作为 yield from 的返回值
                    _r = _e.value
                    break
        else: # gen.send
            try:
                if _s is None:
                    _y = next(_i)
                else:
                    _y = _i.send(_s)
            except StopIteration as _e:
                _r = _e.value
                break
    RESULT = _r
```

## async 实现
