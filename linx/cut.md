# cut

> 打印文件或标准输入中每行中选定的列, 默认的分隔符为 tab

```shell
# 输出 world
echo "hello world" | cut -d' ' -f2

# 输出 /etc/passwd 中每一行以':' 分割的第一列
cut -d':' -f1 /etc/passwd
```
