"""
Jinja2模板引擎  用于渲染模板
模板可以是  任何格式的  纯文本文件

可以在模板中直接使用全局变量
使用 app.context_processor装饰器注册模板上下文处理函数(在调用render_template之前注册)
模板上下文处理函数需要返回包含变量名与值的字典。可以在模板中直接使用

全局对象(在所有模板中都可以使用的对象)
常用全局函数
  range() lipsum() dict() url_for() get_flashed_messages()

使用app.template_global装饰器将函数注册为模板全局函数

Jinja2中的三种界定符
(1) 语句
{% ... %}
(2) 表达式
{{ ... }}
(3) 注释
{# ... #}

可以使用set在模板内自定义变量    
{% set a='a' %}
还可以像下面这样
{% set navigation %}
    <li><a href="/">Home</a>
    <li><a href="/about">About</a>
{% endset %}

过滤器 filter |
使用safe过滤器或转换成Markup()对象保留对象的原始值
使用 app.template_filter装饰器 自定义过滤器

测试器 表3-6 判断变量的属性
使用 app.template_test装饰器  自定义测试器

上述工具都可直接通过app.jinja_env进行配置
"""
"""
模板结构组织

局部模板
{% include '*.html' %}   将局部模板插入到当前模板的指定位置 局部模板一般以 _ 开头

宏(macro) 类似于函数 ，接收参数来构建内容
{% macro function_name(*args,**kwargs) %}
{% endmacro %}
使用 import 导入宏，之后可以在模板中的任意位置调用宏

include 可以使用当前模板的上下文变量，import 不行 需要显示的使用with context声明使用当前模板的上下文变量

继承
使用{% extends 'base.html' %} 继承基模板
extens 必须为子模版的第一个标签
子模版可以对基模板的内容进行 追加 或 覆盖
使用{%- ... %} 和 {% ... -%} 来去除空白
"""
"""
静态文件 css/js/video
静态文件的端点为 static
URL规则 /static/<path: filename>  url_for('static', filename='filename')

Facvicon

使用 app.errorhandler(错误码)装饰器注册错误处理函数
函数接收一个异常类的实例，包含 code name description等常用属性
"""