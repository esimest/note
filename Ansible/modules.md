# 常用模块

## 修改文件内容

### run_once

命令指在一台机器上执行.

### lineinfile

用于判断指定模式(正则)的行是否在文件中, 以及用 `line` 指定的行替换匹配行. 还可以改变文件权限以及属组, 属主.

- backrefs
  - true: 如果 regexp 匹配则使用 line 替换, 否则不改变原文件;
  - false(默认): 如果 regexp 匹配则使用 line 替换, 否则添加行至尾部.

- state: 行在文件中的最终状态
  - present(默认): 存在, 指定了 line 就替换. 此选项和 line 必须同时出现.
  - absent: 不存在(如果存在就删除). 此选项和 regexp 必须同时出现.

- insertafter/insertbefor: 在匹配行做了替换或删除后, 额外插入一行

- validate: 使用指定命令验证修改后的文件的语法准确性, 如果不同过则不保存.

```yaml
# 删除匹配的所有行
lineinfile:
  path: ${path_of_file}
  regexp: # regular expression, 指定所要匹配的行.
  state: absent # 状态: 删除所有匹配行

# 将 hello 替换成 world 并在后面添加一行 esimest
lineinfile:
  path: ${path_of_file}
  regexp: 'hello'
  line: 'world'
  insertafert: 'esimest'

# 向文件中添加一行 'hello world', 如果已存在则不做修改
lineinfile:
  path: ${path_of_file}
  regexp: 'hello world'

# 修改文件的权限以及属组属主
lineinfile:
  path: ${path_of_fiel}
  mode: 0644
  user: root
  group: root
  line: ''
```
