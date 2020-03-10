# 管道与重定向

## 输出重定向

> **1: 标准输出; 2: 便准错误**

- 丢弃标准错误 2 > /dev/null
- 标准输出和标准错误重定向至file 1 > file 2 >&1

```shell
# 将 EOF 后多行作为参数依次传入 command, 并将执行结果重定向到 file
command <<EOF > file  # 或 command > file <<EOF
op1
op2
op...
EOF
```
