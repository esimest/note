# 元类

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
# 元类，不能直接实例化
class Meta(type):
    # def __init__(self, *args, **kwargs):
    #     print("There is __init__")
    #     self.init = 'init'
    #     print(dir(self)) 

    def __call__(self, *args, **kwargs):
        print("There is __call__")
        self.call = 'call'
        print(dir(self))

Meta()

```
