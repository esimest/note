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

# 离开会话 esime(处在 会话中，执行此命令脱离会话)
screen -d esime

# 回到 esime 会话
screen -r esime

# 清除 dead 的会话
screen -wipe

# 显示所有 会话中可用的 screen 命令
Ctrl + a + ?

# 创建一个新 window 并切换至新 window
Ctrl + a + c

# 切换至下（上）一个 window
Ctrl + a + n(p)

# 脱离当前 session
Ctrl + a + d

# 结束当前 session
exit
Ctrl + d

# 显示当前会话的时间
Ctrl + a + t

# 杀死当前窗口
Ctrl + a + k

# 关闭 esime
Ctrl + a + quit

# 进入复制模式
Ctrl + a + [

# 退出复制模式
Ctrl + a + ]

# 解除链接.unlink 不会发出错误消息，所以需要人工校验是否执行成功
unlink link_name
# 使用 link 做链接时尽量不要用 .

# 删除空目录
rm -d empty_dir
rmdir empty_dir

# 删除多级空目录,rmdir 只能删除空目录
rmdir -p a/b/c

# rm  touch cp 命令结束选项使用 --
# 删除 -foo 文件
rm '-foo' /rm -foo 都会失败
rm -- -foo 或 rm ./-foo

# rm 和 cp  的 -r -R --recursive 作用一样
```
