"""
Python协议 就是 双下划线方法
__name__ is the module’s name 
__file__ is the pathname of the file from which the module was loaded__file__ the path of module
__dict__ The namespace supporting arbitrary function attributes.
dir(obj) 返回对象的所有属性 或调用 obj.__dir__()方法
ord(character) 返回字符对应的整数值
chr(int) 返回整数对应的字符
__new__(cls,*args,**kwargs) 创建类的实例,返回__intit__的self参数
__init__(self,*args,**kwargs) 初始化实例
__call__(self,*args,**kwargs) 使类的实例可以成为可调用对象即a=A() a()
"""
"""
可调用对象
函数
方法
类
实现了__call__ 协议的类的实例
python -m doctest name.py
"""