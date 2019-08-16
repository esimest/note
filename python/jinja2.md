# Jinja2

> [Document](https://jinja.palletsprojects.com/en/2.10.x/templates/)
> J2 依赖 MarkupSafe 模块
> J2 的核心是 Environment 类
> 使用该类的实例来保存 配置、全局变量，以及加载模板文件

## Basic Use

```python
# Work with String template
from jinja2 import Template
template = Template('Hello {{ name }} !')
template.render({"name": "World"})
```

```python
# Work with file system
from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader('myapplication', 'templates'), # 从 myapplication 包中加载 templates 目录下所有所有模板
    autoescape=select_autoescape('html', 'xml')
)
template = env.get_template('mytemplate.html')
template.render(the='variables', go='here')
```

## Syntax

```j2
# 用于表达式的模板
{{% statement %}}

# 用于变量替换的模板
{{ variable }}

# 用于注释
{# comment #}

# 用于行表达式
# statement

# + 用于保留空格，- 用于去除空格

```

## 循环中的变量

```shell
loop.index             The current iteration of the loop. (1 indexed)

loop.index0            The current iteration of the loop. (0 indexed)

loop.revindex          The number of iterations from the end of the loop (1 indexed)

loop.revindex0         The number of iterations from the end of the loop (0 indexed)

loop.first             True if first iteration.

loop.last              True if last iteration.

loop.length            The number of items in the sequence.

loop.cycle             A helper function to cycle between a list of sequences. See the explanation below.

loop.depth             Indicates how deep in a recursive loop the rendering currently is. Starts at level 1

loop.depth0            Indicates how deep in a recursive loop the rendering currently is. Starts at level 0

loop.previtem          The item from the previous iteration of the loop. Undefined during the first iteration.

loop.nextitem          The item from the following iteration of the loop. Undefined during the last iteration.

loop.changed(*val)     True if previously called with a different value (or not called at all).
```

## 模板里可以使用的过滤函数

> 使用方法: {{ var | fun}}

```shell
abs()    float()    lower()    round()    tojson()

attr()    forceescape()    map()    safe()    trim()

batch()    format()    max()    select()    truncate()

capitalize()    groupby()    min()    selectattr()    unique()

center()    indent()    pprint()    slice()    upper()

default()    int()    random()    sort()    urlencode()

dictsort()    join()    reject()    string()    urlize()

escape()    last()    rejectattr()    striptags()    wordcount()

filesizeformat()    length()    replace()    sum()    wordwrap()

first()    list()    reverse()    title()    xmlattr()
```

## 内置测试函数

```shell
callable()    even()    le()    none()    string()

defined()    ge()    lower()    number()    undefined()

divisibleby()    gt()    lt()    odd()    upper()

eq()    in()    mapping()    sameas()    escaped()    iterable()    ne()    sequence()
```
