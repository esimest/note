# sed 命令

Sed(流编辑器):

stream editor for filtering and transforming text

## 使用场景

> 对特定行(默认所有行) 进行增(i,a)删(d)改(s)查(p)处理

## 使用方式

> sed [命令选项] '[行匹配][动作[动作参数]]' [文件名]

### 常用命令选项

1. -n(shuoutdown): 不输出模式空间内容到屏幕，即不自动打印
2. -e: 执行多个指定的操作内容，与 grep 的 -e 类似
3. -f(script file): 指定脚本文件
4. -r(--regexp-extended): 扩展正则表达式支持
