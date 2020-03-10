# debug

## 常用技巧

```shell
# 以调试模式运行脚本(添加了调试输出，不影响执行)
bash -x ${script}

# 查看脚本指定行
sed -n ${num}p ${script}

# 查看没有成对双引号的行
grep '"' ${script} | egrep -v '.*".*".*'

```
