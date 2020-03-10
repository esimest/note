# VSCode 快捷键

- 切换
  > 如果打开就关闭，如果没打开就打开


## 通用类

```shell
# 打开快捷键面板
Ctrl K + Ctlr S

# 关闭软件
Ctrl + Shift + W

######## 加解密 ############
# 将选中文本使用 Base64 加密
Ctrl + K Ctrl + E

# 解密
Ctrl + K Ctrl + D
#########################

######## 复制粘贴 ############
# 选中内容向下/上复制
Shift + Alt + Down/Up

#############################

```

## 导航类

```shell
# 光标位置回退/前进(跟浏览器类似的)
Alt + Left/Right
```

## 光标操作

### 移动

```shell
########## 单光标移动 ################
# 光标向下/上移动一行
Down/Up

# 光标向下/上移动一页
PageDown/PageUp

# 移动光标到 Editor 底/顶部
Ctrl + End/Home

# 光标移至行尾/首
End/Home

# 光标向左/右移动一个单词的距离
Ctrl + Left/Right

########### 多光标移动 ##################
# 向下/上一行添加光标
Ctrl + Alt + Down/Up
Ctrl + Shift + Alt + Down/Up

# 向下/上一页中的每行加一个光标
Ctrl + Shift + Alt + PageDown/PageUp

```

### 选择

```shell
# 光标移至 Editor 底/顶部，并选择内容
Ctrl + Shift + End/Home

# 光标移至行尾/首，并选择内容
Shift + End/Home

# 光标向左/右移动，并选中移动区域
Ctrl + Shift + Alt + ArrowLeft/ArrowRight
Shift + ArrowLeft/ArrowRight

# 光标向下/上移动一页并选中内容
Shift + PageDown/PageUp

# 光标向下/上移动，并选中内容
Shift + ArrowDown/ArrowUp

# 选中光标向左/右一个单词的内容
Ctrl + Shift + Left/Right
```

## 视图类

### 关闭类
```shell
# 关闭所有 Groups
Ctrl + K Ctrl + Shift + W

# 关闭所有 Editors 但是不关闭 Groups
Ctrl + K Ctrl + W

# 关闭当前 Group
Ctrl + K W

# 关闭当前 Editor
Ctrl + W(F4)

# 关闭当前 Group 中已保存了的 Editor
Ctrl + K U

# 关闭 WorkSpace
Ctrl + K + F
```
### 打开类
```shell
# 打开 Debug 视图
Ctrl + Shift + D

# 打开资源管理器视图
Ctrl + Shift + E

# 打开扩展视图
Ctrl + Shfit + X

# 打开源码管(Git)理视图
Ctrl + Shift + G

# 打开搜索(搜索模式)视图
Ctrl + Shift + F

# 打开搜索(替换模式)视图
Ctrl + Shift + H

# 快速打开视图(SideBar Explore Docker Git ...)
Ctrl + Q

# 打开已关闭的 Editor
Ctrl + Shift + T

```

### 选择类(光标移动)

```shell
# 从所有 Group 中选择 Editor
Ctrl K + Ctrl P

# 将光标转移到第 n(n > 0) 个 Group 中的 Editor
Ctrl + n

# 将光标转移到 Side Bar
Ctrl + 0

# 将光标转移到上/下/左右面的 Group 中的 Editor 中
Ctrl K + Ctrl (Up/Down/Left/Right)Arrow

# Keep Editor
Ctrl K + Enter

# 打开当前 Group 中最后一个 Editor
Ctrl + 9

# 打开当前 Group 中第一个 Editor
Alt + 0

# 打开当前 Group 中左侧的 Editor
Ctrl + PageUp

# 打开当前 Group 中右侧的 Editor
Ctrl + PageDown

# 按时间顺序打开最近的 Editor
Ctrl + Tab

# 按时间顺序打开最久的 Editor
Ctrl + Shift + Tab
```

### 移动类
```shell

# 将当前 Group 整体向上/下/左/右移动(相对的会改变其它 Group 的位置)
Ctrl K + (Up/Down/Left/Right)Arrow

# 将当前 Editor 移至第一个 Group
Shift + Alt + 1

# 将当前 Editor 移至最后一个 Group
Shift + Alt + 9

# 将当前 Editor 移至右侧 Group
Ctrl + Alt + RightArrow

# 将当前 Editor 移至上左侧 Group
Ctrl + Alt + LeftArrow

# 将当前 Editor 在当前 Group 向左移一位
Ctrl + Shift + PageUp

# 将当前 Editor 在当前 Group 向右移一位
Ctrl + Shift + PageDown

```

### 切换类
```shell
# 切换 Debug Console 面板
Ctrl + Shift + Y

# 切换终端
Ctrl \`

# 切换输出面板
Ctrl + Shift + U

# 切换面板
Ctrl + J

# 切换 Problem 面板
Ctrl + Shift + M

# 切换 Side Bar
Ctrl + B

# 切换 Group 横竖模式
Shift + Alt + 0

```

### 字体调整
```shell
# 还原字体大小
Ctrl + Num(0)

# 字体变大
Ctrl + (=/+)
Ctrl + Num(+)
Ctrl + Shift + (=/+)

# 字体变小
Ctrl + (-/_)
Ctrl + Num(-)
Ctrl + Shift(-/_)
```

### 分屏类

```shell
# 横向切分 Editor
Ctrl + \

# 纵向切分 Editor
Ctrl K + Ctrl \

# 切换全屏
F11

# Toggle Word Wrap
Alt + Z

# 切换禅模式
Ctrl + K Z
```