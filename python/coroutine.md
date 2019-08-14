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

## async 实现
