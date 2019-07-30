# History

> 命令历史纪录会记载在 ~/.bash_history 目录中，目录的大小由环境变量 ${HISTSIZE} 决定
> ${HISTCONTROL} 设置保存历史纪录的方式 ignoredups:忽略连续的重复的命令 ignorespace:忽略空格开头的命令 ignoreboth: 两者都忽略

```shell
# 查看最近十条历史记录
history +10

# !(历史命令的序号)
执行该命令
```
