# 常用技巧

## script

> script 命令输入后，当前目录会有一个 typescript文件
> 记录着输入 script 之后所有的终端输出
> script -q 结束该模式

## screen

> 使用 screen 创建一个独立的 session，可以通过 screen 的控制语句离开 screen 打开的会话，但是不中断正在执行的命令

```shell
# 创建一个名为 esime 的会话
screen -S esime

# 列出当前所有 会话
screen -ls

# 断开会话 esime
screen -d esime

# 回到 esime 会话
screen -r esime

# 清楚 dead 的会话
screen -wipe

# 显示所有 会话中可用的 screen 命令
Ctrl + a + ?

# 创建一个新 window 并切换至新 window
Ctrl + a + c

# 切换至下（上）一个 window
Ctrl + a + n(p)

# 退出当前 session，当前执行的任务放至后台执行
Ctrl + a + d

# 显示当前会话的时间
Ctrl + a + t

# 杀死当前窗口
Ctrl + a + k

# 关闭 回话
Ctrl + a + quit

# 进入复制模式
Ctrl + a + [

# 退出复制模式
Ctrl + a + ]
```
